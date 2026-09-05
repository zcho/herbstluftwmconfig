#!/usr/bin/env python3
import ctypes, sys

x11 = ctypes.CDLL("libX11.so.6")
x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
x11.XOpenDisplay.restype = ctypes.c_void_p

class XkbStateRec(ctypes.Structure):
    _fields_ = [
        ("group", ctypes.c_ubyte),
        ("base_group", ctypes.c_ubyte),
        ("latched_group", ctypes.c_ubyte),
        ("locked_group", ctypes.c_ubyte),
        ("mods", ctypes.c_uint),
        ("base_mods", ctypes.c_uint),
        ("latched_mods", ctypes.c_uint),
        ("locked_mods", ctypes.c_uint),
        ("compat_state", ctypes.c_uint),
        ("grab_mods", ctypes.c_ubyte),
        ("compat_grab_mods", ctypes.c_ubyte),
        ("lookup_mods", ctypes.c_ubyte),
        ("compat_lookup_mods", ctypes.c_ubyte),
        ("ptr_buttons", ctypes.c_uint),
    ]

x11.XkbGetState.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(XkbStateRec)]
x11.XkbGetState.restype = ctypes.c_int
x11.XkbKeycodeToKeysym.restype = ctypes.c_ulong
x11.XkbKeycodeToKeysym.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_int]

dpy = x11.XOpenDisplay(None)
if not dpy:
    sys.exit(1)

state = XkbStateRec()
ret = x11.XkbGetState(dpy, 0x0100, ctypes.byref(state))
if ret != 0:
    sys.exit(2)

# Physical key 'P' (keycode 33): in 'us' it maps to 'p'(0x70), in 'ru' to 'з'(0x6da).
# Determine active language by the keysym in the active group.
P_KEYCODE = 33
sym = x11.XkbKeycodeToKeysym(dpy, P_KEYCODE, state.group, 0)
print("ru" if sym == 0x6da else "us")
