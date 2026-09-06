<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/console-dark.svg" />
  <img src="assets/console-light.svg" width="100%" alt="Ekin Doğucan Akkaya — Full-Stack ve DevOps Engineer, projelendirmeden yayına uçtan uca" />
</picture>

<a href="https://www.linkedin.com/in/ekin-dogucan-akkaya/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badge-linkedin-dark.svg" /><img src="assets/badge-linkedin-light.svg" alt="LinkedIn — Ekin Doğucan Akkaya" height="32" /></picture></a>
<a href="mailto:ekinakkaya0@hotmail.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badge-mail-dark.svg" /><img src="assets/badge-mail-light.svg" alt="e-posta" height="32" /></picture></a>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/badge-views-dark.svg" /><img src="assets/badge-views-light.svg" alt="görüntülenme" height="32" /></picture>

<!-- Sayaç ancak ziyaretçi komarev görselini çektiğinde artar; rozetteki sayı
     her gün bir GitHub Action ile buradan okunup gömülüyor. -->
<img src="https://komarev.com/ghpvc/?username=ekinakkaya0&label=g%C3%B6r%C3%BCnt%C3%BClenme&color=30363D&style=flat-square" width="1" height="1" alt="" />

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/data-dark.svg" />
  <img src="assets/data-light.svg" width="100%" alt="gerçek GitHub verisi: diller, satırlar, çalışma saati ve haftanın günü" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-a-dark.svg" />
  <img src="assets/rule-a-light.svg" width="100%" alt="" />
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/h-yigin-dark.svg" /><img src="assets/h-yigin-light.svg" alt="Yığın" width="100%" /></picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stackband-dark.svg" />
  <img src="assets/stackband-light.svg" width="100%" alt="kullandığım teknolojiler" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg" />
  <img src="assets/stack-light.svg" width="100%" alt="teknoloji yığını: 8 kategoride 51 teknoloji" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-b-dark.svg" />
  <img src="assets/rule-b-light.svg" width="100%" alt="" />
</picture>

<img src="assets/scene.svg" width="100%" alt="ASCII çizim: gece çalışma masası — üç ekran, dizüstü, kahve" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-a-dark.svg" />
  <img src="assets/rule-a-light.svg" width="100%" alt="" />
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="20" /></picture> Kısaca

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/quote-dark.svg" />
  <img src="assets/quote-light.svg" width="100%" alt="Keşif görüşmesinden sunucudaki işletime kadar zincirin tamamı bende kalıyor." />
</picture>

Yazılım işlerini uçtan uca alıyorum: keşif görüşmesinden fizibiliteye, mimariden arayüz
tasarımına, backend ve mobil geliştirmeden sunucuda yayına ve sonrasındaki işletime kadar.

En büyük işim belediyeler için yazdığım multi-tenant yönetim platformu: tek kod tabanı,
kurum başına ayrı veritabanı, 200'ün üzerinde backend modülü ve 43 panel modülü. Ama iş
oradan ibaret değil. Tarımsal üretici platformu, fabrikada CNC makine ve stok takibi,
tekstilde CRM/ERP ile pazaryeri ve ödeme entegrasyonu, restoran işletim sistemi ve dört
ayrı Flutter uygulaması da aynı elden çıktı.

### Çalıştığım alanlar

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sectors-dark.svg" />
  <img src="assets/sectors-light.svg" width="100%" alt="çalıştığım sektörler: kamu, tarım, sanayi, perakende, turizm, spor, sivil toplum, kamu ihale" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-b-dark.svg" />
  <img src="assets/rule-b-light.svg" width="100%" alt="" />
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/h-uctan-uca-dark.svg" /><img src="assets/h-uctan-uca-light.svg" alt="Uçtan uca" width="100%" /></picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stages-dark.svg" />
  <img src="assets/stages-light.svg" width="100%" alt="teslim zinciri: keşif, fizibilite, mimari, arayüz, geliştirme, veri, yayın, işletim, belgeleme" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-a-dark.svg" />
  <img src="assets/rule-a-light.svg" width="100%" alt="" />
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/h-derinlik-dark.svg" /><img src="assets/h-derinlik-light.svg" alt="Derinlik" width="100%" /></picture>

Katman başına, gerçekten uğraştığım türden sorunlar:

| Katman | |
|:--|:--|
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **Reverse proxy** | Blue-green deployment'ta nginx upstream'ini devretmek. Tek dosya olarak bind-mount edilmiş bir config'in konteynere hiç inmemesi (stale inode); `nginx -s reload` bunu kurtarmıyor, süreci HUP'lamak gerekiyor. |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **PostgreSQL** | Tenant rollerinin grant kaybından sonra gelen `permission denied for table`. `pg_restore`'un dolu bir şemaya append edip kayıtları ikiye katlaması. Migration'ın bütün aktif tenant'lara sırayla uygulanması. |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **Geospatial** | Yanlış etiketlenmiş EPSG tanımları ve CAD kaynaklı koordinat kayması. `gpkg_extensions` tablosu olmadan GeoServer'ın GeoPackage katmanını hiç görmemesi. SLD ile referans yazılıma piksel düzeyinde renk eşleme, MVT cache'inin sunucuda pişirilmesi. |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **Uygulama** | Kilitsiz seri numarası üretiminde race condition. Alan adı whitelist'te olmadığı için API mapper'ının payload'u sessizce düşürmesi. Mali hesapta floating point'in yasak olduğu yerler. |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **Mobil** | OCR başarısız olunca e-Devlet doğrulamasının kırılması ve başvuru akışının komple durması. Upload'ın 413 dönmesi çünkü isteği alan vhost'ta `client_max_body_size` tanımlı değil. |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **Sistem** | 30 GB'a dayanan bir Next.js build'i için swap açmak. Self-hosted runner'ların topluca deregister olması. systemd unit'leri, disk baskısı, arşivleme. |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **Ağ ve sertifika** | Postfix SNI map'inin sertifika yenilemesinden sonra bayat kalması; `postmap -F` olmadan çözülmüyor. Birbirini ezen iki ayrı certbot ağacı. |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="14" /></picture> **Olay müdahalesi** | Ele geçirilmiş bir sitede forensic çıkarmak. Üretim veritabanlarını yedekten ayağa kaldırmak ve nedeni ortadan kaldıran düzeltmeyi hatta eklemek. |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-b-dark.svg" />
  <img src="assets/rule-b-light.svg" width="100%" alt="" />
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/h-yakindan-dark.svg" /><img src="assets/h-yakindan-light.svg" alt="Yakından" width="100%" /></picture>

<details>
<summary><b>Multi-tenant yönetim platformu</b></summary>

Her kurum kendi PostgreSQL veritabanında duruyor, global yapılandırma ayrı bir master
veritabanında. İstek başlığındaki tenant kimliği bir middleware'de çözülüyor; connection,
modeller ve permission'lar oradan üretiliyor. Yeni bir kurum eklemek yeni bir sürüm değil,
yeni bir kayıt.

Modüllerin tamamı aynı iskelet üzerinde: model, controller, route. RBAC sayfa bazında
read/create/update/delete. Menü ağacı veritabanından üretiliyor ve menü, permission, route
tek bir slug üzerinden hizalı duruyor.

Mali hesaplar `Decimal` ile, birden fazla tabloya dokunan iş tek transaction içinde.
Otomatik şema senkronizasyonu kapalı; her değişiklik versiyonlanmış bir migration ve aktif
tenant'ların hepsine sırayla uygulanıyor. Denetim kanıtı olabilecek kayıt otomatik
silinmiyor, arşivleniyor.

</details>

<details>
<summary><b>Geospatial veri hattı</b></summary>

CAD ortamında üretilmiş 1/1000 imar planlarını GeoPackage'a çevirip CRS ve karakter
kodlaması sorunlarını düzelttikten sonra PostGIS'e taşıdım. Oradan tarayıcıdaki haritaya
kadar hattın tamamı bende.

Yayın GeoServer üzerinden: WMS, WFS ve MVT. Stiller SLD ile tanımlı, stil kataloğu referans
yazılımla piksel düzeyinde kıyaslanarak eşitlendi. Nizam, ada ve yapılaşma koşulu katmanları
ham veriden türetildi.

Renge göre ayrım gereken katmanlarda stil kararını istemciden alıp sunucuda tile'a gömdüm;
ağır katmanlarda client yükü belirgin düştü. OpenLayers panelinde 3B bina görselleştirme
var, harita durumu kullanıcı bazında persist ediliyor. Ayrıca Sentinel-2 altlıkları, parsel
sorgu ekranı ve görüntüden üretilen tespitlerin kurum kayıtlarıyla aynı ekranda gösterimi.

</details>

<details>
<summary><b>Yayın ve işletim</b></summary>

Candidate slot hazırlanıyor, migration'lar koşuyor, validation geçerse nginx upstream'i
devrediliyor, ardından smoke test. Başarısızlıkta rollback otomatik. Elle konteyner restart
etmek yasak; o yol stale upstream ve 502 demek.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/log-dark.svg" />
  <img src="assets/log-light.svg" width="100%" alt="dağıtım günlüğünden satırlar" />
</picture>

Runner'lar kendi barındırdığım makinelerde, imajlar versiyonlanıp tag ile yayınlanıyor.
İzleme metrik toplayıcıdan alert kurallarına, oradan anlık bildirime gidiyor; error tracking
ayrı bir serviste. Hetzner, Turhost, Hostinger ve müşteri sunucusunda on-prem kurulum yaptım;
DNS, TLS ve mail tarafı da dahil.

İnternete kapalı kurumlar için USB ile taşınan bir kurulum paketi var: tek komutluk sihirbaz,
imajlar ve şema dâhil.

</details>

<details>
<summary><b>Belediye dışı işler</b></summary>

**Tarım / agrotech** — Üretici, kooperatif, teknik ekip, sigorta ve denetleyici kurumun aynı
süreçte rol aldığı bir platform. QR kodlu ürün izlenebilirliği, arsa-parsel sorgusu üzerinden
toprak analizi görüntüleme, karbon ve su ayak izi hesabı, soğuk zincir lojistiği. Mevzuat
dokümanlarından hesap kurallarını çıkarıp modüle çevirmek de bu işin parçasıydı.

**Sanayi** — Fabrikada stok ve sipariş takibi, siparişin baştan sona kaydı, CNC makine
durumlarının izlenmesi. Windows tarafında çalışan bir station agent'ın backend ile
haberleşmesi dahil.

**Perakende** — Tekstil firması için CRM/ERP, pazaryeri entegrasyonu ve ödeme sağlayıcı
tarafında kaybolan siparişin izinin sürülmesi.

**Gastronomi** — Restoran işletim sistemi. Flutter monorepo, garson uygulaması, kasa ve
mutfak istasyonları.

**Sivil toplum ve kurumsal** — İstihdam platformu (Flutter), kadın platformu, spor kulübü
siteleri, bilim merkezi, kamu ihale ve mevzuat modülü.

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-a-dark.svg" />
  <img src="assets/rule-a-light.svg" width="100%" alt="" />
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="20" /></picture> Nasıl çalışırım

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/principles-dark.svg" />
  <img src="assets/principles-light.svg" width="100%" alt="çalışma ilkeleri: ölç, silme, migration, tek göz yetmez" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-b-dark.svg" />
  <img src="assets/rule-b-light.svg" width="100%" alt="" />
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/marker-dark.svg" /><img src="assets/marker-light.svg" alt="" height="20" /></picture> Aktivite

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/ach-dark.svg" />
  <img src="assets/ach-light.svg" width="100%" alt="GitHub rozetleri: Pull Shark, Pair Extraordinaire, YOLO" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ekinakkaya0/ekinakkaya0/output/github-snake-dark.svg" />
  <img src="https://raw.githubusercontent.com/ekinakkaya0/ekinakkaya0/output/github-snake.svg" width="100%" alt="katkı grafiğinde dolaşan yılan" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg" />
  <img src="assets/activity-light.svg" width="100%" alt="son bir yılın günlük katkı yoğunluğu" />
</picture>

<sub>Yılan katkı ızgarasını dolaşıyor; altındaki panel aynı verinin günlük yoğunluğunu ve
yıla yayılmış hâlini gösteriyor. İkisi de GitHub'ın genel katkı verisinden, her gün bir
GitHub Action ile yenileniyor.</sub>

