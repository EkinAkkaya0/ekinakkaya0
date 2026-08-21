#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yığın ızgarası: tek SVG, tema duyarlı.

Önceden bu bölüm 50 ayrı shields.io isteğiydi — sayfadaki uzak isteklerin
neredeyse tamamı. Artık tek dosya: logo yolları simple-icons'tan (CC0)
tools/icons.json içine gömülü, hiçbir dış servise bağlı değil.

Durağan.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICONS = json.load(open(pathlib.Path(__file__).resolve().parent / "icons.json"))
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

LIGHT = dict(name="light", card="#FFFFFF", chip="#F6F8FA", edge="#D0D7DE",
             chipedge="#D8DEE4", ink="#1F2328", label="#0D1117", faint="#6E7781",
             ok="#1A7F37", rim=None, rim_a=0)
DARK  = dict(name="dark", card="#0D1117", chip="#161B22", edge="#30363D",
             chipedge="#2A313A", ink="#E6EDF3", label="#F0F6FC", faint="#8B949E",
             ok="#3FB950", rim="#FFFFFF", rim_a=0.075)

# (kategori, [(ad, ikon-slug | None, logo rengi)])
STACK = [
 ("Runtime & API", [
    ("Node.js","nodedotjs","#5FA04E"), ("Express","express","#9AA4AE"),
    ("ES Modules",None,None), ("Socket.IO","socketdotio","#9AA4AE"),
    ("REST",None,None), ("Python","python","#3776AB"),
    ("FastAPI","fastapi","#009688"), ("PHP / Laravel","laravel","#FF2D20")]),
 ("Frontend", [
    ("Next.js","nextdotjs","#9AA4AE"), ("React","react","#61DAFB"),
    ("TypeScript","typescript","#3178C6"), ("Tailwind","tailwindcss","#06B6D4"),
    ("MUI","mui","#007FFF"), ("Vite","vite","#646CFF")]),
 ("Mobil", [
    ("Flutter","flutter","#02569B"), ("Dart","dart","#0175C2")]),
 ("Veri katmanı", [
    ("PostgreSQL","postgresql","#4169E1"), ("Sequelize","sequelize","#52B0E7"),
    ("Prisma","prisma","#7C8AA0"), ("Migration",None,None),
    ("Transaction / ACID",None,None), ("Decimal",None,None)]),
 ("Geospatial", [
    ("PostGIS","postgresql","#3FB950"), ("GeoServer","osgeo","#4CAF50"),
    ("GDAL / OGR","gdal","#5CAE58"), ("QGIS","qgis","#8BC34A"),
    ("OpenLayers","openlayers","#4FC3F7"), ("Leaflet","leaflet","#7CB342"),
    ("OGC WMS / WFS",None,None), ("Vektör karo (MVT)",None,None),
    ("SLD",None,None), ("EPSG / CRS",None,None), ("GeoPackage",None,None)]),
 ("DevOps", [
    ("Docker","docker","#2496ED"), ("GitHub Actions","githubactions","#58A6FF"),
    ("nginx","nginx","#3FB950"), ("Linux","linux","#FCC624"),
    ("Blue-Green Deployment",None,None), ("GHCR",None,None), ("systemd",None,None)]),
 ("Gözlemlenebilirlik", [
    ("Grafana","grafana","#F46800"), ("Sentry / GlitchTip","sentry","#A78BFA"),
    ("MinIO / S3","minio","#F87171"), ("Let's Encrypt","letsencrypt","#5EA9E8"),
    ("Postfix / Dovecot",None,None)]),
 ("Entegrasyon", [
    ("SSO / OAuth",None,None), ("Webhook",None,None), ("iyzico",None,None),
    ("Trendyol",None,None), ("GTFS",None,None), ("OCR",None,None)]),
]

W        = 1000
PAD      = 26
LABEL_W  = 168
CHIP_X   = PAD + LABEL_W + 14
CHIP_R   = W - PAD
CHIP_H   = 27
CHIP_GAP = 7
ROW_GAP  = 8
FS       = 11.5
CWID     = FS * 0.6005          # monospace ilerleme
ICO      = 14


def chip_w(name, has_icon):
    inner = len(name) * CWID
    return round(inner + (ICO + 7 if has_icon else 0) + 22, 1)


def build(p):
    rows = []                                   # (kategori, [[(x,w,ad,slug,renk)], ...])
    for cat, items in STACK:
        lines, cur, x = [], [], CHIP_X
        for name, slug, col in items:
            w = chip_w(name, bool(slug))
            if x + w > CHIP_R and cur:
                lines.append(cur); cur = []; x = CHIP_X
            cur.append((x, w, name, slug, col)); x += w + CHIP_GAP
        if cur:
            lines.append(cur)
        rows.append((cat, lines))

    H = PAD
    for _, lines in rows:
        H += max(1, len(lines)) * CHIP_H + (len(lines)-1)*ROW_GAP + 20
    H = int(H + PAD - 20)

    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" '
                 f'stroke-width="1.2" fill="none"/>')

    defs = []
    for slug in {s for _, items in STACK for _, s, _ in items if s}:
        defs.append(f'<g id="i{slug}"><path d="{ICONS[slug]}"/></g>')

    y = PAD
    for gi, (cat, lines) in enumerate(rows):
        blk = len(lines)*CHIP_H + (len(lines)-1)*ROW_GAP
        if gi:
            o.append(f'<line x1="{PAD}" y1="{y-10}" x2="{W-PAD}" y2="{y-10}" stroke="{p["edge"]}"/>')
        o.append(f'<rect x="{PAD}" y="{y+2}" width="2.5" height="{blk-4}" rx="1.25" fill="{p["ok"]}" opacity="0.55"/>')
        o.append(f'<text x="{PAD+12}" y="{y+CHIP_H/2+4:.1f}" font-family="{MONO}" font-size="12" '
                 f'font-weight="700" fill="{p["label"]}">{cat.replace("&","&amp;")}</text>')
        for li, line in enumerate(lines):
            ly = y + li*(CHIP_H+ROW_GAP)
            for cx, cw, name, slug, col in line:
                o.append(f'<rect x="{cx:.1f}" y="{ly}" width="{cw:.1f}" height="{CHIP_H}" rx="6" '
                         f'fill="{p["chip"]}" stroke="{p["chipedge"]}"/>')
                tx = cx + 11
                if slug:
                    o.append(f'<use href="#i{slug}" xlink:href="#i{slug}" fill="{col}" '
                             f'transform="translate({tx:.1f},{ly+(CHIP_H-ICO)/2:.1f}) '
                             f'scale({ICO/24:.4f})"/>')
                    tx += ICO + 7
                o.append(f'<text x="{tx:.1f}" y="{ly+CHIP_H/2+4:.1f}" font-family="{MONO}" '
                         f'font-size="{FS}" fill="{p["ink"]}">{name.replace("&","&amp;")}</text>')
        y += blk + 20

    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')
    n = sum(len(i) for _, i in STACK)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Teknoloji yığını: {len(STACK)} kategoride {n} teknoloji">'
            f'<defs>{"".join(defs)}</defs>{"".join(o)}</svg>\n')


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"stack-{p['name']}.svg").write_text(build(p), encoding="utf-8")
    n = sum(len(i) for _, i in STACK)
    print(f"yığın ızgarası yazıldı: {len(STACK)} kategori, {n} teknoloji")


if __name__ == "__main__":
    main()
