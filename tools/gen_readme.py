#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""README üreteci. Metin içerikler burada; görseller assets/ altındaki SVG'ler.

Akış: başlık → rozetler → VERİ → yığın → sahne → kısaca → alanlar → uçtan uca
→ derinlik → yakından → nasıl çalışırım → aktivite.
Yapısal bölümler (alanlar, uçtan uca, ilkeler, vurgu) tools/gen_panels.py'den
gelen SVG kartlar; uzun metin (derinlik, yakından) aranabilir kalsın diye markdown.
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
U = "ekinakkaya0"
LINKEDIN = "https://www.linkedin.com/in/ekin-dogucan-akkaya/"
MAIL = "ekinakkaya0@hotmail.com"
VIEWS = f"https://komarev.com/ghpvc/?username={U}&label=g%C3%B6r%C3%BCnt%C3%BClenme&color=30363D&style=flat-square"

def pic(base, alt, width="100%"):
    return ("<picture>\n"
            f'  <source media="(prefers-color-scheme: dark)" srcset="assets/{base}-dark.svg" />\n'
            f'  <img src="assets/{base}-light.svg" width="{width}" alt="{alt}" />\n</picture>')

def pic1(base, alt, extra=""):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{base}-dark.svg" />'
            f'<img src="assets/{base}-light.svg" alt="{alt}"{extra} /></picture>')

_r = [0]
def RULE():
    v = "rule-a" if _r[0] % 2 == 0 else "rule-b"; _r[0] += 1
    return pic(v, "")

def BAND(slug, alt):
    return "## " + pic1(f"h-{slug}", alt, ' width="100%"')

def MARK(title):
    return "## " + pic1("marker", "", ' height="20"') + " " + title

def badge(slug, href, alt):
    b = pic1(f"badge-{slug}", alt, ' height="32"')
    return f'<a href="{href}">{b}</a>' if href else b

KISACA = "Yazılım işlerini uçtan uca alıyorum: keşif görüşmesinden fizibiliteye, mimariden arayüz\ntasarımına, backend ve mobil geliştirmeden sunucuda yayına ve sonrasındaki işletime kadar.\n\nEn büyük işim belediyeler için yazdığım multi-tenant yönetim platformu: tek kod tabanı,\nkurum başına ayrı veritabanı, 200'ün üzerinde backend modülü ve 43 panel modülü. Ama iş\noradan ibaret değil. Tarımsal üretici platformu, fabrikada CNC makine ve stok takibi,\ntekstilde CRM/ERP ile pazaryeri ve ödeme entegrasyonu, restoran işletim sistemi ve dört\nayrı Flutter uygulaması da aynı elden çıktı."

DERIN_INTRO = "Katman başına, gerçekten uğraştığım türden sorunlar:"
DERINLIK = [
 [
  "Reverse proxy",
  "Blue-green deployment'ta nginx upstream'ini devretmek. Tek dosya olarak bind-mount edilmiş bir config'in konteynere hiç inmemesi (stale inode); `nginx -s reload` bunu kurtarmıyor, süreci HUP'lamak gerekiyor."
 ],
 [
  "PostgreSQL",
  "Tenant rollerinin grant kaybından sonra gelen `permission denied for table`. `pg_restore`'un dolu bir şemaya append edip kayıtları ikiye katlaması. Migration'ın bütün aktif tenant'lara sırayla uygulanması."
 ],
 [
  "Geospatial",
  "Yanlış etiketlenmiş EPSG tanımları ve CAD kaynaklı koordinat kayması. `gpkg_extensions` tablosu olmadan GeoServer'ın GeoPackage katmanını hiç görmemesi. SLD ile referans yazılıma piksel düzeyinde renk eşleme, MVT cache'inin sunucuda pişirilmesi."
 ],
 [
  "Uygulama",
  "Kilitsiz seri numarası üretiminde race condition. Alan adı whitelist'te olmadığı için API mapper'ının payload'u sessizce düşürmesi. Mali hesapta floating point'in yasak olduğu yerler."
 ],
 [
  "Mobil",
  "OCR başarısız olunca e-Devlet doğrulamasının kırılması ve başvuru akışının komple durması. Upload'ın 413 dönmesi çünkü isteği alan vhost'ta `client_max_body_size` tanımlı değil."
 ],
 [
  "Sistem",
  "30 GB'a dayanan bir Next.js build'i için swap açmak. Self-hosted runner'ların topluca deregister olması. systemd unit'leri, disk baskısı, arşivleme."
 ],
 [
  "Ağ ve sertifika",
  "Postfix SNI map'inin sertifika yenilemesinden sonra bayat kalması; `postmap -F` olmadan çözülmüyor. Birbirini ezen iki ayrı certbot ağacı."
 ],
 [
  "Olay müdahalesi",
  "Ele geçirilmiş bir sitede forensic çıkarmak. Üretim veritabanlarını yedekten ayağa kaldırmak ve nedeni ortadan kaldıran düzeltmeyi hatta eklemek."
 ]
]

YAKINDAN = [
 "<details>\n<summary><b>Multi-tenant yönetim platformu</b></summary>\n\nHer kurum kendi PostgreSQL veritabanında duruyor, global yapılandırma ayrı bir master\nveritabanında. İstek başlığındaki tenant kimliği bir middleware'de çözülüyor; connection,\nmodeller ve permission'lar oradan üretiliyor. Yeni bir kurum eklemek yeni bir sürüm değil,\nyeni bir kayıt.\n\nModüllerin tamamı aynı iskelet üzerinde: model, controller, route. RBAC sayfa bazında\nread/create/update/delete. Menü ağacı veritabanından üretiliyor ve menü, permission, route\ntek bir slug üzerinden hizalı duruyor.\n\nMali hesaplar `Decimal` ile, birden fazla tabloya dokunan iş tek transaction içinde.\nOtomatik şema senkronizasyonu kapalı; her değişiklik versiyonlanmış bir migration ve aktif\ntenant'ların hepsine sırayla uygulanıyor. Denetim kanıtı olabilecek kayıt otomatik\nsilinmiyor, arşivleniyor.\n\n</details>",
 "<details>\n<summary><b>Geospatial veri hattı</b></summary>\n\nCAD ortamında üretilmiş 1/1000 imar planlarını GeoPackage'a çevirip CRS ve karakter\nkodlaması sorunlarını düzelttikten sonra PostGIS'e taşıdım. Oradan tarayıcıdaki haritaya\nkadar hattın tamamı bende.\n\nYayın GeoServer üzerinden: WMS, WFS ve MVT. Stiller SLD ile tanımlı, stil kataloğu referans\nyazılımla piksel düzeyinde kıyaslanarak eşitlendi. Nizam, ada ve yapılaşma koşulu katmanları\nham veriden türetildi.\n\nRenge göre ayrım gereken katmanlarda stil kararını istemciden alıp sunucuda tile'a gömdüm;\nağır katmanlarda client yükü belirgin düştü. OpenLayers panelinde 3B bina görselleştirme\nvar, harita durumu kullanıcı bazında persist ediliyor. Ayrıca Sentinel-2 altlıkları, parsel\nsorgu ekranı ve görüntüden üretilen tespitlerin kurum kayıtlarıyla aynı ekranda gösterimi.\n\n</details>",
 "<details>\n<summary><b>Yayın ve işletim</b></summary>\n\nCandidate slot hazırlanıyor, migration'lar koşuyor, validation geçerse nginx upstream'i\ndevrediliyor, ardından smoke test. Başarısızlıkta rollback otomatik. Elle konteyner restart\netmek yasak; o yol stale upstream ve 502 demek.\n\n<picture>\n  <source media=\"(prefers-color-scheme: dark)\" srcset=\"assets/log-dark.svg\" />\n  <img src=\"assets/log-light.svg\" width=\"100%\" alt=\"dağıtım günlüğünden satırlar\" />\n</picture>\n\nRunner'lar kendi barındırdığım makinelerde, imajlar versiyonlanıp tag ile yayınlanıyor.\nİzleme metrik toplayıcıdan alert kurallarına, oradan anlık bildirime gidiyor; error tracking\nayrı bir serviste. Hetzner, Turhost, Hostinger ve müşteri sunucusunda on-prem kurulum yaptım;\nDNS, TLS ve mail tarafı da dahil.\n\nİnternete kapalı kurumlar için USB ile taşınan bir kurulum paketi var: tek komutluk sihirbaz,\nimajlar ve şema dâhil.\n\n</details>",
 "<details>\n<summary><b>Belediye dışı işler</b></summary>\n\n**Tarım / agrotech** — Üretici, kooperatif, teknik ekip, sigorta ve denetleyici kurumun aynı\nsüreçte rol aldığı bir platform. QR kodlu ürün izlenebilirliği, arsa-parsel sorgusu üzerinden\ntoprak analizi görüntüleme, karbon ve su ayak izi hesabı, soğuk zincir lojistiği. Mevzuat\ndokümanlarından hesap kurallarını çıkarıp modüle çevirmek de bu işin parçasıydı.\n\n**Sanayi** — Fabrikada stok ve sipariş takibi, siparişin baştan sona kaydı, CNC makine\ndurumlarının izlenmesi. Windows tarafında çalışan bir station agent'ın backend ile\nhaberleşmesi dahil.\n\n**Perakende** — Tekstil firması için CRM/ERP, pazaryeri entegrasyonu ve ödeme sağlayıcı\ntarafında kaybolan siparişin izinin sürülmesi.\n\n**Gastronomi** — Restoran işletim sistemi. Flutter monorepo, garson uygulaması, kasa ve\nmutfak istasyonları.\n\n**Sivil toplum ve kurumsal** — İstihdam platformu (Flutter), kadın platformu, spor kulübü\nsiteleri, bilim merkezi, kamu ihale ve mevzuat modülü.\n\n</details>"
]

AKTIVITE = "<picture>\n  <source media=\"(prefers-color-scheme: dark)\" srcset=\"https://raw.githubusercontent.com/ekinakkaya0/ekinakkaya0/output/github-snake-dark.svg\" />\n  <img src=\"https://raw.githubusercontent.com/ekinakkaya0/ekinakkaya0/output/github-snake.svg\" width=\"100%\" alt=\"katkı grafiğinde dolaşan yılan\" />\n</picture>\n\n<picture>\n  <source media=\"(prefers-color-scheme: dark)\" srcset=\"assets/activity-dark.svg\" />\n  <img src=\"assets/activity-light.svg\" width=\"100%\" alt=\"son bir yılın günlük katkı yoğunluğu\" />\n</picture>\n\n<sub>Yılan katkı ızgarasını dolaşıyor; altındaki panel aynı verinin günlük yoğunluğunu ve\nyıla yayılmış hâlini gösteriyor. İkisi de GitHub'ın genel katkı verisinden, her gün bir\nGitHub Action ile yenileniyor.</sub>"

def build():
    o = []; w = o.append
    w('<div align="center">'); w("")
    w(pic("console", "Ekin Doğucan Akkaya — Full-Stack ve DevOps Engineer, projelendirmeden yayına uçtan uca")); w("")
    w(badge("linkedin", LINKEDIN, "LinkedIn — Ekin Doğucan Akkaya"))
    w(badge("mail", f"mailto:{MAIL}", "e-posta"))
    w(badge("views", None, "görüntülenme"))
    w("")
    w("<!-- Sayaç ancak ziyaretçi komarev görselini çektiğinde artar; rozetteki sayı")
    w("     her gün bir GitHub Action ile buradan okunup gömülüyor. -->")
    w(f'<img src="{VIEWS}" width="1" height="1" alt="" />')
    w(""); w("</div>"); w("")
    w(pic("data", "gerçek GitHub verisi: diller, satırlar, çalışma saati ve haftanın günü")); w("")
    w(RULE()); w("")
    w(BAND("yigin", "Yığın")); w("")
    w(pic("stackband", "kullandığım teknolojiler")); w("")
    w(pic("stack", "teknoloji yığını: 8 kategoride 51 teknoloji")); w("")
    w(RULE()); w("")
    w('<img src="assets/scene.svg" width="100%" alt="ASCII çizim: gece çalışma masası — üç ekran, dizüstü, kahve" />'); w("")
    w(RULE()); w("")
    w(MARK("Kısaca")); w("")
    w(pic("quote", "Keşif görüşmesinden sunucudaki işletime kadar zincirin tamamı bende kalıyor.")); w("")
    w(KISACA); w("")
    w("### Çalıştığım alanlar"); w("")
    w(pic("sectors", "çalıştığım sektörler: kamu, tarım, sanayi, perakende, turizm, spor, sivil toplum, kamu ihale")); w("")
    w(RULE()); w("")
    w(BAND("uctan-uca", "Uçtan uca")); w("")
    w(pic("stages", "teslim zinciri: keşif, fizibilite, mimari, arayüz, geliştirme, veri, yayın, işletim, belgeleme")); w("")
    w(RULE()); w("")
    w(BAND("derinlik", "Derinlik")); w("")
    w(DERIN_INTRO); w("")
    w("| Katman | |"); w("|:--|:--|")
    for a, b in DERINLIK:
        w(f"| {pic1('marker', '', ' height=\"14\"')} **{a}** | {b} |")
    w("")
    w(RULE()); w("")
    w(BAND("yakindan", "Yakından")); w("")
    for d in YAKINDAN:
        w(d); w("")
    w(RULE()); w("")
    w(MARK("Nasıl çalışırım")); w("")
    w(pic("principles", "çalışma ilkeleri: ölç, silme, migration, tek göz yetmez")); w("")
    w(RULE()); w("")
    w(MARK("Aktivite")); w("")
    w(pic("ach", "GitHub rozetleri: Pull Shark, Pair Extraordinaire, YOLO")); w("")
    w(AKTIVITE); w("")
    return "\n".join(o) + "\n"

if __name__ == "__main__":
    out = build()
    (ROOT / "README.md").write_text(out, encoding="utf-8")
    print(f"README yazıldı: {len(out.encode())} bayt, {out.count(chr(10))} satır")
