#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import threading
import os
import re
import struct

try:
    import capstone
    import pefile
except ImportError:
    import sys
    print("Missing dependencies. Run: pip install capstone pefile")
    sys.exit(1)

try:
    import keystone
    HAS_KEYSTONE = True
except ImportError:
    HAS_KEYSTONE = False






import sys



#THEMES -------------------------------------------------------------------

THEMES = {
    "DORFic": {
        "BG": "#fff7f0",
        "BG2": "#fff2e6",
        "BG3": "#ffe4cc",
        "GLASS": "#ffffff",
        "BORDER": "#ff9a3c",
        "BORDER_DARK": "#d96a00",
        "ACCENT": "#ff7a00",
        "ACCENT2": "#ffb347",
        "ACCENT3": "#ffd08a",
        "GREEN_GLOW": "#8dff8d",
        "CHROME": "#ffe0bf",
        "FG": "#4a2500",
        "FG_DIM": "#8a5a2b",
        "FG_LIGHT": "#ffffff",
        "HILIGHT": "#ffd8b0",
        "DIRTY_BG": "#fff1c2",
        "ERR_BG": "#ffd4d4",
        "SHADOW": "#cc8a4d",
    },

    "Glossy Aqua": {
        "BG": "#c9f8ff",
        "BG2": "#efffff",
        "BG3": "#8eeeff",
        "GLASS": "#ffffff",
        "BORDER": "#00cfff",
        "BORDER_DARK": "#008fb3",
        "ACCENT": "#009dff",
        "ACCENT2": "#00ffb7",
        "ACCENT3": "#6ffff0",
        "GREEN_GLOW": "#8dffcb",
        "CHROME": "#d7f8ff",
        "FG": "#003847",
        "FG_DIM": "#3c7f91",
        "FG_LIGHT": "#ffffff",
        "HILIGHT": "#b8f6ff",
        "DIRTY_BG": "#fff0a6",
        "ERR_BG": "#ffd1d1",
        "SHADOW": "#5fcfe6",
    },

    "Dark Frutiger": {
        "BG": "#0a1218",
        "BG2": "#10202b",
        "BG3": "#173444",
        "GLASS": "#20495c",
        "BORDER": "#00c8ff",
        "BORDER_DARK": "#006f91",
        "ACCENT": "#00bfff",
        "ACCENT2": "#00ffbf",
        "ACCENT3": "#6ae8ff",
        "GREEN_GLOW": "#6dffcb",
        "CHROME": "#355767",
        "FG": "#e8fbff",
        "FG_DIM": "#89c0cf",
        "FG_LIGHT": "#ffffff",
        "HILIGHT": "#29586d",
        "DIRTY_BG": "#6d5f1c",
        "ERR_BG": "#662727",
        "SHADOW": "#050b0f",
    },

    "Galaxy": {
        "BG": "#12001f",
        "BG2": "#1f0938",
        "BG3": "#31125e",
        "GLASS": "#44207a",
        "BORDER": "#9d5cff",
        "BORDER_DARK": "#5a24c4",
        "ACCENT": "#42d9ff",
        "ACCENT2": "#ff3de2",
        "ACCENT3": "#b18cff",
        "GREEN_GLOW": "#70ffe8",
        "CHROME": "#5b3f8c",
        "FG": "#f8efff",
        "FG_DIM": "#c8a8ea",
        "FG_LIGHT": "#ffffff",
        "HILIGHT": "#6344a1",
        "DIRTY_BG": "#8b5bcc",
        "ERR_BG": "#6b2146",
        "SHADOW": "#07020f",
    },

    "Y2K Girly": {
        "BG": "#ffe0f5",
        "BG2": "#fff2fb",
        "BG3": "#ffb5e3",
        "GLASS": "#ffffff",
        "BORDER": "#ff63c3",
        "BORDER_DARK": "#d43291",
        "ACCENT": "#ff2fb2",
        "ACCENT2": "#58d8ff",
        "ACCENT3": "#b56dff",
        "GREEN_GLOW": "#aafff0",
        "CHROME": "#ffd3ef",
        "FG": "#6a1457",
        "FG_DIM": "#b25a96",
        "FG_LIGHT": "#ffffff",
        "HILIGHT": "#ffc8ea",
        "DIRTY_BG": "#ffe49d",
        "ERR_BG": "#ffcad8",
        "SHADOW": "#d995bf",
    }
}

#Frutiger Aero Palette ----------------------------------------------------
# Sky blues, aqua greens, glassy whites, chrome accents

BG           = "#d6eaf8"        # sky-blue background
BG2          = "#eaf4fb"        # lighter panel
BG3          = "#b8d8f0"        # mid-tone blue panel
GLASS        = "#f0f8ff"        # glass-white
BORDER       = "#7ab8d9"        # chrome border
BORDER_DARK  = "#4a90b8"        # deeper border
ACCENT       = "#0077cc"        # vivid blue
ACCENT2      = "#00aa88"        # aqua-teal
ACCENT3      = "#2ec4b6"        # bright teal
GREEN_GLOW   = "#52d68a"        # nature green
CHROME       = "#c8dfe8"        # chrome silver
FG           = "#1a3a4a"        # dark navy text
FG_DIM       = "#6a9ab0"        # dimmed text
FG_LIGHT     = "#ffffff"        # white text on dark buttons
HILIGHT      = "#cce8ff"        # selection highlight
DIRTY_BG     = "#fff3cd"        # amber tint for edited lines
ERR_BG       = "#fce4e4"        # soft red for errors
SHADOW       = "#8ab0c8"        # shadow tone

FONT_MONO    = ("Consolas", 10)
FONT_UI      = ("Segoe UI", 9)
FONT_UI_B    = ("Segoe UI", 9, "bold")
FONT_TITLE   = ("Segoe UI", 11, "bold")
FONT_LOGO    = ("Segoe UI", 18, "bold")

COLS = 16


#Gradient / Gloss helpers -------------------------------------------------

def draw_gloss_rect(canvas, x1, y1, x2, y2, color_top, color_bot,
                    radius=8, outline=None):
    """Draw a rounded glossy rectangle on a Canvas."""
    r = radius
    # Background fill (approx with polygon)
    canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90,
                      fill=color_top, outline="")
    canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90,
                      fill=color_top, outline="")
    canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90,
                      fill=color_bot, outline="")
    canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90,
                      fill=color_bot, outline="")
    canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=color_top, outline="")
    canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=color_top, outline="")
    mid = (y1+y2)//2
    canvas.create_rectangle(x1+r, mid, x2-r, y2-r, fill=color_bot, outline="")
    if outline:
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90,
                          style="arc", outline=outline)
        canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90,
                          style="arc", outline=outline)
        canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90,
                          style="arc", outline=outline)
        canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90,
                          style="arc", outline=outline)


#GlossButton -------------------------------------------------------------

class GlossButton(tk.Canvas):
    """A glossy Frutiger Aero-style button drawn on canvas."""

    def __init__(self, parent, text, command=None, color=ACCENT,
                 text_color=FG_LIGHT, width=110, height=28,
                 disabled_color=CHROME, **kwargs):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bd=0,
                         cursor="hand2", **kwargs)
        self._text      = text
        self._cmd       = command
        self._color     = color
        self._dis_color = disabled_color
        self._txt_color = text_color
        self._enabled   = True
        self._hover     = False
        self._btn_width  = width
        self._btn_height = height
        self._draw()
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)
        self.bind("<Button-1>", self._on_click)




    def _on_enter(self, e):
        if self._enabled:
            self._hover = True; self._draw()

    def _on_leave(self, e):
        self._hover = False; self._draw()

    def _on_click(self, e):
        if self._enabled and self._cmd:
            self._cmd()

    def configure(self, **kw):
        if "state" in kw:
            self._enabled = (kw.pop("state") == "normal")
            self._draw()
        super().configure(**kw)

    def __setitem__(self, key, val):
        self.configure(**{key: val})

    def _draw(self):
        self.delete("all")
        w, h = self._btn_width, self._btn_height
        r = 6
        base  = self._color if self._enabled else self._dis_color
        if self._hover and self._enabled:
            # Lighten on hover
            top = self._lighten(base, 0.25)
            bot = base
        else:
            top = self._lighten(base, 0.15)
            bot = self._darken(base, 0.12)

        # Shadow
        self.create_rounded_rect(2, 2, w-1, h-1, r, fill=SHADOW, outline="")
        # Body gradient (top half lighter, bottom darker)
        self.create_rounded_rect(1, 1, w-2, h-2, r, fill=bot, outline="")
        self.create_rounded_rect(1, 1, w-2, h//2, r, fill=top, outline="")
        # Gloss highlight strip
        self.create_rounded_rect(3, 2, w-4, h//3, r-2,
                                 fill=self._lighten(top, 0.4), outline="")
        # Border
        border_c = self._darken(base, 0.25)
        self.create_rounded_rect(1, 1, w-2, h-2, r,
                                 fill="", outline=border_c)
        # Text
        state_color = self._txt_color if self._enabled else FG_DIM
        self.create_text(w//2, h//2, text=self._text,
                         font=FONT_UI_B, fill=state_color)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [
            x1+r, y1,  x2-r, y1,
            x2,   y1,  x2,   y1+r,
            x2,   y2-r, x2,  y2,
            x2-r, y2,  x1+r, y2,
            x1,   y2,  x1,   y2-r,
            x1,   y1+r, x1,  y1,
            x1+r, y1,
        ]
        return self.create_polygon(pts, smooth=True, **kw)

    @staticmethod
    def _lighten(hex_color, factor=0.2):
        r, g, b = int(hex_color[1:3],16), int(hex_color[3:5],16), int(hex_color[5:7],16)
        r = min(255, int(r + (255-r)*factor))
        g = min(255, int(g + (255-g)*factor))
        b = min(255, int(b + (255-b)*factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def _darken(hex_color, factor=0.15):
        r, g, b = int(hex_color[1:3],16), int(hex_color[3:5],16), int(hex_color[5:7],16)
        r = max(0, int(r * (1-factor)))
        g = max(0, int(g * (1-factor)))
        b = max(0, int(b * (1-factor)))
        return f"#{r:02x}{g:02x}{b:02x}"


#Architecture helpers -----------------------------------------------------

def get_architecture(pe):
    machine = pe.FILE_HEADER.Machine
    arch_map = {
        0x014c: (capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32),  "x86 32-bit",  32),
        0x8664: (capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64),  "x86 64-bit",  64),
        0xAA64: (capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM), "ARM64",      64),
        0x01c0: (capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM),  "ARM 32-bit",  32),
    }
    if machine not in arch_map:
        raise ValueError(f"Unsupported architecture: 0x{machine:04X}")
    md, label, bits = arch_map[machine]
    md.detail = True
    return md, label, bits


def extract_strings(data, min_len=5):
    results, current, start = [], [], 0
    for i, byte in enumerate(data):
        if 0x20 <= byte <= 0x7E:
            if not current:
                start = i
            current.append(chr(byte))
        else:
            if len(current) >= min_len:
                results.append((start, "".join(current)))
            current = []
    if len(current) >= min_len:
        results.append((start, "".join(current)))
    return results


#Simple x86 assembler ------------------------------------------------------

def simple_assemble(mnem, ops, original_size, bits=64):
    mnem = mnem.strip().lower()
    ops  = ops.strip()

    trivial = {
        "nop": b"\x90", "ret": b"\xc3", "retn": b"\xc3",
        "retf": b"\xcb", "hlt": b"\xf4", "int3": b"\xcc",
        "pushf": b"\x9c", "popf": b"\x9d",
        "cld": b"\xfc", "std": b"\xfd", "sti": b"\xfb", "cli": b"\xfa",
    }
    if mnem in trivial and not ops:
        return _pad(trivial[mnem], original_size), None

    if mnem in ("ret", "retn") and ops:
        try:
            n = int(ops, 0)
            raw = b"\xc2" + struct.pack("<H", n & 0xFFFF)
            return _pad(raw, original_size), None
        except ValueError:
            pass

    if mnem == "int" and ops:
        try:
            n = int(ops, 0)
            if n == 3:
                return _pad(b"\xcc", original_size), None
            return _pad(b"\xcd" + bytes([n & 0xFF]), original_size), None
        except ValueError:
            pass

    if mnem == "jmp" and ops.startswith("$"):
        try:
            delta = int(ops[1:], 0)
            rel   = delta - 2
            if -128 <= rel <= 127:
                return _pad(b"\xeb" + struct.pack("b", rel), original_size), None
        except ValueError:
            pass

    reg32 = {"eax":0,"ecx":1,"edx":2,"ebx":3,"esp":4,"ebp":5,"esi":6,"edi":7}
    reg64 = {"rax":0,"rcx":1,"rdx":2,"rbx":3,"rsp":4,"rbp":5,"rsi":6,"rdi":7,
             "r8":8,"r9":9,"r10":10,"r11":11,"r12":12,"r13":13,"r14":14,"r15":15}

    if mnem == "xor" and "," in ops:
        a, b_ = [x.strip().lower() for x in ops.split(",", 1)]
        if a == b_:
            if a in reg32:
                r = reg32[a]
                return _pad(bytes([0x31, 0xC0 | (r << 3) | r]), original_size), None
            if a in reg64:
                r = reg64[a]; rex = 0x4D if r >= 8 else 0x48; r &= 7
                return _pad(bytes([rex, 0x31, 0xC0 | (r << 3) | r]), original_size), None

    if mnem == "mov" and "," in ops:
        a, b_ = [x.strip().lower() for x in ops.split(",", 1)]
        try:
            imm = int(b_, 0)
            if a in reg32:
                r = reg32[a]
                return _pad(bytes([0xB8 + r]) + struct.pack("<I", imm & 0xFFFFFFFF), original_size), None
            if a in reg64 and 0 <= imm <= 0xFFFFFFFF:
                r = reg64[a] & 7
                return _pad(bytes([0xB8 + r]) + struct.pack("<I", imm), original_size), None
        except ValueError:
            pass

    if mnem == "push" and ops:
        try:
            imm = int(ops, 0)
            if -128 <= imm <= 127:
                raw = b"\x6a" + struct.pack("b", imm)
            else:
                raw = b"\x68" + struct.pack("<i", imm)
            return _pad(raw, original_size), None
        except ValueError:
            pass

    if HAS_KEYSTONE:
        try:
            ks_mode = keystone.KS_MODE_64 if bits == 64 else keystone.KS_MODE_32
            ks = keystone.Ks(keystone.KS_ARCH_X86, ks_mode)
            insn_str = f"{mnem} {ops}".strip()
            encoded, _ = ks.asm(insn_str)
            raw = bytes(encoded)
            if len(raw) <= original_size:
                return _pad(raw, original_size), None
            else:
                return None, f"Encoded {len(raw)} bytes but slot is only {original_size} bytes"
        except Exception as e:
            return None, str(e)

    return None, (
        f"Cannot assemble '{mnem} {ops}' without keystone.\n"
        "Supported: nop, ret, int3, hlt, xor r,r, mov r,imm, push imm"
    )


def _pad(raw, size):
    if len(raw) < size:
        raw = raw + b"\x90" * (size - len(raw))
    return raw[:size]


#Widget helpers ------------------------------------------------------------

def write_text(widget, content, clear=True):
    widget.configure(state="normal")
    if clear:
        widget.delete("1.0", "end")
    widget.insert("end", content)
    widget.configure(state="disabled")


def make_scrolled_text(parent, editable=False, bg=BG2, **kwargs):
    frame = tk.Frame(parent, bg=bg, bd=1, relief="solid",
                     highlightbackground=BORDER, highlightthickness=1)
    t = tk.Text(
        frame, bg=GLASS, fg=FG, insertbackground=ACCENT,
        font=FONT_MONO, relief="flat", bd=0,
        selectbackground=HILIGHT, selectforeground=FG,
        wrap="none", undo=True, padx=6, pady=4, **kwargs
    )
    sx = tk.Scrollbar(frame, orient="horizontal", command=t.xview,
                      bg=CHROME, troughcolor=BG2, relief="flat",
                      highlightthickness=0)
    sy = tk.Scrollbar(frame, command=t.yview,
                      bg=CHROME, troughcolor=BG2, relief="flat",
                      highlightthickness=0)
    t.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)
    sy.pack(side="right", fill="y")
    sx.pack(side="bottom", fill="x")
    t.pack(fill="both", expand=True)
    if not editable:
        t.configure(state="disabled")
    frame.text = t
    return frame


#Glass Panel label helper --------------------------------------------------

def glass_label(parent, text, bg=BG3):
    """A section header label with a separator line."""
    f = tk.Frame(parent, bg=bg, pady=2)
    f.pack(fill="x", padx=6, pady=(8, 2))
    tk.Label(f, text=text, font=FONT_UI_B, bg=bg, fg=ACCENT,
             padx=4).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x",
                                           expand=True, padx=(4, 0))


#ROM Space meter -----------------------------------------------------------

class RomMeter(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG3, **kwargs)
        self.lbl = tk.Label(self, text="", font=FONT_UI, bg=BG3, fg=FG_DIM)
        self.lbl.pack(side="left", padx=8)
        self.canvas = tk.Canvas(self, bg=BG3, highlightthickness=0,
                                height=14, width=180)
        self.canvas.pack(side="left", padx=(0, 8), pady=4)

    def update(self, used, total):
        ratio = used / total if total else 0
        pct   = ratio * 100
        if ratio > 0.9:
            bar_color = "#e74c3c"
        elif ratio > 0.7:
            bar_color = "#f39c12"
        else:
            bar_color = ACCENT2
        self.lbl.config(text=f"ROM  {used:,} / {total:,} bytes  ({pct:.1f}%)")
        w = self.canvas.winfo_width() or 180
        h = 14
        r = 5
        self.canvas.delete("all")
        # Track
        self._rounded(0, 2, w, h-2, r, CHROME)
        # Fill
        fw = max(0, int((w-2) * ratio))
        if fw > 1:
            self._rounded(1, 3, fw, h-3, r, bar_color)
        # Gloss
        self._rounded(2, 3, fw-2 if fw > 4 else fw, (h)//2-1, r-1,
                      "#ffffff" if fw > 4 else "")

    def _rounded(self, x1, y1, x2, y2, r, color):
        if not color or x2 <= x1: return
        c = self.canvas
        c.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, fill=color, outline="")
        c.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, fill=color, outline="")
        c.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, fill=color, outline="")
        c.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, fill=color, outline="")
        c.create_rectangle(x1+r, y1, x2-r, y2, fill=color, outline="")
        c.create_rectangle(x1, y1+r, x2, y2-r, fill=color, outline="")


#Search Bar ----------------------------------------------------------------

class SearchBar(tk.Frame):
    def __init__(self, parent, target=None, keep_state=False, **kwargs):
        super().__init__(parent, bg=BG3, pady=4, **kwargs)
        self.configure(bd=0, relief="flat",
                       highlightbackground=BORDER, highlightthickness=1)
        self.target     = target
        self.keep_state = keep_state
        self._matches   = []
        self._current   = -1

        tk.Label(self, text="🔍 Find:", font=FONT_UI_B, bg=BG3, fg=FG,
                 padx=4).pack(side="left", padx=(8, 2))
        self.var = tk.StringVar()
        self.var.trace_add("write", lambda *_: self._search())
        self.entry = tk.Entry(self, textvariable=self.var, font=FONT_MONO,
                              bg=GLASS, fg=FG, relief="solid",
                              bd=1, highlightthickness=1,
                              highlightbackground=BORDER,
                              highlightcolor=ACCENT,
                              insertbackground=ACCENT, width=24)
        self.entry.pack(side="left", ipady=3, padx=4)
        self.entry.bind("<Return>",       lambda e: self._next())
        self.entry.bind("<Shift-Return>", lambda e: self._prev())
        self.entry.bind("<Escape>",       lambda e: self.hide())

        for text, cmd in [("▲", self._prev), ("▼", self._next)]:
            GlossButton(self, text, command=cmd, color=ACCENT2,
                        width=30, height=24
                        ).pack(side="left", padx=2, pady=2)

        self.count_lbl = tk.Label(self, text="", font=FONT_UI, bg=BG3, fg=FG_DIM)
        self.count_lbl.pack(side="left", padx=8)
        GlossButton(self, "✕ Close", command=self.hide, color="#c0392b",
                    width=70, height=24).pack(side="right", padx=8, pady=2)

        if target:
            self._init_tags()

    def _init_tags(self):
        self.target.tag_configure("_hi",   background=HILIGHT,  foreground=FG)
        self.target.tag_configure("_curr", background=ACCENT,   foreground=FG_LIGHT)

    def set_target(self, w, keep_state=False):
        self.target = w; self.keep_state = keep_state; self._init_tags()

    def show(self):
        self.pack(fill="x")
        self.entry.focus_set()
        self.entry.select_range(0, "end")
        self._search()

    def hide(self):
        self._clear(); self.pack_forget()
        if self.target: self.target.focus_set()

    def _restore(self):
        if not self.keep_state:
            self.target.configure(state="disabled")

    def _search(self):
        self._clear()
        q = self.var.get()
        if not q or not self.target:
            self.count_lbl.config(text=""); return
        content = self.target.get("1.0", "end")
        ql, cl  = q.lower(), content.lower()
        self._matches, s = [], 0
        while True:
            i = cl.find(ql, s)
            if i == -1: break
            self._matches.append(i); s = i + 1
        self.target.configure(state="normal")
        for i in self._matches:
            line = content[:i].count("\n") + 1
            col  = i - content[:i].rfind("\n") - 1
            self.target.tag_add("_hi", f"{line}.{col}", f"{line}.{col+len(q)}")
        self._restore()
        if self._matches:
            self._current = 0; self._jump()
            self.count_lbl.config(text=f"1 / {len(self._matches)}")
        else:
            self._current = -1
            self.count_lbl.config(text="no results")

    def _clear(self):
        if not self.target: return
        self.target.configure(state="normal")
        self.target.tag_remove("_hi",   "1.0", "end")
        self.target.tag_remove("_curr", "1.0", "end")
        self._restore()

    def _jump(self):
        if not self._matches or self._current < 0: return
        q       = self.var.get()
        content = self.target.get("1.0", "end")
        i       = self._matches[self._current]
        line    = content[:i].count("\n") + 1
        col     = i - content[:i].rfind("\n") - 1
        self.target.configure(state="normal")
        self.target.tag_remove("_curr", "1.0", "end")
        self.target.tag_add("_curr", f"{line}.{col}", f"{line}.{col+len(q)}")
        self.target.see(f"{line}.{col}")
        self._restore()
        self.count_lbl.config(text=f"{self._current+1} / {len(self._matches)}")

    def _next(self):
        if not self._matches: return
        self._current = (self._current + 1) % len(self._matches); self._jump()

    def _prev(self):
        if not self._matches: return
        self._current = (self._current - 1) % len(self._matches); self._jump()


#Patch Dialog --------------------------------------------------------------

class PatchDialog(tk.Toplevel):
    def __init__(self, parent, raw_data, on_patched):
        super().__init__(parent)
        self.title("NEONFLUX — Patch Bytes")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self.raw        = bytearray(raw_data)
        self.on_patched = on_patched

        # Header
        hdr = tk.Frame(self, bg=BG3, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="  🔧  PATCH BYTES",
                 font=FONT_TITLE, bg=BG3, fg=ACCENT
                 ).pack(side="left", padx=14)

        body = tk.Frame(self, bg=BG, padx=20, pady=16)
        body.pack(fill="both", expand=True)

        for row, (lbl, attr) in enumerate([
            ("File Offset (hex):", "off_var"),
            ("New Bytes (hex):",   "bytes_var"),
        ]):
            tk.Label(body, text=lbl, font=FONT_UI_B, bg=BG, fg=FG
                     ).grid(row=row*2, column=0, sticky="w", pady=(8,2))
            var = tk.StringVar(); setattr(self, attr, var)
            e = tk.Entry(body, textvariable=var, font=FONT_MONO,
                         bg=GLASS, fg=FG, relief="solid", bd=1,
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=ACCENT,
                         insertbackground=ACCENT, width=38)
            e.grid(row=row*2+1, column=0, sticky="ew", ipady=4)
            if row == 0: e.focus_set()

        tk.Label(body, text="e.g.  offset: 1A2B    bytes: 90 90 90",
                 font=FONT_UI, bg=BG, fg=FG_DIM
                 ).grid(row=4, column=0, sticky="w", pady=(4, 8))

        # Preview box
        preview_f = tk.Frame(body, bg=GLASS, bd=1, relief="solid",
                             highlightthickness=1, highlightbackground=BORDER)
        preview_f.grid(row=5, column=0, sticky="ew", pady=4)
        self.preview = tk.Text(preview_f, font=FONT_MONO, bg=GLASS, fg=FG,
                               relief="flat", bd=0, height=4,
                               state="disabled", padx=8, pady=6)
        self.preview.pack(fill="both")

        self.off_var.trace_add("write",   lambda *_: self._update())
        self.bytes_var.trace_add("write", lambda *_: self._update())

        bf = tk.Frame(self, bg=BG, pady=14)
        bf.pack()
        GlossButton(bf, "✓  Apply", command=self._apply,
                    color=ACCENT2, width=100, height=32
                    ).pack(side="left", padx=8)
        GlossButton(bf, "✕  Cancel", command=self.destroy,
                    color="#c0392b", width=100, height=32
                    ).pack(side="left", padx=8)

    def _parse(self):
        try:
            off = int(self.off_var.get().strip().lstrip("0x").lstrip("0X") or "0", 16)
        except ValueError:
            off = None
        try:
            toks = self.bytes_var.get().strip().split()
            new  = bytes(int(t, 16) for t in toks) if toks else None
        except ValueError:
            new = None
        return off, new

    def _update(self):
        off, new = self._parse()
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        if off is not None and new and 0 <= off < len(self.raw):
            end   = min(off + len(new), len(self.raw))
            old_b = self.raw[off:end]
            self.preview.insert("end",
                f"  Offset : 0x{off:08X}\n"
                f"  Before : {' '.join(f'{b:02x}' for b in old_b)}\n"
                f"  After  : {' '.join(f'{b:02x}' for b in new)}\n")
        else:
            self.preview.insert("end", "  (enter a valid offset and bytes)")
        self.preview.configure(state="disabled")

    def _apply(self):
        off, new = self._parse()
        if off is None:
            messagebox.showerror("Error", "Invalid offset.", parent=self); return
        if not new:
            messagebox.showerror("Error", "Invalid bytes.", parent=self); return
        if off + len(new) > len(self.raw):
            messagebox.showerror("Error", "Patch extends past file end.", parent=self); return
        for i, b in enumerate(new):
            self.raw[off + i] = b
        self.on_patched(bytes(self.raw))
        self.destroy()


#ttk Styles ----------------------------------------------------------------

def configure_ttk_styles():
    s = ttk.Style()
    s.theme_use("default")

    # Notebook
    s.configure("N.TNotebook",
                background=BG, borderwidth=0)
    s.configure("N.TNotebook.Tab",
                background=BG3, foreground=FG_DIM,
                font=FONT_UI_B, padding=[16, 8],
                borderwidth=0, relief="flat")
    s.map("N.TNotebook.Tab",
          background=[("selected", GLASS), ("active", CHROME)],
          foreground=[("selected", ACCENT), ("active", FG)])

    # Progressbar
    s.configure("P.Horizontal.TProgressbar",
                troughcolor=CHROME, background=ACCENT2,
                borderwidth=0, lightcolor=ACCENT2,
                darkcolor=ACCENT)

    # Combobox
    s.configure("TCombobox",
                fieldbackground=GLASS, background=CHROME,
                foreground=FG, arrowcolor=ACCENT,
                bordercolor=BORDER, lightcolor=BORDER,
                darkcolor=BORDER)
    s.map("TCombobox",
          fieldbackground=[("readonly", GLASS)],
          foreground=[("readonly", FG)])




def apply_theme(theme_name):
    global BG, BG2, BG3, GLASS
    global BORDER, BORDER_DARK
    global ACCENT, ACCENT2, ACCENT3
    global GREEN_GLOW, CHROME
    global FG, FG_DIM, FG_LIGHT
    global HILIGHT, DIRTY_BG, ERR_BG, SHADOW

    theme = THEMES[theme_name]

    BG           = theme["BG"]
    BG2          = theme["BG2"]
    BG3          = theme["BG3"]
    GLASS        = theme["GLASS"]
    BORDER       = theme["BORDER"]
    BORDER_DARK  = theme["BORDER_DARK"]
    ACCENT       = theme["ACCENT"]
    ACCENT2      = theme["ACCENT2"]
    ACCENT3      = theme["ACCENT3"]
    GREEN_GLOW   = theme["GREEN_GLOW"]
    CHROME       = theme["CHROME"]
    FG           = theme["FG"]
    FG_DIM       = theme["FG_DIM"]
    FG_LIGHT     = theme["FG_LIGHT"]
    HILIGHT      = theme["HILIGHT"]
    DIRTY_BG     = theme["DIRTY_BG"]
    ERR_BG       = theme["ERR_BG"]
    SHADOW       = theme["SHADOW"]

    configure_ttk_styles()

#Main Application ----------------------------------------------------------

class DisassemblerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(resource_path("icon.ico"))
        self.title("NEONFLUX — Binary Disassembler & Viewer")
        self.configure(bg=BG)
        self.geometry("1440x920")
        self.minsize(1024, 680)

        configure_ttk_styles()

        self.filepath     = None
        self.pe           = None
        self.raw_data     = b""
        self.modified     = False
        self._all_strings = []
        self._asm_meta    = []
        self._arch_bits   = 64

        self._build_menu()
        self._build_topbar()
        self._build_main()
        self._build_statusbar()
        self._bind_keys()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _change_theme(self, theme_name):
     apply_theme(theme_name)

     self.configure(bg=BG)

     def recolor(widget):
        try:
            cls = widget.winfo_class()

            if cls in ("Frame", "LabelFrame", "PanedWindow"):
                widget.configure(bg=BG)

            elif cls == "Label":
                widget.configure(bg=BG, fg=FG)

            elif cls == "Text":
                widget.configure(
                    bg=GLASS,
                    fg=FG,
                    insertbackground=ACCENT,
                    selectbackground=HILIGHT
                )

            elif cls == "Listbox":
                widget.configure(
                    bg=GLASS,
                    fg=FG,
                    selectbackground=HILIGHT,
                    selectforeground=FG
                )

            elif cls == "Entry":
                widget.configure(
                    bg=GLASS,
                    fg=FG,
                    insertbackground=ACCENT
                )

            elif cls == "Canvas":
                widget.configure(bg=BG3)

        except:
            pass

        for child in widget.winfo_children():
            recolor(child)

     recolor(self)

     self._setup_asm_tags()
     self._setup_hex_tags()

     self._set_status(f"Theme changed to {theme_name}")
     
    #Menu -----------------------------------------------------------------

    def _build_menu(self):
        def _menu(parent, label, items):
            m = tk.Menu(parent, bg=GLASS, fg=FG, activebackground=HILIGHT,
                        activeforeground=ACCENT, relief="flat", tearoff=False,
                        font=FONT_UI, bd=1)
            parent.add_cascade(label=label, menu=m)
            for it in items:
                if it == "---": m.add_separator()
                else: m.add_command(label=it[0], command=it[1])
        mb = tk.Menu(self, bg=GLASS, fg=FG, activebackground=HILIGHT,
                     activeforeground=ACCENT, relief="flat", tearoff=False,
                     font=FONT_UI)
        self.config(menu=mb)
        _menu(mb, "File", [
            ("Open…           Ctrl+O",       self._open_file),
            "---",
            ("Save            Ctrl+S",        self._save),
            ("Save As…        Ctrl+Shift+S",  self._save_as),
            "---",
            ("Quit            Ctrl+Q",        self._on_close),
        ])
        _menu(mb, "Edit", [
            ("Patch Bytes…    Ctrl+P",        self._open_patch),
            ("Go to Address…  Ctrl+G",        self._goto_address),
            ("Apply ASM Edits Ctrl+E",        self._apply_asm_edits),
            ("Apply Hex Edits Ctrl+Return",   self._apply_hex_edits),
        ])
        _menu(mb, "Search", [
            ("Search Strings  Ctrl+F", self._focus_string_search),
            ("Search Disasm   Ctrl+D", self._focus_asm_search),
            ("Search Hex      Ctrl+H", self._focus_hex_search),
        ])
        # VIEW MENU
        view_menu = tk.Menu(
            mb,
            bg=GLASS,
            fg=FG,
            activebackground=HILIGHT,
            activeforeground=ACCENT,
            relief="flat",
            tearoff=False,
            font=FONT_UI
        )

        mb.add_cascade(label="View", menu=view_menu)

        view_menu.add_command(
            label="Re-analyze      F5",
            command=self._run_analysis
        )

        view_menu.add_separator()

        theme_menu = tk.Menu(
            view_menu,
            bg=GLASS,
            fg=FG,
            activebackground=HILIGHT,
            activeforeground=ACCENT,
            relief="flat",
            tearoff=False,
            font=FONT_UI
        )

        view_menu.add_cascade(label="Themes", menu=theme_menu)

        theme_menu.add_command(
            label=" DORFic",
            command=lambda: self._change_theme("DORFic")
        )

        theme_menu.add_command(
            label=" Glossy Aqua",
            command=lambda: self._change_theme("Glossy Aqua")
        )

        theme_menu.add_command(
            label=" Dark Frutiger",
            command=lambda: self._change_theme("Dark Frutiger")
        )

        theme_menu.add_command(
            label=" Galaxy",
            command=lambda: self._change_theme("Galaxy")
        )

        theme_menu.add_command(
            label=" Y2K Girly",
            command=lambda: self._change_theme("Y2K Girly")
        )
        
        _menu(mb, "About", [
            ("About NEONFLUX", self._show_about_tab),
        ])

    #Top Bar ---------------------------------------------------------------

    def _build_topbar(self):
        # Outer container with gradient-like effect via layered frames
        bar_outer = tk.Frame(self, bg=BG3)
        bar_outer.pack(fill="x", side="top")
        bar_inner = tk.Frame(bar_outer, bg=BG3, height=58)
        bar_inner.pack(fill="x")
        bar_inner.pack_propagate(False)

        # Bottom border line
        tk.Frame(bar_outer, bg=BORDER, height=2).pack(fill="x")

        # Logo section
        logo_f = tk.Frame(bar_inner, bg=BG3)
        logo_f.pack(side="left", padx=16, pady=6)

        logo_canvas = tk.Canvas(logo_f, bg=BG3, width=180, height=44,
                                highlightthickness=0)
        logo_canvas.pack()

        # Draw a little glassy logo badge
        logo_canvas.create_rectangle(0, 4, 176, 42, fill=ACCENT,
                                     outline=BORDER_DARK)
        logo_canvas.create_rectangle(2, 5, 174, 22, fill="#2a9fd8",
                                     outline="")  # gloss top
        logo_canvas.create_text(88, 23, text="✦ NEONFLUX",
                                font=("Segoe UI", 12, "bold"),
                                fill=FG_LIGHT)

        tk.Label(bar_inner, text="Binary Disassembler & Editor",
                 font=FONT_UI, bg=BG3, fg=FG_DIM
                 ).pack(side="left", padx=4)

        # Right-side buttons
        right_f = tk.Frame(bar_inner, bg=BG3)
        right_f.pack(side="right", padx=10, pady=8)

        GlossButton(right_f, "📂 Open", command=self._open_file,
                    color=ACCENT, width=90, height=36
                    ).pack(side="left", padx=4)

        def _gbtn(text, color, cmd, attr, w=88):
            b = GlossButton(right_f, text, command=cmd,
                            color=color, width=w, height=36)
            b.pack(side="left", padx=3)
            b["state"] = "disabled"
            setattr(self, attr, b)

        _gbtn("💾 Save",      ACCENT2,   self._save,            "btn_save",    80)
        _gbtn("Save As",      ACCENT2,   self._save_as,         "btn_saveas",  76)
        _gbtn("🔧 Patch",     "#e67e22",  self._open_patch,      "btn_patch",   80)
        _gbtn("📍 GoTo",      "#8e44ad",  self._goto_address,    "btn_goto",    72)
        _gbtn("▶ ASM",        "#27ae60",  self._apply_asm_edits, "btn_apply_asm", 68)
        _gbtn("▶ Hex",        "#27ae60",  self._apply_hex_edits, "btn_apply_hex", 68)
        _gbtn("⟳ Analyze",   FG_DIM,    self._run_analysis,    "btn_analyze", 80)

        # Section + Limit controls
        ctrl_f = tk.Frame(bar_inner, bg=BG3)
        ctrl_f.pack(side="right", padx=(0, 6), pady=10)

        tk.Label(ctrl_f, text="Limit:", font=FONT_UI, bg=BG3, fg=FG_DIM
                 ).grid(row=0, column=0, padx=(0, 2))
        self.limit_var = tk.StringVar(value="500")
        tk.Entry(ctrl_f, textvariable=self.limit_var, width=6,
                 font=FONT_UI, bg=GLASS, fg=FG, relief="solid", bd=1,
                 highlightthickness=1, highlightbackground=BORDER,
                 insertbackground=ACCENT
                 ).grid(row=0, column=1, ipady=3, padx=(0, 8))

        tk.Label(ctrl_f, text="Section:", font=FONT_UI, bg=BG3, fg=FG_DIM
                 ).grid(row=0, column=2, padx=(0, 2))
        self.section_var  = tk.StringVar(value="all")
        self.section_menu = ttk.Combobox(ctrl_f, textvariable=self.section_var,
                                          state="disabled", width=10,
                                          font=FONT_UI)
        self.section_menu.grid(row=0, column=3, ipady=3)

    #Main Layout -----------------------------------------------------------

    def _build_main(self):
        pane = tk.PanedWindow(self, orient="horizontal", bg=BG,
                              sashwidth=6, sashrelief="raised",
                              sashpad=2, bd=0)
        pane.pack(fill="both", expand=True)

        #Left panel -------------------------------------------------------
        left = tk.Frame(pane, bg=BG, width=320)
        pane.add(left, minsize=220)

        glass_label(left, "📋  PE INFORMATION", BG)
        self.pe_frame = make_scrolled_text(left, height=10)
        self.pe_frame.pack(fill="x", padx=8, pady=(0, 6))

        glass_label(left, "📁  SECTIONS", BG)
        list_f = tk.Frame(left, bg=GLASS, bd=1, relief="solid",
                          highlightthickness=1, highlightbackground=BORDER)
        list_f.pack(fill="x", padx=8, pady=(0, 6))
        self.sec_list = tk.Listbox(list_f, bg=GLASS, fg=FG, font=FONT_MONO,
                                    relief="flat", bd=0, height=6,
                                    selectbackground=HILIGHT,
                                    selectforeground=ACCENT,
                                    activestyle="underline")
        self.sec_list.pack(fill="x")
        self.sec_list.bind("<<ListboxSelect>>", self._on_section_select)

        # Strings
        glass_label(left, "🔤  STRINGS", BG)
        sf = tk.Frame(left, bg=BG)
        sf.pack(fill="x", padx=8, pady=(0, 4))
        tk.Label(sf, text="Filter:", font=FONT_UI, bg=BG, fg=FG_DIM
                 ).pack(side="left")
        self.str_filter_var = tk.StringVar()
        self.str_filter_var.trace_add("write", lambda *_: self._filter_strings())
        fentry = tk.Entry(sf, textvariable=self.str_filter_var,
                          font=FONT_MONO, bg=GLASS, fg=FG, relief="solid",
                          bd=1, highlightthickness=1,
                          highlightbackground=BORDER,
                          highlightcolor=ACCENT,
                          insertbackground=ACCENT, width=18)
        fentry.pack(side="left", padx=(4, 0), ipady=3)

        self.str_frame = make_scrolled_text(left)
        self.str_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        #Right: Notebook ---------------------------------------------------
        right = tk.Frame(pane, bg=BG)
        pane.add(right, minsize=620)

        self.nb = ttk.Notebook(right, style="N.TNotebook")
        self.nb.pack(fill="both", expand=True, padx=6, pady=6)

        #Tab 0: Disassembly ------------------------------------------------
        asm_outer = tk.Frame(self.nb, bg=BG2)
        self.nb.add(asm_outer, text="  ⚙  DISASSEMBLY  ")

        asm_info = tk.Frame(asm_outer, bg=BG3, pady=4)
        asm_info.pack(fill="x")
        tk.Label(asm_info,
                 text="  ✏  Edit mnemonic / operands  ·  Ctrl+E to assemble  ·  NOP-padding fills unchanged size",
                 font=FONT_UI, bg=BG3, fg=FG_DIM, anchor="w"
                 ).pack(side="left", padx=6)
        self.asm_dirty_lbl = tk.Label(asm_info, text="", font=FONT_UI_B,
                                       bg=BG3, fg="#e67e22")
        self.asm_dirty_lbl.pack(side="right", padx=12)

        self.asm_search = SearchBar(asm_outer, None, keep_state=True)
        self.asm_text_frame = make_scrolled_text(asm_outer, editable=True)
        self.asm_text_frame.pack(fill="both", expand=True)
        self.asm_text = self.asm_text_frame.text
        self.asm_search.set_target(self.asm_text, keep_state=True)
        self._setup_asm_tags()
        self.asm_text.bind("<KeyRelease>", self._asm_on_key)

        #Tab 1: Hex Editor -------------------------------------------------
        hex_outer = tk.Frame(self.nb, bg=BG2)
        self.nb.add(hex_outer, text="  🔢  HEX VIEWER  ")

        hex_info = tk.Frame(hex_outer, bg=BG3, pady=4)
        hex_info.pack(fill="x")
        tk.Label(hex_info,
                 text=f"  ✏  Edit hex bytes  ·  {COLS} bytes/row  ·  ASCII on right  ·  Ctrl+Return to apply",
                 font=FONT_UI, bg=BG3, fg=FG_DIM, anchor="w"
                 ).pack(side="left", padx=6)
        self.rom_meter = RomMeter(hex_info)
        self.rom_meter.pack(side="right", padx=8)

        self.hex_search = SearchBar(hex_outer, None, keep_state=True)
        self.hex_text_frame = make_scrolled_text(hex_outer, editable=True)
        self.hex_text_frame.pack(fill="both", expand=True)
        self.hex_text = self.hex_text_frame.text
        self.hex_search.set_target(self.hex_text, keep_state=True)
        self._setup_hex_tags()
        self.hex_text.bind("<KeyRelease>", self._hex_on_key)

        #Tab 2: About ------------------------------------------------------
        self._build_about_tab()

    #About Tab ------------------------------------------------------------

    def _build_about_tab(self):
        about_outer = tk.Frame(self.nb, bg=BG)
        self.nb.add(about_outer, text="  ℹ  ABOUT  ")

        canvas = tk.Canvas(about_outer, bg=BG, highlightthickness=0)
        scroll = tk.Scrollbar(about_outer, command=canvas.yview,
                               bg=CHROME, troughcolor=BG, relief="flat")
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # Logo hero
        hero = tk.Frame(inner, bg=ACCENT, pady=24)
        hero.pack(fill="x")
        tk.Label(hero, text="✦ NEONFLUX",
                 font=("Segoe UI", 28, "bold"), bg=ACCENT, fg=FG_LIGHT
                 ).pack()
        tk.Label(hero, text="Binary Disassembler & Editor  ·  Frutiger Aero Edition",
                 font=("Segoe UI", 11), bg=ACCENT, fg="#c8e8ff"
                 ).pack(pady=(2, 0))
        tk.Label(hero, text="Version 4.0  ·  Python 3 + Capstone + Tkinter",
                 font=FONT_UI, bg=ACCENT, fg="#a0c8e0"
                 ).pack(pady=(4, 0))
        # Gloss stripe
        tk.Frame(hero, bg="#4ab0e8", height=3).pack(fill="x", pady=(12, 0))

        def section(title, emoji=""):
            f = tk.Frame(inner, bg=BG3, padx=24, pady=16,
                         highlightthickness=1, highlightbackground=BORDER)
            f.pack(fill="x", padx=24, pady=(16, 0))
            tk.Label(f, text=f"{emoji}  {title}",
                     font=FONT_TITLE, bg=BG3, fg=ACCENT
                     ).pack(anchor="w", pady=(0, 10))
            tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=(0, 10))
            return f

        # Credits
        cf = section("CREDITS", "🏆")
        credits = [
            ("Tool",         "NEONFLUX"),
            ("Built with",   "Python 3  ·  tkinter  ·  Capstone"),
            ("Optional",     "Keystone assembler engine"),
            ("PE parsing",   "pefile library"),
            ("Architecture", "x86 32/64-bit  ·  ARM  ·  ARM64"),
            ("License",      "MIT — use freely, credit appreciated"),
        ]
        for lbl, val in credits:
            r = tk.Frame(cf, bg=BG3)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=f"{lbl}:", font=FONT_UI_B, bg=BG3, fg=FG_DIM,
                     width=14, anchor="w").pack(side="left")
            tk.Label(r, text=val, font=FONT_MONO, bg=BG3, fg=FG,
                     anchor="w").pack(side="left")

        # Features
        ff = section("FEATURES", "✨")
        features = [
            "Disassemble PE executables, DLLs, raw binaries",
            "Editable disassembly — modify ASM instructions in-place",
            "Hex editor — edit bytes directly, 16 per row with ASCII",
            "ROM space meter — track used vs available bytes",
            "Patch bytes at any file offset via the Patch dialog",
            "Go-to-address — jump to any VA or file offset instantly",
            "String extraction with live filter",
            "Search across disassembly, hex, and strings",
            "Save / Save As — write patched binary back to disk",
            "Section-aware analysis — disassemble individual sections",
        ]
        for feat in features:
            r = tk.Frame(ff, bg=BG3)
            r.pack(anchor="w", pady=2)
            tk.Label(r, text="  ✓", font=FONT_UI_B, bg=BG3, fg=ACCENT2
                     ).pack(side="left")
            tk.Label(r, text=f"  {feat}", font=FONT_UI, bg=BG3, fg=FG,
                     anchor="w").pack(side="left")

        # Notes
        nf = section("NOTES & CREDITS", "✏")
        tk.Label(nf, text="Editable — your text is kept for the session",
                 font=FONT_UI, bg=BG3, fg=FG_DIM
                 ).pack(anchor="w", pady=(0, 6))
        self.about_notes = tk.Text(
            nf, bg=GLASS, fg=FG, insertbackground=ACCENT,
            font=FONT_MONO, relief="solid", bd=1, height=12,
            highlightthickness=1, highlightbackground=BORDER,
            selectbackground=HILIGHT, wrap="word", padx=10, pady=8)
        self.about_notes.pack(fill="x")
        self.about_notes.insert("end",
            "Project  : NEONFLUX\n"
            "Made By  : JackTheGothGuy\n"
            "Version  : BETA 0.4\n"
            "\n"
            "Info\n"
            "--------------------------------------------\n"
            "Created for a school project and for\n"
            "disassembling Windows PE binaries.\n"
            "\n"
            "  - Special thanks to ...\n"
            "  - Based on research by ...\n"
            "  - Target binary: ...\n"
            "  - Notes: ...\n"
            "\n"
            "If you'd like to support the project,\n"
            "any donation is appreciated — link here.\n"
        )

        # Keyboard shortcuts
        kf = section("KEYBOARD SHORTCUTS", "⌨")
        shortcuts = [
            ("Ctrl+O",       "Open binary file"),
            ("Ctrl+S",       "Save file"),
            ("Ctrl+Shift+S", "Save As"),
            ("Ctrl+P",       "Patch bytes dialog"),
            ("Ctrl+G",       "Go to address"),
            ("Ctrl+E",       "Apply ASM edits"),
            ("Ctrl+Return",  "Apply hex edits"),
            ("Ctrl+D",       "Search disassembly"),
            ("Ctrl+H",       "Search hex editor"),
            ("Ctrl+F",       "Filter strings"),
            ("F5",           "Re-analyze binary"),
            ("Ctrl+Q",       "Quit"),
        ]
        cols_f = tk.Frame(kf, bg=BG3)
        cols_f.pack(anchor="w")
        half = len(shortcuts) // 2
        for col_idx, chunk in enumerate([shortcuts[:half], shortcuts[half:]]):
            col_f = tk.Frame(cols_f, bg=BG3)
            col_f.pack(side="left", padx=(0, 40))
            for key, desc in chunk:
                r = tk.Frame(col_f, bg=BG3)
                r.pack(anchor="w", pady=2)
                tk.Label(r, text=f"  {key:<18}", font=FONT_MONO,
                         bg=BG3, fg=ACCENT2, anchor="w", width=20
                         ).pack(side="left")
                tk.Label(r, text=desc, font=FONT_UI, bg=BG3, fg=FG,
                         anchor="w").pack(side="left")

        tk.Frame(inner, bg=BG, height=32).pack(fill="x")
        self._about_tab_index = self.nb.index("end") - 1

    def _show_about_tab(self):
        self.nb.select(self._about_tab_index)

    #Status Bar -----------------------------------------------------------

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=BG3, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        tk.Frame(bar, bg=BORDER, height=1).pack(fill="x", side="top")
        self.status_var = tk.StringVar(value="Ready — open a binary to begin.")
        tk.Label(bar, textvariable=self.status_var, font=FONT_UI,
                 bg=BG3, fg=FG_DIM, anchor="w"
                 ).pack(side="left", padx=12)
        self.modified_lbl = tk.Label(bar, text="", font=FONT_UI_B,
                                      bg=BG3, fg="#e67e22")
        self.modified_lbl.pack(side="right", padx=12)
        self.progress = ttk.Progressbar(bar, mode="indeterminate", length=120)
        self.progress.configure(style="P.Horizontal.TProgressbar")

    #Text tag setup -------------------------------------------------------

    def _setup_asm_tags(self):
        t = self.asm_text
        t.tag_configure("addr",    foreground=ACCENT,   font=("Consolas", 10, "bold"))
        t.tag_configure("bytes",   foreground=FG_DIM)
        t.tag_configure("mnem",    foreground=ACCENT2,  font=("Consolas", 10, "bold"))
        t.tag_configure("ops",     foreground=FG)
        t.tag_configure("call",    foreground="#e67e22", font=("Consolas", 10, "bold"))
        t.tag_configure("jmp",     foreground="#8e44ad", font=("Consolas", 10, "bold"))
        t.tag_configure("comment", foreground=FG_DIM,   font=("Consolas", 10, "italic"))
        t.tag_configure("goto_hi", background=ACCENT,   foreground=FG_LIGHT)
        t.tag_configure("dirty",   background=DIRTY_BG)
        t.tag_configure("err",     background=ERR_BG,   foreground="#c0392b")

    def _setup_hex_tags(self):
        t = self.hex_text
        t.tag_configure("hex_byte",  foreground=ACCENT)
        t.tag_configure("hex_zero",  foreground=FG_DIM)
        t.tag_configure("hex_ascii", foreground=ACCENT2)
        t.tag_configure("hex_sep",   foreground=BORDER_DARK)
        t.tag_configure("dirty",     background=DIRTY_BG)

    #Key bindings ---------------------------------------------------------

    def _bind_keys(self):
        self.bind("<Control-o>",      lambda e: self._open_file())
        self.bind("<Control-s>",      lambda e: self._save())
        self.bind("<Control-S>",      lambda e: self._save_as())
        self.bind("<Control-p>",      lambda e: self._open_patch())
        self.bind("<Control-g>",      lambda e: self._goto_address())
        self.bind("<Control-e>",      lambda e: self._apply_asm_edits())
        self.bind("<Control-Return>", lambda e: self._apply_hex_edits())
        self.bind("<Control-f>",      lambda e: self._focus_string_search())
        self.bind("<Control-d>",      lambda e: self._focus_asm_search())
        self.bind("<Control-h>",      lambda e: self._focus_hex_search())
        self.bind("<F5>",             lambda e: self._run_analysis())
        self.bind("<Control-q>",      lambda e: self._on_close())

    #File I/O -------------------------------------------------------------

    def _open_file(self):
        path = filedialog.askopenfilename(
            title="Open Binary",
            filetypes=[("Executables", "*.exe *.dll *.sys *.bin *.so *.elf"),
                       ("All files", "*.*")]
        )
        if not path: return
        if self.modified and not self._confirm_discard(): return
        self.filepath = path
        self.modified = False
        self._update_title()
        with open(path, "rb") as f:
            self.raw_data = f.read()
        try:
            self.pe = pefile.PE(path)
            secs = ["all"] + [
                s.Name.decode(errors="replace").strip("\x00")
                for s in self.pe.sections]
            self.section_menu["values"] = secs
            self.section_menu["state"]  = "readonly"
            self.section_var.set("all")
        except pefile.PEFormatError:
            self.pe = None
            self.section_menu["values"] = ["raw"]
            self.section_var.set("raw")
            self.section_menu["state"]  = "readonly"
        for b in (self.btn_analyze, self.btn_save, self.btn_saveas,
                  self.btn_patch,   self.btn_goto,
                  self.btn_apply_asm, self.btn_apply_hex):
            b["state"] = "normal"
        self._clear_all()
        self._run_analysis()

    def _save(self):
        if not self.filepath:
            self._save_as(); return
        with open(self.filepath, "wb") as f:
            f.write(self.raw_data)
        self.modified = False
        self._update_title()
        self._set_status(f"Saved → {self.filepath}")

    def _save_as(self):
        if not self.raw_data: return
        path = filedialog.asksaveasfilename(
            title="Save As",
            initialfile=os.path.basename(self.filepath or "output.bin"),
            filetypes=[("Binary", "*.bin *.exe *.dll"), ("All files", "*.*")]
        )
        if not path: return
        with open(path, "wb") as f:
            f.write(self.raw_data)
        self.filepath = path
        self.modified = False
        self._update_title()
        self._set_status(f"Saved as → {path}")

    def _confirm_discard(self):
        return messagebox.askyesno("Unsaved Changes",
                                    "Discard unsaved changes?", icon="warning")

    def _update_title(self):
        name = os.path.basename(self.filepath) if self.filepath else "—"
        flag = " •" if self.modified else ""
        self.title(f"NEONFLUX — {name}{flag}")
        self.modified_lbl.config(text="● UNSAVED" if self.modified else "")

    def _on_close(self):
        if self.modified and not self._confirm_discard(): return
        self.destroy()

    #Patch & GoTo ---------------------------------------------------------

    def _open_patch(self):
        if not self.raw_data: return
        def on_patched(new_data):
            self.raw_data = new_data
            self.modified = True
            self._update_title()
            self._run_analysis()
            self._set_status("Patch applied — re-analyzed.")
        PatchDialog(self, self.raw_data, on_patched)

    def _goto_address(self):
        if not self.raw_data: return
        addr_str = simpledialog.askstring(
            "Go to Address",
            "Virtual address or file offset (hex):", parent=self)
        if not addr_str: return
        try:
            addr = int(addr_str.strip().lstrip("0x").lstrip("0X") or "0", 16)
        except ValueError:
            messagebox.showerror("Error", "Invalid address.", parent=self); return
        target  = f"0x{addr:08x}"
        content = self.asm_text.get("1.0", "end").lower()
        idx     = content.find(target)
        if idx != -1:
            line = content[:idx].count("\n") + 1
            col  = idx - content[:idx].rfind("\n") - 1
            self.asm_text.tag_remove("goto_hi", "1.0", "end")
            self.asm_text.tag_add("goto_hi", f"{line}.{col}",
                                   f"{line}.{col+len(target)}")
            self.asm_text.see(f"{line}.0")
            self.nb.select(0)
            self._set_status(f"Jumped to 0x{addr:08X}")
            return
        hex_content = self.hex_text.get("1.0", "end").lower()
        hidx = hex_content.find(f"{addr:08x}")
        if hidx != -1:
            line = hex_content[:hidx].count("\n") + 1
            self.hex_text.see(f"{line}.0")
            self.nb.select(1)
            self._set_status(f"Found 0x{addr:08X} in hex editor.")
            return
        messagebox.showinfo("Go to Address",
            f"0x{addr:08X} not found. Try raising the instruction limit.",
            parent=self)

    #Search ---------------------------------------------------------------

    def _focus_string_search(self):
        self.str_filter_var.set("")
        self._walk_focus(self.str_filter_var)

    def _walk_focus(self, var):
        def _w(w):
            if isinstance(w, tk.Entry):
                try:
                    if w.cget("textvariable") == str(var):
                        w.focus_set(); w.select_range(0, "end"); return True
                except Exception: pass
            for c in w.winfo_children():
                if _w(c): return True
        _w(self)

    def _focus_asm_search(self):
        self.nb.select(0); self.asm_search.show()

    def _focus_hex_search(self):
        self.nb.select(1); self.hex_search.show()

    #Analysis -------------------------------------------------------------

    def _run_analysis(self):
        if not self.filepath: return
        self.btn_analyze["state"] = "disabled"
        self.progress.pack(side="right", padx=12, pady=4)
        self.progress.start(12)
        threading.Thread(target=self._analyze_worker, daemon=True).start()

    def _analyze_worker(self):
        try:
            raw = self.raw_data
            if self.pe:
                self._show_pe_info()
                self._show_sections_list()
                self._disassemble_pe(raw)
            else:
                self._disassemble_raw(raw)
            self._all_strings = extract_strings(raw)
            self.after(0, lambda: self._render_strings(self._all_strings))
            self._populate_hex_editor(raw)
            self._set_status(
                f"Analysis complete — {os.path.basename(self.filepath)}"
                f"  ({len(raw):,} bytes)")
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self._set_status(f"Error: {e}")
        finally:
            self.after(0, self._stop_progress)

    def _stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.btn_analyze["state"] = "normal"

    #PE Info ---------------------------------------------------------------

    def _show_pe_info(self):
        pe = self.pe
        try:
            _, arch, bits = get_architecture(pe)
            self._arch_bits = bits
        except ValueError as e:
            arch = str(e)
        ts = pe.FILE_HEADER.TimeDateStamp
        lines = [
            f"  File        : {os.path.basename(self.filepath)}",
            f"  Architecture: {arch}",
            f"  Entry Point : 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:08X}",
            f"  Image Base  : 0x{pe.OPTIONAL_HEADER.ImageBase:08X}",
            f"  Timestamp   : 0x{ts:08X}",
            f"  Sections    : {len(pe.sections)}",
            f"  File Size   : {len(self.raw_data):,} bytes",
            "",
        ]
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            lines.append(f"  Imports : {len(pe.DIRECTORY_ENTRY_IMPORT)} DLLs")
            for entry in pe.DIRECTORY_ENTRY_IMPORT[:8]:
                dll = entry.dll.decode(errors="replace")
                lines.append(f"    → {dll}")
            if len(pe.DIRECTORY_ENTRY_IMPORT) > 8:
                lines.append(f"    … {len(pe.DIRECTORY_ENTRY_IMPORT)-8} more")
        self.after(0, lambda: write_text(self.pe_frame.text, "\n".join(lines)))

    def _show_sections_list(self):
        def _u():
            self.sec_list.delete(0, "end")
            for s in self.pe.sections:
                name  = s.Name.decode(errors="replace").strip("\x00")
                flags = ""
                c = s.Characteristics
                if c & 0x20000000: flags += "X"
                if c & 0x40000000: flags += "R"
                if c & 0x80000000: flags += "W"
                self.sec_list.insert("end",
                    f"  {name:<10} {flags:<4} 0x{s.VirtualAddress:08X}")
        self.after(0, _u)

    def _on_section_select(self, event):
        sel = self.sec_list.curselection()
        if not sel: return
        name = self.pe.sections[sel[0]].Name.decode(
            errors="replace").strip("\x00")
        self.section_var.set(name)
        self._run_analysis()

    #Disassembly -----------------------------------------------------------

    def _disassemble_pe(self, raw):
        pe = self.pe
        try:
            md, _, bits = get_architecture(pe)
            self._arch_bits = bits
        except ValueError:
            md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
            md.detail = True
        limit      = self._get_limit()
        target     = self.section_var.get()
        image_base = pe.OPTIONAL_HEADER.ImageBase
        lines, meta = [], []
        for section in pe.sections:
            sname = section.Name.decode(errors="replace").strip("\x00")
            if target != "all" and sname != target: continue
            data        = section.get_data()
            base_addr   = image_base + section.VirtualAddress
            file_offset = section.PointerToRawData
            lines.append(("header", f"\n;;{sname}  0x{base_addr:08X} --\n"))
            meta.append(None)
            count = 0
            for insn in md.disasm(data, base_addr):
                rb  = " ".join(f"{b:02x}" for b in insn.bytes[:8])
                off = file_offset + (insn.address - base_addr)
                lines.append(("insn", insn.address, rb,
                               insn.mnemonic, insn.op_str))
                meta.append((off, len(insn.bytes), insn.address,
                              insn.mnemonic, insn.op_str))
                count += 1
                if limit and count >= limit:
                    lines.append(("trunc",
                        f";; [truncated at {limit} — raise limit]\n"))
                    meta.append(None)
                    break
        self._asm_meta = meta
        self.after(0, lambda: self._render_asm(lines))

    def _disassemble_raw(self, data):
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        md.detail = True
        limit = self._get_limit()
        lines = [("header", "\n")]
        meta  = [None]
        count = 0
        for insn in md.disasm(data, 0x0):
            rb = " ".join(f"{b:02x}" for b in insn.bytes[:8])
            lines.append(("insn", insn.address, rb,
                           insn.mnemonic, insn.op_str))
            meta.append((insn.address, len(insn.bytes),
                          insn.address, insn.mnemonic, insn.op_str))
            count += 1
            if limit and count >= limit:
                lines.append(("trunc", f";; [truncated at {limit}]\n"))
                meta.append(None)
                break
        self._asm_meta = meta
        self.after(0, lambda: self._render_asm(lines))

    def _render_asm(self, lines):
        t = self.asm_text
        t.delete("1.0", "end")
        for item in lines:
            kind = item[0]
            if kind in ("header", "trunc"):
                t.insert("end", item[1], "comment")
            elif kind == "insn":
                _, addr, rb, mnem, ops = item
                t.insert("end", f"  0x{addr:08X}  ", "addr")
                t.insert("end", f"{rb:<26}  ", "bytes")
                if mnem.startswith("j"):
                    t.insert("end", f"{mnem:<10}", "jmp")
                elif mnem in ("call", "ret", "retn"):
                    t.insert("end", f"{mnem:<10}", "call")
                else:
                    t.insert("end", f"{mnem:<10}", "mnem")
                t.insert("end", f"{ops}\n", "ops")
        self.asm_dirty_lbl.config(text="")

    #ASM edit tracking -----------------------------------------------------

    def _asm_on_key(self, event=None):
        t    = self.asm_text
        line = int(t.index("insert").split(".")[0])
        t.tag_add("dirty", f"{line}.0", f"{line}.end")
        self.asm_dirty_lbl.config(text="● edited — Ctrl+E to assemble")
        self._mark_modified()

    #Apply ASM edits -------------------------------------------------------

    def _apply_asm_edits(self):
        if not self._asm_meta:
            messagebox.showinfo("Nothing to apply", "Run analysis first.", parent=self); return

        t          = self.asm_text
        content    = t.get("1.0", "end")
        text_lines = content.splitlines()
        raw        = bytearray(self.raw_data)
        errors     = []
        changed    = 0
        meta_idx   = 0

        for lno, line in enumerate(text_lines):
            stripped = line.strip()
            if stripped.startswith(";") or not stripped:
                meta_idx += 1
                continue
            if meta_idx >= len(self._asm_meta):
                break
            m = self._asm_meta[meta_idx]
            meta_idx += 1
            if m is None:
                continue
            file_off, insn_size, addr, orig_mnem, orig_ops = m

            try:
                rest = line
                if rest.startswith("  0x"):
                    rest = rest[14:]   # skip "  0xXXXXXXXX  "
                    rest = rest[28:] if len(rest) >= 28 else rest.lstrip()
                else:
                    rest = rest.strip()
                parts    = rest.strip().split(None, 1)
                if not parts: continue
                new_mnem = parts[0].lower()
                new_ops  = parts[1].strip() if len(parts) > 1 else ""

                if new_mnem == orig_mnem.lower() and new_ops == orig_ops:
                    continue

                encoded, err = simple_assemble(
                    new_mnem, new_ops, insn_size, self._arch_bits)
                if err and encoded is None:
                    errors.append(f"Line {lno+1}: {err}")
                    t.tag_add("err", f"{lno+1}.0", f"{lno+1}.end")
                    continue

                for i, b in enumerate(encoded):
                    if file_off + i < len(raw):
                        raw[file_off + i] = b
                t.tag_remove("dirty", f"{lno+1}.0", f"{lno+1}.end")
                t.tag_remove("err",   f"{lno+1}.0", f"{lno+1}.end")
                changed += 1
            except Exception as ex:
                errors.append(f"Line {lno+1}: {ex}")

        if errors:
            messagebox.showwarning("Assembly Errors",
                "\n".join(errors[:10]) +
                (f"\n… and {len(errors)-10} more" if len(errors) > 10 else ""),
                parent=self)

        if changed:
            self.raw_data = bytes(raw)
            self.modified = True
            self._update_title()
            self._run_analysis()
            self._set_status(f"Assembled {changed} instruction(s) — re-analyzed.")
            self.asm_dirty_lbl.config(text="")
        else:
            self._set_status("No changes detected in disassembly.")

    #Hex Editor ------------------------------------------------------------

    def _populate_hex_editor(self, data):
        total = len(data)
        used  = sum(1 for b in data if b != 0xFF)
        lines = []
        for i in range(0, total, COLS):
            chunk = data[i:i+COLS]
            hex_  = " ".join(f"{b:02x}" for b in chunk)
            hex_  = f"{hex_:<{COLS*3-1}}"
            asc   = "".join(chr(b) if 0x20 <= b < 0x7F else "·" for b in chunk)
            lines.append(f"{hex_}  │  {asc}")

        def _do():
            t = self.hex_text
            t.delete("1.0", "end")
            t.insert("end", "\n".join(lines))
            self._recolor_hex()
            self.rom_meter.update(used, total)
        self.after(0, _do)

    def _recolor_hex(self):
        t       = self.hex_text
        content = t.get("1.0", "end")
        for tag in ("hex_byte", "hex_zero", "hex_ascii", "hex_sep"):
            t.tag_remove(tag, "1.0", "end")
        for lno, line in enumerate(content.splitlines(), 1):
            sep_idx = line.find("│")
            if sep_idx == -1: continue
            hex_part = line[:sep_idx]
            for m in re.finditer(r"[0-9a-fA-F]{2}", hex_part):
                val = int(m.group(), 16)
                tag = "hex_zero" if val == 0 else "hex_byte"
                t.tag_add(tag, f"{lno}.{m.start()}", f"{lno}.{m.end()}")
            t.tag_add("hex_sep",   f"{lno}.{sep_idx}", f"{lno}.{sep_idx+3}")
            t.tag_add("hex_ascii", f"{lno}.{sep_idx+3}", f"{lno}.end")

    def _hex_on_key(self, event=None):
        t    = self.hex_text
        line = int(t.index("insert").split(".")[0])
        t.tag_add("dirty", f"{line}.0", f"{line}.end")
        self._mark_modified()

    #Apply Hex edits -------------------------------------------------------

    def _apply_hex_edits(self):
        t       = self.hex_text
        content = t.get("1.0", "end")
        new_raw = bytearray(self.raw_data)
        errors  = []
        changed = 0

        for lno, line in enumerate(content.splitlines()):
            sep_idx  = line.find("│")
            hex_part = line[:sep_idx].strip() if sep_idx != -1 else line.strip()
            if not hex_part: continue
            offset = lno * COLS
            for i, tok in enumerate(hex_part.split()):
                if len(tok) != 2: continue
                try:
                    b = int(tok, 16)
                except ValueError:
                    errors.append(f"Line {lno+1} token '{tok}': invalid hex"); continue
                pos = offset + i
                if pos < len(new_raw):
                    if new_raw[pos] != b:
                        new_raw[pos] = b; changed += 1

        if errors:
            messagebox.showwarning("Hex Parse Errors",
                                    "\n".join(errors[:10]), parent=self)

        if changed:
            self.raw_data = bytes(new_raw)
            self.modified = True
            self._update_title()
            total = len(self.raw_data)
            used  = sum(1 for b in self.raw_data if b != 0xFF)
            self.rom_meter.update(used, total)
            t.tag_remove("dirty", "1.0", "end")
            self._recolor_hex()
            self._run_analysis()
            self._set_status(f"Hex edits applied — {changed} byte(s) changed.")
        else:
            self._set_status("No hex changes detected.")

    #Strings ---------------------------------------------------------------

    def _render_strings(self, found):
        lines = [f"  {len(found)} strings (min 5 chars)\n"]
        for offset, s in found[:1000]:
            lines.append(f"  0x{offset:08X}  {s}")
        if len(found) > 1000:
            lines.append(f"\n  [… {len(found)-1000} more omitted]")
        write_text(self.str_frame.text, "\n".join(lines))

    def _filter_strings(self):
        q = self.str_filter_var.get().lower().strip()
        if not self._all_strings: return
        filtered = ([(o, s) for o, s in self._all_strings if q in s.lower()]
                    if q else self._all_strings)
        self._render_strings(filtered)
        self._set_status(f"Strings: {len(filtered)} match(es)"
                         + (f" for '{q}'" if q else ""))

    #Helpers ---------------------------------------------------------------








    def _mark_modified(self):
        if not self.modified:
            self.modified = True
            self._update_title()

    def _get_limit(self):
        try:    return max(0, int(self.limit_var.get()))
        except: return 500

    def _set_status(self, msg):
        self.after(0, lambda: self.status_var.set(msg))

    def _clear_all(self):
        for w in (self.pe_frame.text, self.str_frame.text):
            w.configure(state="normal")
            w.delete("1.0", "end")
            w.configure(state="disabled")
        self.asm_text.delete("1.0", "end")
        self.hex_text.delete("1.0", "end")
        self.sec_list.delete(0, "end")
        self._asm_meta = []

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



#Entry ---------------------------------------------------------------------

if __name__ == "__main__":
    app = DisassemblerApp()
    app.mainloop()