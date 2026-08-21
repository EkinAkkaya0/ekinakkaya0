#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASCII sahne: üç ekranlı gece masası.

Satırlar elle yazılmaz; bir karakter tuvaline kutu/metin çizilir, böylece
hizalama garanti olur. Çıktı tema duyarlı SVG'dir (kod blokları tema
duyarlı olmadığı için koyu temada tonlar ters dönüyordu). Her satır renk
koşularına bölünüp ayrı <text> olarak basılır; genişlik textLength ile
sabit, yani kullanıcının fontundan bağımsız.

Durağan — sayfada hareket eden tek şey yılan.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

LIGHT = dict(name="light", card="#FFFFFF", edge="#D0D7DE", ink="#0D1117", frame="#57606A",
             faint="#C2C9D0", dim="#8C959F", ok="#1A7F37", warn="#9A6700", glow="#EEF2F5",
             rim=None, rim_a=0)
DARK  = dict(name="dark", card="#0D1117", edge="#30363D", ink="#E6EDF3", frame="#6E7681",
             faint="#2B3138", dim="#8B949E", ok="#3FB950", warn="#D29922", glow="#161C24",
             rim="#FFFFFF", rim_a=0.075)

W, H = 104, 33          # tuval: sütun x satır


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.ch = [[" "]*w for _ in range(h)]
        self.co = [["frame"]*w for _ in range(h)]

    def put(self, x, y, s, color="frame"):
        if not (0 <= y < self.h):
            return
        for i, c in enumerate(s):
            if 0 <= x+i < self.w:
                self.ch[y][x+i] = c
                self.co[y][x+i] = color

    def box(self, x, y, w, h, color="frame", round_=False):
        tl, tr, bl, br = ("╭", "╮", "╰", "╯") if round_ else ("┌", "┐", "└", "┘")
        self.put(x, y, tl + "─"*(w-2) + tr, color)
        for i in range(1, h-1):
            self.put(x, y+i, "│", color); self.put(x+w-1, y+i, "│", color)
        self.put(x, y+h-1, bl + "─"*(w-2) + br, color)

    def sep(self, x, y, w, color="frame"):
        self.put(x, y, "├" + "─"*(w-2) + "┤", color)

    def fill(self, x, y, w, h, c, color="faint"):
        for i in range(h):
            self.put(x, y+i, c*w, color)


def scene():
    """Ekranlardaki her şey uydurmadır; gerçek proje, sunucu ya da alan adı geçmez."""
    c = Canvas(W, H)

    # ── gece göğü: yıldızlar ve hilal ────────────────────────────────
    for x, y in ((6,0),(19,1),(31,0),(44,1),(57,0),(70,1),(88,0),(97,1),(13,1),(78,0)):
        c.put(x, y, "·", "faint")
    for x, y in ((25,0),(52,1),(83,1)):
        c.put(x, y, "*", "dim")
    c.put(95, 0, ".-.", "warn"); c.put(94, 1, "(  `", "warn")

    # ── üstte geniş ekran: kod editörü ───────────────────────────────
    IX, IY, IW, IH = 2, 2, 74, 14
    c.box(IX, IY, IW, IH, "frame")
    c.put(IX+2, IY+1, "● ● ●", "dim")
    c.put(IX+10, IY+1, "src/server.js", "ink")
    c.put(IX+IW-9, IY+1, "IDE", "dim")
    c.sep(IX, IY+2, IW, "frame")
    for i in range(1, IH-4):
        c.put(IX+16, IY+2+i, "│", "frame")
    tree = ["▾ src", "  ▸ routes", "  ▸ models", "  • server.js", "  • db.js", "▸ tests", "▸ scripts", "  .env"]
    for i, t in enumerate(tree):
        c.put(IX+2, IY+3+i, t[:13], "ok" if i == 3 else "dim")
    code = [
        (" 41", 'import express from "express";', "ink"),
        (" 42", 'import { router } from "./routes";', "ink"),
        (" 43", "", "ink"),
        (" 44", "const app = express();", "ink"),
        (" 45", "app.use(express.json());", "ok"),
        (" 46", 'app.use("/api", router);', "ink"),
        (" 47", "", "ink"),
        (" 48", "export default app;", "dim"),
    ]
    for i, (ln, src, col) in enumerate(code):
        c.put(IX+18, IY+3+i, ln, "faint")
        c.put(IX+22, IY+3+i, src[:IW-25], col)
    c.sep(IX, IY+IH-3, IW, "frame")
    c.put(IX+2, IY+IH-2, "main", "ok")
    c.put(IX+12, IY+IH-2, "0 hata   2 uyarı", "dim")
    c.put(IX+IW-16, IY+IH-2, "JS  UTF-8  LF", "dim")
    c.put(IX+IW//2-4, IY+IH, "└──┬──┘", "dim")

    # ── sağda dik ekran: sunucu terminali ────────────────────────────
    TX, TY, TW, TH = 80, 2, 22, 23
    c.box(TX, TY, TW, TH, "frame")
    c.put(TX+2, TY+1, "root@srv01", "ok")
    c.sep(TX, TY+2, TW, "frame")
    term = [
        ("$ docker ps", "ink"), ("web        up 9d", "dim"), ("api        up 9d", "dim"),
        ("db         up 9d", "dim"), ("cache      up 9d", "dim"), ("", "dim"),
        ("$ ./deploy.sh", "ink"), ("build      ok", "ok"), ("migrate    ok", "ok"),
        ("validate   ok", "ok"), ("promote    ok", "ok"), ("smoke      ok", "ok"),
        ("0 downtime", "warn"), ("", "dim"), ("$ tail -f app.log", "ink"),
        ("200 GET /health", "dim"), ("200 GET /api", "dim"),
    ]
    for i, (t, col) in enumerate(term[:TH-6]):
        c.put(TX+2, TY+3+i, t[:TW-4], col)
    c.put(TX+2, TY+TH-3, "█", "ok")
    c.put(TX+TW//2-3, TY+TH, "└──┬──┘", "dim")

    # ── ortada dizüstü: ekran + gövde + klavye ───────────────────────
    MX, MY, MW, MH = 20, 17, 44, 8
    c.box(MX, MY, MW, MH, "frame")
    c.put(MX+2, MY+1, "● ● ●", "dim")
    c.put(MX+9, MY+1, "localhost:3000", "ink")
    c.sep(MX, MY+2, MW, "frame")
    # sayfa içeriği: gerçek metin değil, yer tutucu bloklar
    c.put(MX+3, MY+3, "████████████  ▁▁▁▁▁▁▁▁", "ok")
    c.put(MX+3, MY+4, "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓", "dim")
    c.put(MX+3, MY+5, "▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓", "faint")

    # gövde: menteşeden biraz geniş, üstünde dizüstü klavyesi ve izleme yüzeyi
    DX, DY, DW, DH = MX-3, MY+MH, MW+6, 7
    c.box(DX, DY, DW, DH, "dim", round_=True)
    keys = [
        "▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄▄",
        " ▄▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄▄▄",
        "  ▄▄▄▄ ▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄ ▄▄▄ ▄▄ ▄▄",
    ]
    for i, r in enumerate(keys):
        c.put(DX+3, DY+1+i, r[:DW-5], "faint")
    tp = 14
    c.put(DX + (DW-tp)//2, DY+4, "┌" + "─"*(tp-2) + "┐", "faint")
    c.put(DX + (DW-tp)//2, DY+5, "└" + "─"*(tp-2) + "┘", "faint")

    # ── kahve ────────────────────────────────────────────────────────
    QX, QY = 71, 26
    c.put(QX+2, QY,   "≈  ≈", "faint")
    c.put(QX,   QY+1, "┌──────┐", "dim")
    c.put(QX,   QY+2, "│      ├╮", "dim")
    c.put(QX,   QY+3, "│      │╯", "dim")
    c.put(QX,   QY+4, "╰──────╯", "dim")

    # ── masa kenarı ve ekran ışığının masaya vurması ─────────────────
    c.put(0, H-1, "─"*W, "edge")
    for x in range(6, 70):
        if c.ch[H-2][x] == " ":
            c.ch[H-2][x] = "·"; c.co[H-2][x] = "glow"
    return c

FS = 13.5
CW = FS * 0.6005
LH = 16.4
PAD_TOP, PAD_BOT = 26, 22
PANEL_W = 1000


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(p, c):
    height = int(PAD_TOP + c.h*LH + PAD_BOT)
    left = (PANEL_W - c.w*CW) / 2
    o = [f'<rect width="{PANEL_W}" height="{height}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{PANEL_W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" '
                 f'stroke-width="1.2" fill="none"/>')

    for y in range(c.h):
        row, cols = c.ch[y], c.co[y]
        x = 0
        while x < c.w:
            if row[x] == " ":
                x += 1; continue
            key = cols[x]; start = x
            while x < c.w and cols[x] == key and row[x] != " ":
                x += 1
            txt = "".join(row[start:x])
            n = len(txt)
            o.append(f'<text x="{left + start*CW:.1f}" y="{PAD_TOP + y*LH + FS*0.78:.1f}" '
                     f'font-family="{MONO}" font-size="{FS}" fill="{p[key]}" '
                     f'xml:space="preserve" textLength="{n*CW:.1f}" lengthAdjust="spacing">'
                     f'{esc(txt)}</text>')

    o.append(f'<rect x="0.5" y="0.5" width="{PANEL_W-1}" height="{height-1}" rx="6" '
             f'fill="none" stroke="{p["edge"]}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PANEL_W} {height}" '
            f'width="{PANEL_W}" height="{height}" role="img" '
            f'aria-label="ASCII çizim: gece çalışma masası — üstte geniş ekranda kod editörü, '
            f'ortada dizüstünde tarayıcı, sağda dik ekranda sunucu terminali, önde klavye, '
            f'yanda kahve">{"".join(o)}</svg>\n')


def main():
    c = scene()
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"scene-{p['name']}.svg").write_text(build(p, c), encoding="utf-8")
    print(f"sahne yazıldı: {c.w}x{c.h} tuval")


if __name__ == "__main__":
    main()
