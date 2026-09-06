#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Düzyazı panelleri: yapısal bölümleri tasarlanmış kartlara çevirir.

Uzun metin (Derinlik tablosu, Yakından bölümleri) markdown olarak kalır —
SVG içinde sarılmaz, aranmaz, seçilmez. Buraya yalnızca kısa ve yapısal
olanlar gelir: teslim zinciri, sektörler, çalışma ilkeleri, bir vurgu cümlesi.

Tipografi: gövde sistem sans-serif'i, etiket ve numaralar mono.
Hareket ölçülü: kartlar sırayla belirir, uzun süre durur, sönüp baştan başlar.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans',sans-serif"

LIGHT = dict(name="light", card="#F6F8FA", chip="#FFFFFF", edge="#D0D7DE", chipedge="#D8DEE4",
             ink="#1F2328", sub="#57606A", faint="#8C959F", ok="#1A7F37", rim=None, rim_a=0)
DARK  = dict(name="dark", card="#0E141B", chip="#161B22", edge="#30363D", chipedge="#2A313A",
             ink="#E6EDF3", sub="#8B949E", faint="#6E7681", ok="#3FB950", rim="#FFFFFF", rim_a=0.075)

W = 1000
PAD = 24
GAP = 14
CYC, IN, HOLD = 16.0, 3.0, 10.5

STAGES = [
 ("Keşif ve kapsam", "Kurumla oturup ihtiyacı çıkarmak, mevcut sistemi incelemek, kapsamı yazıya dökmek."),
 ("Fizibilite ve teklif", "Sunucu altyapısı ve maliyet hesabı, teknik ön araştırma raporu, hibe ve ihale başvuru dosyası, fiyat teklifi."),
 ("Mimari", "Veri modeli, API sözleşmesi, yetki matrisi, entegrasyon sınırları; monorepo mu ayrı servis mi kararı."),
 ("Arayüz", "Mockup'tan üretime. Tasarım dili, responsive davranış, bileşen kütüphanesi."),
 ("Geliştirme", "Backend, frontend ve mobil. Node ve Express, FastAPI, Next.js, Flutter."),
 ("Veri", "Şema tasarımı, migration hattı, PostGIS, raporlama ve toplu veri aktarımı."),
 ("Yayın", "Docker, GitHub Actions, blue-green deployment, nginx, TLS, DNS. Hetzner, Turhost, Hostinger ve on-prem."),
 ("İşletim", "İzleme ve alarm, yedekleme ve restore, olay müdahalesi, kapasite ve maliyet takibi."),
 ("Belgeleme", "Kullanım kılavuzu, runbook, teknik olmayan anlatım, satış sunumu."),
]
SECTORS = [
 ("kamu / belediye", "multi-tenant yönetim platformu, CBS, vatandaş mobil"),
 ("tarım / agrotech", "üretici platformu, QR izlenebilirlik, toprak analizi"),
 ("sanayi / üretim", "stok ve sipariş takibi, CNC makine izleme"),
 ("perakende", "CRM/ERP, pazaryeri ve ödeme entegrasyonu"),
 ("turizm / gastronomi", "restoran işletim sistemi, otel, garson uygulaması"),
 ("spor kulüpleri", "kurumsal site, üyelik, içerik yönetimi"),
 ("sivil toplum", "istihdam platformu, kadın platformu, bilim merkezi"),
 ("kamu ihale / mevzuat", "mevzuat ve teklif modülü"),
]
PRINCIPLES = [
 ("ölç", "Üretimle ilgili bir şey iddia etmeden önce ölçerim. \"Muhtemelen öyledir\" bir cevap değil."),
 ("silme", "Denetim kanıtı olabilecek kaydı silmem, arşivlerim. Yer sıkışıyorsa bölümle, pasife al."),
 ("migration", "Şema değişikliği elle değil migration ile gider: sürümlenmiş, izlenebilir, geri alınabilir."),
 ("tek göz yetmez", "Geri dönüşü olmayan işlerde biten işi bağımsız gözlerle kırmaya çalışırım. Dağıtım fark ediliyorsa hatta bir sorun var demektir."),
]
QUOTE = ("Keşif görüşmesinden sunucudaki işletime kadar zincirin tamamı bende kalıyor.",
         "Arada kimseye devretmem gerekmiyor.")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def wrap(text, max_px, fs, factor=0.53):
    """sans-serif için kaba sarma: ortalama karakter genişliği fs*factor."""
    cw = fs * factor
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        cand = (cur + " " + w_).strip()
        if len(cand) * cw > max_px and cur:
            lines.append(cur); cur = w_
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def reveal(i, n):
    """i. kartın belirme/sönme zaman çizelgesi (opacity + hafif yükselme)"""
    t = IN * (i / max(1, n))
    k0 = round(t / CYC, 5); k1 = round((t + 0.7) / CYC, 5)
    k2 = round((IN + HOLD) / CYC, 5); k3 = round((IN + HOLD + 0.6) / CYC, 5)
    return (f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{k0};{k1};{k2};{k3};1" '
            f'dur="{CYC}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 8;0 8;0 0;0 0;0 8;0 8" '
            f'keyTimes="0;{k0};{k1};{k2};{k3};1" dur="{CYC}s" repeatCount="indefinite"/>')


def panel(p, h, body, label):
    o = [f'<rect width="{W}" height="{h}" rx="6" fill="{p["card"]}"/>']
    if p["rim"]:
        o.append(f'<path d="M7,1.2 H{W-7}" stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width="1.2" fill="none"/>')
    o.append(body)
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="6" fill="none" stroke="{p["edge"]}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
            f'role="img" aria-label="{esc(label)}">{"".join(o)}</svg>\n')


def card(p, x, y, w, h, i, n, head_mono, head_sans, lines, fs=12.0, lh=16.0):
    o = [f'<g opacity="0">{reveal(i, n)}',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{p["chip"]}" stroke="{p["chipedge"]}"/>',
         f'<rect x="{x+12}" y="{y+14}" width="3" height="16" rx="1.5" fill="{p["ok"]}"/>']
    tx = x + 24
    if head_mono:
        o.append(f'<text x="{tx}" y="{y+27}" font-family="{MONO}" font-size="10" letter-spacing="1.6" fill="{p["faint"]}">{esc(head_mono)}</text>')
        tx += (len(head_mono) * 10 * 0.6005) + (len(head_mono) * 1.6) + 10
    if head_sans:
        o.append(f'<text x="{tx}" y="{y+27}" font-family="{SANS}" font-size="13.5" font-weight="600" fill="{p["ink"]}">{esc(head_sans)}</text>')
    for k, ln in enumerate(lines):
        o.append(f'<text x="{x+24}" y="{y+50+k*lh}" font-family="{SANS}" font-size="{fs}" fill="{p["sub"]}">{esc(ln)}</text>')
    o.append('</g>')
    return "".join(o)


def stages(p):
    cols, cw = 3, (W - 2*PAD - 2*GAP) / 3
    lines = [wrap(d, cw - 48, 12.0) for _, d in STAGES]
    ch = 50 + 3*16 + 14
    rows = (len(STAGES) + cols - 1) // cols
    H = PAD + rows*ch + (rows-1)*GAP + PAD
    o = []
    for i, (t, d) in enumerate(STAGES):
        r, c = divmod(i, cols)
        x = PAD + c*(cw + GAP); y = PAD + r*(ch + GAP)
        o.append(card(p, x, y, cw, ch, i, len(STAGES), f"{i+1:02d}", t, lines[i]))
    return panel(p, H, "".join(o), "Uçtan uca: " + ", ".join(t for t, _ in STAGES))


def sectors(p):
    cols, cw = 4, (W - 2*PAD - 3*GAP) / 4
    lines = [wrap(d, cw - 48, 11.5) for _, d in SECTORS]
    ch = 50 + 2*15 + 12
    rows = 2
    H = PAD + rows*ch + GAP + PAD
    o = []
    for i, (s, d) in enumerate(SECTORS):
        r, c = divmod(i, cols)
        x = PAD + c*(cw + GAP); y = PAD + r*(ch + GAP)
        o.append(card(p, x, y, cw, ch, i, len(SECTORS), None, s, lines[i][:2], fs=11.5, lh=15.0))
    return panel(p, H, "".join(o), "Çalıştığım alanlar: " + ", ".join(s for s, _ in SECTORS))


def principles(p):
    cols, cw = 2, (W - 2*PAD - GAP) / 2
    lines = [wrap(d, cw - 48, 12.5) for _, d in PRINCIPLES]
    ch = 50 + 3*17 + 10
    H = PAD + 2*ch + GAP + PAD
    o = []
    for i, (t, d) in enumerate(PRINCIPLES):
        r, c = divmod(i, cols)
        x = PAD + c*(cw + GAP); y = PAD + r*(ch + GAP)
        o.append(card(p, x, y, cw, ch, i, len(PRINCIPLES), f"{i+1:02d}", t, lines[i][:3], fs=12.5, lh=17.0))
    return panel(p, H, "".join(o), "Nasıl çalışırım: " + "; ".join(d for _, d in PRINCIPLES))


def quote(p):
    H = 104
    a, b = QUOTE
    o = [f'<rect x="{PAD}" y="26" width="4" height="52" rx="2" fill="{p["ok"]}">'
         f'<animate attributeName="opacity" values="0.55;1;0.55" dur="5s" repeatCount="indefinite"/></rect>',
         f'<text x="{PAD+22}" y="52" font-family="{SANS}" font-size="19" font-weight="600" fill="{p["ink"]}">{esc(a)}</text>',
         f'<text x="{PAD+22}" y="78" font-family="{SANS}" font-size="13.5" fill="{p["sub"]}">{esc(b)}</text>',
         # cümlenin altında yavaşça çizilen ince çizgi
         f'<rect x="{PAD+22}" y="60" width="0" height="1.5" rx="0.75" fill="{p["ok"]}" opacity="0.6">'
         f'<animate attributeName="width" values="0;0;{len(a)*19*0.53:.0f};{len(a)*19*0.53:.0f};0" '
         f'keyTimes="0;0.05;0.35;0.9;1" dur="14s" repeatCount="indefinite"/></rect>']
    return panel(p, H, "".join(o), a + " " + b)


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    for p in (LIGHT, DARK):
        for name, fn in (("stages", stages), ("sectors", sectors), ("principles", principles), ("quote", quote)):
            (ROOT / "assets" / f"{name}-{p['name']}.svg").write_text(fn(p), encoding="utf-8")
    print("4 panel x 2 tema yazıldı: stages, sectors, principles, quote")


if __name__ == "__main__":
    main()
