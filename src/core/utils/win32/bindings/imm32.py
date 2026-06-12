"""Wrappers for imm32 win32 API functions."""

from ctypes import POINTER, windll
from ctypes.wintypes import BOOL, DWORD, HANDLE, HWND

imm32 = windll.imm32

imm32.ImmGetDefaultIMEWnd.argtypes = [HWND]
imm32.ImmGetDefaultIMEWnd.restype = HWND

imm32.ImmGetContext.argtypes = [HWND]
imm32.ImmGetContext.restype = HANDLE

imm32.ImmReleaseContext.argtypes = [HWND, HANDLE]
imm32.ImmReleaseContext.restype = BOOL

imm32.ImmGetOpenStatus.argtypes = [HANDLE]
imm32.ImmGetOpenStatus.restype = BOOL

imm32.ImmGetConversionStatus.argtypes = [HANDLE, POINTER(DWORD), POINTER(DWORD)]
imm32.ImmGetConversionStatus.restype = BOOL


def ImmGetDefaultIMEWnd(hwnd: int) -> int:
    return imm32.ImmGetDefaultIMEWnd(hwnd)


def ImmGetContext(hwnd: int) -> int:
    return imm32.ImmGetContext(hwnd)


def ImmReleaseContext(hwnd: int, himc: int) -> bool:
    return bool(imm32.ImmReleaseContext(hwnd, himc))


def ImmGetOpenStatus(himc: int) -> bool:
    return bool(imm32.ImmGetOpenStatus(himc))


def ImmGetConversionStatus(himc: int, conversion, sentence) -> bool:
    return bool(imm32.ImmGetConversionStatus(himc, conversion, sentence))
