import tkinter as tk
import ctypes
from ctypes import wintypes

# Windows API
user32 = ctypes.windll.user32

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

toggle = False


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("mi", MOUSEINPUT),
    ]


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
    ]


def get_cursor_position():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def move_mouse_relative(dx, dy):
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.mi.dx = dx
    inp.mi.dy = dy
    inp.mi.dwFlags = MOUSEEVENTF_MOVE

    user32.SendInput(
        1,
        ctypes.byref(inp),
        ctypes.sizeof(INPUT)
    )


def keep_alive():
    global toggle

    x, y = get_cursor_position()
    print(f"Pozice kurzoru: {x}, {y}")

    if toggle:
        move_mouse_relative(5, 0)
    else:
        move_mouse_relative(-5, 0)

    toggle = not toggle

    root.after(60000, keep_alive)


root = tk.Tk()
root.title("SLP")
root.geometry("100x50")

label = tk.Label(
    root,
    text="Waiting ..."
)
label.pack(pady=15)

root.after(60000, keep_alive)

root.mainloop()
