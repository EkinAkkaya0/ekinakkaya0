#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub'ın GERÇEK rozetleri (Pull Shark, YOLO vb.) — metrics'in kendi hesapladığı
S/A/B/C/X sıralaması değil.

Resmi API yok; profil sayfası ?tab=achievements tokensiz okunur. Rozet PNG'leri
github.githubassets.com'dan indirilip base64 olarak SVG'ye gömülür: tanınır ikon,
sayfanın kendi kart stili, sıfır uzak istek. Her rozetin altında ne anlama geldiği.
"""
import base64, pathlib, re, urllib.request

USER = "ekinakkaya0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans',sans-serif"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

LIGHT = dict(name="light", card="#F6F8FA", chip="#FFFFFF", edge="#D0D7DE", chipedge="#D8DEE4",
             ink="#1F2328", sub="#57606A", faint="#8C959F", ok="#1A7F37", rim=None, rim_a=0)
DARK  = dict(name="dark", card="#0E141B", chip="#161B22", edge="#30363D", chipedge="#2A313A",
             ink="#E6EDF3", sub="#8B949E", faint="#6E7681", ok="#3FB950", rim="#FFFFFF", rim_a=0.075)

# GitHub'ın resmi rozet adları ve ne için verildiği
MEANING = {
    "pull-shark":          ("Pull Shark",          "birleştirilmiş pull request'ler"),
    "pair-extraordinaire": ("Pair Extraordinaire", "ortak yazarlı commit'ler"),
    "yolo":                ("YOLO",                "incelemesiz birleştirilmiş PR"),
    "quickdraw":           ("Quickdraw",           "beş dakikada kapatılan issue"),
    "starstruck":          ("Starstruck",          "yıldız toplayan repo"),
    "galaxy-brain":        ("Galaxy Brain",        "kabul edilen cevaplar"),
    "public-sponsor":      ("Public Sponsor",      "açık kaynak sponsorluğu"),
    "arctic-code-vault-contributor": ("Arctic Code Vault", "2020 arşiv katkısı"),
}


def fetch():
    req = urllib.request.Request(f"https://github.com/{USER}?tab=achievements", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        html = r.read().decode("utf-8", "replace")
    out, seen = [], set()
    # her <img> ile ondan sonra gelen ilk kademe etiketi (varsa) eşleşir
    for m in re.finditer(r'<img[^>]*src="([^"]+)"[^>]*data-hovercard-url="/users/[^/]+/achievements/([a-z0-9-]+)/detail[^"]*"[^>]*>', html):
        src, slug = m.group(1), m.group(2)
        if slug in seen:
            continue
        seen.add(slug)
        tail = html[m.end(): m.end() + 600]
        t = re.search(r'achievement-tier-label[^>]*>\s*(x\d+)\s*<', tail)
        out.append((slug, src, t.group(1) if t else ""))
    return out


def png_b64(url, size=128):
    """rozet PNG'sini indir, 128px'e küçült (orijinal ~500px, 64px'te gösteriliyor)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
    try:
        import io
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGBA")
        im.thumbnail((size, size), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); raw = buf.getvalue()
    except ImportError:
        pass                                   # PIL yoksa orijinal boyut kalır
    return base64.b64encode(raw).decode()


def build(p, items):
    W = 1000; PAD, GAP = 24, 14
    n = max(1, len(items)); cw = (W - 2*PAD - (n-1)*GAP) / n
    CH = 92; H = PAD + CH + PAD
    o = [f'<rect width="{W}" height="{H}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')
    for i, (slug, b64, tier) in enumerate(items):
        x = PAD + i*(cw + GAP); y = PAD
        name, meaning = MEANING.get(slug, (slug.replace("-", " ").title(), ""))
        t0 = round(i*0.9/12, 4); t1 = round(t0 + 0.06, 4)
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{t0};{t1};0.82;0.88;1" dur="16s" repeatCount="indefinite"/>'
                 f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{CH}" rx="7" fill="{p["chip"]}" stroke="{p["chipedge"]}"/>'
                 f'<image x="{x+16:.1f}" y="{y+14}" width="64" height="64" href="data:image/png;base64,{b64}"/>'
                 f'<text x="{x+96:.1f}" y="{y+38}" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{p["ink"]}">{name}</text>')
        if tier:
            tx = x + 96 + len(name)*8.2 + 10
            o.append(f'<rect x="{tx:.1f}" y="{y+25}" width="{len(tier)*7.5+12:.0f}" height="18" rx="9" fill="{p["ok"]}" fill-opacity="0.14"/>'
                     f'<text x="{tx+6:.1f}" y="{y+38}" font-family="{MONO}" font-size="11" font-weight="700" fill="{p["ok"]}">{tier}</text>')
        o.append(f'<text x="{x+96:.1f}" y="{y+60}" font-family="{SANS}" font-size="12" fill="{p["sub"]}">{meaning}</text>'
                 f'<text x="{x+96:.1f}" y="{y+77}" font-family="{MONO}" font-size="9.5" letter-spacing="1.2" fill="{p["faint"]}">GitHub rozeti</text></g>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')
    label = ", ".join(f"{MEANING.get(s,(s,''))[0]} {t}".strip() for s, _, t in items)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub rozetleri: {label}">'
            f'{"".join(o)}</svg>\n')


def main():
    items = fetch()
    if not items:
        print("rozet bulunamadı — mevcut dosya korunuyor"); return
    data = [(slug, png_b64(src), tier) for slug, src, tier in items]
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        (ROOT / "assets" / f"ach-{p['name']}.svg").write_text(build(p, data), encoding="utf-8")
    print("rozetler yazıldı:", [(s, t or "-") for s, _, t in items])


if __name__ == "__main__":
    main()
