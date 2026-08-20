<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sheet-dark.svg" />
  <img src="assets/sheet-light.svg" width="100%" alt="Ekin Akkaya, platform mühendisi" />
</picture>

<img src="https://img.shields.io/github/last-commit/ekinakkaya0/ekinakkaya0?style=flat-square&label=son%20g%C3%BCncelleme&labelColor=30363D&color=C2410C&display_timestamp=author" alt="" />
<img src="https://komarev.com/ghpvc/?username=ekinakkaya0&label=g%C3%B6r%C3%BCnt%C3%BClenme&color=30363D&style=flat-square" alt="" />
<img src="https://img.shields.io/github/followers/ekinakkaya0?style=flat-square&logo=github&logoColor=C9D1D9&label=takip%C3%A7i&labelColor=30363D&color=30363D" alt="" />

<!-- iletişim rozeti: adresi doldurup yorumdan çıkar
<a href="mailto:ADRES@ornek.com"><img src="https://img.shields.io/badge/e--posta-30363D?style=flat-square&logo=gmail&logoColor=EA4335" alt="e-posta" /></a>
<a href="https://www.linkedin.com/in/KULLANICI"><img src="https://img.shields.io/badge/linkedin-30363D?style=flat-square&logo=linkedin&logoColor=0A66C2" alt="LinkedIn" /></a>
-->

</div>

```
┌─ LEJANT ─────────────────────────────────────────────────────────┐
│                                                                  │
│  ━━━━━   platform        200+ modül, 43 panel, tek kod tabanı    │
│  ─────   jeo-uzamsal     CAD → PostGIS → GeoServer → tarayıcı    │
│  ┄┄┄┄┄   dağıtım         mavi-yeşil geçiş, otomatik geri alma    │
│  ·  ·    entegrasyon     mobil API, SSO, GTFS, görüntü işleme    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-dark.svg" />
  <img src="assets/rule-light.svg" width="100%" alt="" />
</picture>

## Kısaca

Belediyeler için çok kiracılı bir yönetim sistemi yazıyorum. Tek kod tabanı, kurum başına
ayrı veritabanı. Bugün 200'ün üzerinde backend modülü, 43 panel modülü ve 4800 civarı
backend testi var.

İş uygulama katmanında bitmiyor. Sistemin koştuğu makineler, dağıtım hattı, izleme,
yedekler ve sertifikalar da bende.

Son dönemde uğraştıklarım: imar paftasının CAD dosyasından çıkıp tarayıcıda vektör karo
olarak açılması, internete kapalı bir sunucuya USB'yle kurulum, yirmi küsur kiracıya aynı
anda migration, Postfix'in SNI haritasının sertifika yenilemesinden sonra bayat kalması.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-dark.svg" />
  <img src="assets/rule-light.svg" width="100%" alt="" />
</picture>

## Derinlik

Katman başına, gerçekten uğraştığım türden sorunlar:

| Katman | |
|:--|:--|
| **HTTP kenarı** | Mavi-yeşil geçişte ters vekilin yukarı akışını devretmek. Tek dosya olarak bind-mount edilmiş bir yapılandırmanın konteynere hiç inmemesi (bayat inode); `nginx -s reload` bunu kurtarmıyor. |
| **PostgreSQL** | Kiracı rollerinin grant kaybından sonra gelen `permission denied for table`. `pg_restore`'un dolu bir şemaya ekleme yapıp kayıtları ikiye katlaması. Migration'ın bütün aktif kiracılara sırayla uygulanması. |
| **Jeo-uzamsal veri** | Yanlış etiketlenmiş EPSG tanımları, CAD kaynaklı koordinat kayması. `gpkg_extensions` tablosu olmadan GeoServer'ın GeoPackage katmanını hiç görmemesi. SLD ile referans imar yazılımına piksel düzeyinde renk eşleme. |
| **Uygulama** | Kilitsiz seri numarası üretiminin yarış koşulu. Alan adı beyaz listede olmadığı için API eşleyicisinin veriyi sessizce düşürmesi. Mali hesapta kayan noktalı sayının yasak olduğu yerler. |
| **Sistem** | 30 GB'a dayanan bir Next.js derlemesi için takas alanı açmak. Kendi barındırdığım koşucuların topluca kaydının düşmesi. |
| **Posta ve TLS** | Postfix SNI haritasının sertifika yenilemesinden sonra bayat kalması; `postmap -F` olmadan çözülmüyor. Birbirini ezen iki ayrı certbot ağacı. |

## Genişlik

Vatandaş mobil uygulamasının REST API'si, tek oturum açma vekilleri, araç takip
entegrasyonu, GTFS beslemeli rota planlayıcı, görüntü işleme hattını besleyen ayrı bir
FastAPI servisi, S3 uyumlu nesne depolama, yedekleme ve geri yükleme, VPN üzerinden kurum
içi sunucuya bağlanmak, kapalı ağ için USB kurulum paketi, mali muhasebe ve bütçe motoru,
rol-izin matrisi, denetim izi, gerçek zamanlı bildirim.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-dark.svg" />
  <img src="assets/rule-light.svg" width="100%" alt="" />
</picture>

## Yığın

<table>
<tr>
<td valign="middle" width="17%"><b>Sunucu tarafı</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/Node.js-30363D?style=flat-square&labelColor=30363D&logo=nodedotjs&logoColor=5FA04E" alt="Node.js" /> <img src="https://img.shields.io/badge/Express-30363D?style=flat-square&labelColor=30363D&logo=express&logoColor=C9D1D9" alt="Express" /> <img src="https://img.shields.io/badge/Socket.IO-30363D?style=flat-square&labelColor=30363D&logo=socketdotio&logoColor=C9D1D9" alt="Socket.IO" /> <img src="https://img.shields.io/badge/ES_Modules-30363D?style=flat-square&labelColor=30363D" alt="ES Modules" /> <img src="https://img.shields.io/badge/Python-30363D?style=flat-square&labelColor=30363D&logo=python&logoColor=3776AB" alt="Python" /> <img src="https://img.shields.io/badge/FastAPI-30363D?style=flat-square&labelColor=30363D&logo=fastapi&logoColor=009688" alt="FastAPI" /></td>
</tr>
<tr>
<td valign="middle" width="17%"><b>Veri ve şema</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/PostgreSQL-30363D?style=flat-square&labelColor=30363D&logo=postgresql&logoColor=4169E1" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/Sequelize-30363D?style=flat-square&labelColor=30363D&logo=sequelize&logoColor=52B0E7" alt="Sequelize" /> <img src="https://img.shields.io/badge/Migration-30363D?style=flat-square&labelColor=30363D" alt="Migration" /> <img src="https://img.shields.io/badge/Transaction-30363D?style=flat-square&labelColor=30363D" alt="Transaction" /> <img src="https://img.shields.io/badge/Decimal-30363D?style=flat-square&labelColor=30363D" alt="Decimal" /></td>
</tr>
<tr>
<td valign="middle" width="17%"><b>Jeo-uzamsal</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/PostGIS-30363D?style=flat-square&labelColor=30363D&logo=postgresql&logoColor=C2410C" alt="PostGIS" /> <img src="https://img.shields.io/badge/GeoServer-30363D?style=flat-square&labelColor=30363D&logo=osgeo&logoColor=4CAF50" alt="GeoServer" /> <img src="https://img.shields.io/badge/GDAL_%2F_OGR-30363D?style=flat-square&labelColor=30363D&logo=gdal&logoColor=5CAE58" alt="GDAL / OGR" /> <img src="https://img.shields.io/badge/QGIS-30363D?style=flat-square&labelColor=30363D&logo=qgis&logoColor=8BC34A" alt="QGIS" /> <img src="https://img.shields.io/badge/OGC_WMS_%2F_WFS-30363D?style=flat-square&labelColor=30363D" alt="OGC WMS / WFS" /> <img src="https://img.shields.io/badge/Vekt%C3%B6r_karo_%28MVT%29-30363D?style=flat-square&labelColor=30363D" alt="Vektör karo (MVT)" /> <img src="https://img.shields.io/badge/SLD-30363D?style=flat-square&labelColor=30363D" alt="SLD" /> <img src="https://img.shields.io/badge/EPSG_%2F_CRS-30363D?style=flat-square&labelColor=30363D" alt="EPSG / CRS" /> <img src="https://img.shields.io/badge/GeoPackage-30363D?style=flat-square&labelColor=30363D" alt="GeoPackage" /> <img src="https://img.shields.io/badge/OpenLayers-30363D?style=flat-square&labelColor=30363D&logo=openlayers&logoColor=4FC3F7" alt="OpenLayers" /></td>
</tr>
<tr>
<td valign="middle" width="17%"><b>İstemci</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/Next.js-30363D?style=flat-square&labelColor=30363D&logo=nextdotjs&logoColor=C9D1D9" alt="Next.js" /> <img src="https://img.shields.io/badge/React-30363D?style=flat-square&labelColor=30363D&logo=react&logoColor=61DAFB" alt="React" /> <img src="https://img.shields.io/badge/TypeScript-30363D?style=flat-square&labelColor=30363D&logo=typescript&logoColor=3178C6" alt="TypeScript" /> <img src="https://img.shields.io/badge/MUI-30363D?style=flat-square&labelColor=30363D&logo=mui&logoColor=007FFF" alt="MUI" /> <img src="https://img.shields.io/badge/Tailwind-30363D?style=flat-square&labelColor=30363D&logo=tailwindcss&logoColor=06B6D4" alt="Tailwind" /></td>
</tr>
<tr>
<td valign="middle" width="17%"><b>İşletim</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/Docker-30363D?style=flat-square&labelColor=30363D&logo=docker&logoColor=2496ED" alt="Docker" /> <img src="https://img.shields.io/badge/NGINX-30363D?style=flat-square&labelColor=30363D&logo=nginx&logoColor=2ECC71" alt="NGINX" /> <img src="https://img.shields.io/badge/GitHub_Actions-30363D?style=flat-square&labelColor=30363D&logo=githubactions&logoColor=58A6FF" alt="GitHub Actions" /> <img src="https://img.shields.io/badge/Linux-30363D?style=flat-square&labelColor=30363D&logo=linux&logoColor=FCC624" alt="Linux" /> <img src="https://img.shields.io/badge/Ubuntu-30363D?style=flat-square&labelColor=30363D&logo=ubuntu&logoColor=E95420" alt="Ubuntu" /> <img src="https://img.shields.io/badge/MinIO_%2F_S3-30363D?style=flat-square&labelColor=30363D&logo=minio&logoColor=F87171" alt="MinIO / S3" /> <img src="https://img.shields.io/badge/Grafana-30363D?style=flat-square&labelColor=30363D&logo=grafana&logoColor=F46800" alt="Grafana" /> <img src="https://img.shields.io/badge/Sentry_%2F_GlitchTip-30363D?style=flat-square&labelColor=30363D&logo=sentry&logoColor=A78BFA" alt="Sentry / GlitchTip" /> <img src="https://img.shields.io/badge/Postfix_%2F_Dovecot-30363D?style=flat-square&labelColor=30363D" alt="Postfix / Dovecot" /> <img src="https://img.shields.io/badge/Let%27s_Encrypt-30363D?style=flat-square&labelColor=30363D&logo=letsencrypt&logoColor=5EA9E8" alt="Let's Encrypt" /></td>
</tr>
</table>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-dark.svg" />
  <img src="assets/rule-light.svg" width="100%" alt="" />
</picture>

## Yakından

<details>
<summary><b>Çok kiracılı platform</b></summary>

Her kurum kendi PostgreSQL veritabanında duruyor, global yapılandırma ayrı bir master
veritabanında. İstek başlığındaki kiracı kimliği ara katmanda çözülüyor; bağlantı,
modeller ve izinler oradan üretiliyor. Yeni bir belediye eklemek yeni bir sürüm değil,
yeni bir kayıt.

Modüllerin tamamı aynı iskelet üzerinde: model, denetleyici, rota. Yetki sayfa bazında
oku/oluştur/güncelle/sil. Menü ağacı veritabanından üretiliyor ve menü, izin, rota tek bir
kısa ad üzerinden hizalı duruyor.

Para hesapları `Decimal` ile yapılıyor, birden fazla tabloya dokunan iş tek transaction
içinde. Otomatik şema senkronizasyonu kapalı; her değişiklik sürümlenmiş bir migration.
Denetim kanıtı olabilecek kayıt otomatik silinmiyor, arşivleniyor.

</details>

<details>
<summary><b>Jeo-uzamsal hat</b></summary>

CAD ortamında üretilmiş 1/1000 imar planlarını GeoPackage'a çevirip koordinat sistemi ve
karakter kodlaması sorunlarını düzelttikten sonra PostGIS'e taşıdım. Oradan tarayıcıdaki
haritaya kadar hattın tamamı bende.

Yayın GeoServer üzerinden: WMS, WFS ve vektör karo. Stiller SLD ile tanımlı ve stil
kataloğu referans imar yazılımıyla piksel düzeyinde kıyaslanarak eşitlendi. Nizam, ada ve
yapılaşma koşulu katmanları ham veriden türetildi.

Renge göre ayrım gereken katmanlarda stil kararını istemciden alıp sunucuda karoya gömdüm;
ağır katmanlarda istemci yükü belirgin düştü. OpenLayers panelinde 3B bina görselleştirme
var, harita durumu kullanıcı bazında saklanıyor. Görüntüden üretilen kaçak yapı tespitleri
kurumun kendi kayıtlarıyla aynı ekranda.

</details>

<details>
<summary><b>Dağıtım ve işletim</b></summary>

Aday slot hazırlanıyor, migration'lar koşuyor, doğrulama geçerse ters vekilin yukarı akışı
devrediliyor, ardından duman testi. Başarısızlıkta geri alma otomatik. Elle konteyner
yeniden başlatmak yasak; o yol bayat yukarı akış ve 502 demek.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/log-dark.svg" />
  <img src="assets/log-light.svg" width="100%" alt="dağıtım günlüğünden satırlar" />
</picture>

Koşucular kendi barındırdığım makinelerde, imajlar sürümlenip etiketle yayınlanıyor.
İzleme metrik toplayıcıdan alarm kurallarına, oradan anlık bildirime gidiyor; hata takibi
ayrı bir serviste. Gerçek bir veri kaybı olayında üretim veritabanlarını yedekten ayağa
kaldırdım, sonra aynı şeyin tekrarını engelleyen düzeltmeyi hatta ekledim.

İnternete kapalı kurumlar için USB ile taşınan bir kurulum paketi var: tek komutluk
sihirbaz, imajlar ve şema dâhil.

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-dark.svg" />
  <img src="assets/rule-light.svg" width="100%" alt="" />
</picture>

## Nasıl çalışırım

Üretimle ilgili bir şey iddia etmeden önce ölçerim; "muhtemelen öyledir" bir cevap değil.
Denetim kanıtı olabilecek kaydı silmem, arşivlerim. Şema değişikliği elle değil migration
ile gider. Geri dönüşü olmayan işlerde tek gözle yetinmem, biteni bağımsız gözlerle kırmaya
çalışırım. Dağıtımın fark edilmesi gerekmiyor; fark ediliyorsa hatta bir sorun var demektir.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/rule-dark.svg" />
  <img src="assets/rule-light.svg" width="100%" alt="" />
</picture>

<sub>Buradaki açık depolar eski öğrenci çalışmalarım. Güncel iş kurumsal özel depolarda
yürüdüğü için katkı grafiği bu profil hakkında bir şey söylemiyor.</sub>

<!--
  AKTİVİTE BÖLÜMÜ — kapalı. Commit'ler ekinakkaya1@hotmail.com ile atılıyor ama bu adres
  GitHub hesabına doğrulanmış olarak ekli değil, dolayısıyla katkılar hiçbir profile
  yazılmıyor (ölçüm 20.08.2026: son 1 yıl 36 katkı, gizli katkı 0, güncel seri 0).
  Açmak için: (1) Settings > Emails'e o adresi ekle ve doğrula, (2) Settings > Public
  profile > Include private contributions on my profile, (3) yılan/seri kartlarını ekle.
-->
