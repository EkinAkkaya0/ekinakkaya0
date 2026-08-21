#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASCII sahne: gece çalışma masası.

Kod bloğu yerine tema duyarlı SVG olarak basılır — kod blokları tema
duyarlı olmadığı için koyu temada tonlar ters dönüyordu. SVG'de her tema
için ayrı renk verilebiliyor ve karakter genişliği textLength ile
sabitlendiği için hizalama fonttan bağımsız duruyor.

Durağan; sayfada hareket eden tek şey yılan.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

LIGHT = dict(name="light", card="#FFFFFF", edge="#D0D7DE", ink="#0D1117", sub="#57606A",
             faint="#B0B8BF", ok="#1A7F37", dim="#8C959F", rim=None, rim_a=0)
DARK  = dict(name="dark", card="#0D1117", edge="#30363D", ink="#E6EDF3", sub="#8B949E",
             faint="#3D444D", ok="#3FB950", dim="#6E7681", rim="#FFFFFF", rim_a=0.075)

# (satır, renk anahtarı)
SCENE = [
    ("       .                         *                              .",        "faint"),
    ("                 .                             *                        .", "faint"),
    ("     ╭──────────────────────────────────────────────────╮",               "sub"),
    ("     │                                                  │",               "sub"),
    ("     │                                                  │",               "sub"),
    ("     │ $ deploy --blue-green                            │",               "ink"),
    ("     │ migrate ok   validate ok   promote ok            │",               "ok"),
    ("     │ 0 downtime                                       │",               "dim"),
    ("     │                                                  │",               "sub"),
    ("     ╰────────────────────────┬─────────────────────────╯",               "sub"),
    ("               ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄",                             "dim"),
    ("",                                                                         "sub"),
    ("        ┌──────────────────────────────────────┐",                        "dim"),
    ("        │ ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪ │",                        "faint"),
    ("        └──────────────────────────────────────┘",                        "dim"),
    ("  ══════════════════════════════════════════════════════════════════════", "edge"),
]
# sağdaki kule ve fincan, ayrı sütun olarak bindirilir
OVERLAY = [
    (3,  "       ▁▂▄▆█▇▅▃▂▁▂▃▅▇█▆▄▂▁▂▄▆█▇▅▃▂▁▂▃▅▇█▆▄▂▁▂▄▆█▇▅▃▂▁▂▃", "ok"),
    (3,  "                                                            ┌─────────┐", "dim"),
    (4,  "                                                            │ ▓▓▓  ░░ │", "sub"),
    (5,  "                                                            │ ▓▓▓  ░░ │", "sub"),
    (6,  "                                                            │ ▓▓▓  ░░ │", "sub"),
    (7,  "                                                            │ ▓▓▓  ░░ │", "sub"),
    (8,  "                                                            │ ▓▓▓  ░░ │", "sub"),
    (9,  "                                                            │ ░░░  ░░ │", "sub"),
    (10, "                                                            └─────────┘", "dim"),
    (12, "                                                      .---.", "dim"),
    (13, "                                                      |   |]", "dim"),
    (14, "                                                      `---'", "dim"),
]

FS = 17.0
CW = FS * 0.6005
LH = 20.0
PAD_X, PAD_TOP, PAD_BOT = 34, 30, 26


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(p):
    cols = max([len(t) for t, _ in SCENE] + [len(t) for _, t, _ in OVERLAY])
    W = 1000                                   # diğer varlıklarla aynı ölçek
    left = (W - cols*CW) / 2
    H = int(PAD_TOP + len(SCENE)*LH + PAD_BOT)
    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" '
                 f'stroke-width="1.2" fill="none"/>')

    def line(i, text, key):
        if not text.strip():
            return
        n = len(text)
        y = PAD_TOP + i*LH + FS*0.78
        o.append(f'<text x="{left:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{FS}" '
                 f'fill="{p[key]}" xml:space="preserve" textLength="{n*CW:.1f}" '
                 f'lengthAdjust="spacing">{esc(text)}</text>')

    for i, (t, k) in enumerate(SCENE):
        line(i, t, k)
    for i, t, k in OVERLAY:
        line(i, t, k)

    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" '
             f'stroke="{p["edge"]}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
            f'height="{H}" role="img" aria-label="ASCII çizim: gece çalışma masası, '
            f'ekranda mavi-yeşil dağıtım çıktısı, yanında sunucu kulesi">'
            f'{"".join(o)}</svg>\n')


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"scene-{p['name']}.svg").write_text(build(p), encoding="utf-8")
    cols = max([len(t) for t, _ in SCENE] + [len(t) for _, t, _ in OVERLAY])
    print(f"sahne yazıldı: {len(SCENE)} satır, {cols} sütun")


if __name__ == "__main__":
    main()
