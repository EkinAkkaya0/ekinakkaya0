<div align="center">

<img src="assets/header.svg" width="100%" alt="Ekin Akkaya — Platform Mühendisi" />

<img src="assets/typing.svg" width="72%" alt="Ne yaptığımın kısa dökümü" />

<img src="https://img.shields.io/github/last-commit/ekinakkaya0/ekinakkaya0?style=flat-square&label=son%20g%C3%BCncelleme&labelColor=0D1117&color=22D3EE&display_timestamp=author" alt="son güncelleme" />
<img src="https://komarev.com/ghpvc/?username=ekinakkaya0&label=g%C3%B6r%C3%BCnt%C3%BClenme&color=6366F1&style=flat-square" alt="görüntülenme" />
<img src="https://img.shields.io/github/followers/ekinakkaya0?style=flat-square&logo=github&logoColor=C9D1D9&label=takip%C3%A7i&labelColor=0D1117&color=A855F7" alt="takipçi" />
<img src="https://img.shields.io/badge/konum-T%C3%BCrkiye-34D399?style=flat-square&labelColor=0D1117" alt="konum" />

<!-- İletişim rozeti eklemek istersen aşağıdakileri doldurup bu yorumdan çıkar:
<a href="mailto:ADRES@ornek.com"><img src="https://img.shields.io/badge/e--posta-161B22?style=flat-square&logo=gmail&logoColor=EA4335" alt="e-posta" /></a>
<a href="https://www.linkedin.com/in/KULLANICI"><img src="https://img.shields.io/badge/linkedin-161B22?style=flat-square&logo=linkedin&logoColor=0A66C2" alt="LinkedIn" /></a>
-->

</div>

```
╭────────────────────────────────────────────────────────────────╮
│                                                                │
│  $ whoami                                                      │
│  ekin akkaya · platform mühendisi                              │
│                                                                │
│  $ ls ~/uretim                                                 │
│  cok-kiracili-platform/     jeo-uzamsal-veri/                  │
│  sifir-kesintili-dagitim/   kapali-ag-kurulum/                 │
│                                                                │
│  $ tail -1 /var/log/deploy.log                                 │
│  promote ok · upstream devredildi · kesinti yok                │
│                                                                │
╰────────────────────────────────────────────────────────────────╯
```

<img src="assets/divider.svg" width="100%" height="4" alt="" />

## Kısaca

Belediyelerin bütün işini tek panelde toplayan bir yönetim sistemi yazıyorum. Kod tek,
her kurum kendi veritabanında duruyor. Şu an 200'ün üzerinde backend modülü ve 43 panel
modülü var.

İş uygulama katmanıyla bitmiyor. Sistemin koştuğu makineler, dağıtım hattı, izleme
zinciri, yedekler ve sertifikalar da bende. Gece bir şey patlarsa aranan kişi benim.

Son dönemde uğraştıklarım kabaca şöyle: imar paftasının CAD dosyasından çıkıp tarayıcıda
vektör karo olarak açılması, internete kapalı bir belediye sunucusuna USB'yle kurulum,
yirmi küsur kiracıya aynı anda migration, Postfix'in SNI haritasının sertifika
yenilemesinden sonra neden bayat kaldığı.

> [!NOTE]
> Buradaki açık depolar eski öğrenci çalışmalarım. Asıl iş kurumsal özel depolarda
> yürüdüğü için katkı grafiği bu profil hakkında pek bir şey söylemiyor.

<img src="assets/divider.svg" width="100%" height="4" alt="" />

## Uzmanlık

Bir konuyu bildiğimi söyleyebilmem için o konunun bozulduğu yeri görmüş olmam gerekiyor.
Aşağıdaki tablo hangi katmanda ne kadar derine indiğimi, uydurma yetkinlik listesiyle
değil kendi çözdüğüm arızalarla anlatıyor.

### Derinlik

| Katman | Elimle çözdüğüm türden sorunlar |
|:--|:--|
| **HTTP kenarı** | Mavi-yeşil geçişte ters vekilin yukarı akışını devretmek. Tek dosya olarak bind-mount edilmiş bir yapılandırmanın konteynere hiç inmemesi (bayat inode) ve `nginx -s reload` ile kurtarılamaması. |
| **PostgreSQL** | Kiracı rollerinin grant kaybından sonra gelen `permission denied for table`. `pg_restore`'un dolu bir şemaya ekleme yapıp kayıtları ikiye katlaması. Migration'ın bütün aktif kiracılara sırayla uygulanması. |
| **Jeo-uzamsal veri** | Yanlış etiketlenmiş EPSG tanımları ve CAD kaynaklı koordinat kayması. `gpkg_extensions` tablosu olmadan GeoServer'ın GeoPackage katmanını hiç görmemesi. SLD ile referans imar yazılımına piksel düzeyinde renk eşleme. |
| **Uygulama** | Kilitsiz seri numarası üretiminin yarış koşulu. Alan adı beyaz listede olmadığı için API eşleyicisinin veriyi sessizce düşürüp `notNull` hatası vermesi. Mali hesapta kayan noktalı sayının yasak olduğu yerler. |
| **Sistem** | 30 GB'a dayanan bir Next.js derlemesi için takas alanı açmak. Kendi barındırdığım koşucuların topluca kaydının düşmesi. systemd birimleri, disk baskısı, arşivleme. |
| **Posta ve TLS** | Postfix SNI haritasının sertifika yenilemesinden sonra bayat kalması ve `postmap -F` olmadan çözülmemesi. Birbirini ezen iki ayrı certbot ağacı. |

### Genişlik

Katman ayırt etmiyorum. Vatandaş mobil uygulamasının REST API'si, tek oturum açma
vekilleri, araç takip entegrasyonu, GTFS beslemeli toplu taşıma rota planlayıcı, görüntü
işleme hattını besleyen ayrı bir FastAPI servisi, S3 uyumlu nesne depolama, yedekleme ve
geri yükleme, VPN üzerinden kurum içi sunucuya bağlanıp on-prem kurulumla uğraşmak,
kapalı ağ için USB kurulum paketi hazırlamak, mali muhasebe ve bütçe motoru, rol-izin
matrisi, denetim izi, gerçek zamanlı bildirim. Hepsi aynı sistemin parçası ve hepsine
bakan aynı kişiyim.

<img src="assets/divider.svg" width="100%" height="4" alt="" />

## Teknoloji Yığını

<table>
<tr>
<td valign="middle" width="26%"><b>Çalışma Zamanı &amp; API Katmanı</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/Node.js-1F2937?style=flat-square&labelColor=1F2937&logo=nodedotjs&logoColor=5FA04E" alt="Node.js" /> <img src="https://img.shields.io/badge/Express-1F2937?style=flat-square&labelColor=1F2937&logo=express&logoColor=E6EDF3" alt="Express" /> <img src="https://img.shields.io/badge/ES_Modules-1F2937?style=flat-square&labelColor=1F2937" alt="ES Modules" /> <img src="https://img.shields.io/badge/Socket.IO-1F2937?style=flat-square&labelColor=1F2937&logo=socketdotio&logoColor=E6EDF3" alt="Socket.IO" /> <img src="https://img.shields.io/badge/REST-1F2937?style=flat-square&labelColor=1F2937" alt="REST" /> <img src="https://img.shields.io/badge/Python-1F2937?style=flat-square&labelColor=1F2937&logo=python&logoColor=3776AB" alt="Python" /> <img src="https://img.shields.io/badge/FastAPI-1F2937?style=flat-square&labelColor=1F2937&logo=fastapi&logoColor=009688" alt="FastAPI" /></td>
</tr>
<tr>
<td valign="middle" width="26%"><b>Kalıcılık &amp; Şema Yönetimi</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/PostgreSQL-1F2937?style=flat-square&labelColor=1F2937&logo=postgresql&logoColor=4169E1" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/Sequelize_ORM-1F2937?style=flat-square&labelColor=1F2937&logo=sequelize&logoColor=52B0E7" alt="Sequelize ORM" /> <img src="https://img.shields.io/badge/Migration_Hatt%C4%B1-1F2937?style=flat-square&labelColor=1F2937" alt="Migration Hattı" /> <img src="https://img.shields.io/badge/Transaction_%2F_ACID-1F2937?style=flat-square&labelColor=1F2937" alt="Transaction / ACID" /> <img src="https://img.shields.io/badge/Decimal_Aritmeti%C4%9Fi-1F2937?style=flat-square&labelColor=1F2937" alt="Decimal Aritmetiği" /> <img src="https://img.shields.io/badge/%C3%87ok_Kirac%C4%B1l%C4%B1_%C4%B0zolasyon-1F2937?style=flat-square&labelColor=1F2937" alt="Çok Kiracılı İzolasyon" /></td>
</tr>
<tr>
<td valign="middle" width="26%"><b>Jeo-uzamsal Veri &amp; Kartografya</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/PostGIS-1F2937?style=flat-square&labelColor=1F2937&logo=postgresql&logoColor=22D3EE" alt="PostGIS" /> <img src="https://img.shields.io/badge/GeoServer-1F2937?style=flat-square&labelColor=1F2937&logo=osgeo&logoColor=4CAF50" alt="GeoServer" /> <img src="https://img.shields.io/badge/GDAL_%2F_OGR-1F2937?style=flat-square&labelColor=1F2937&logo=gdal&logoColor=5CAE58" alt="GDAL / OGR" /> <img src="https://img.shields.io/badge/QGIS-1F2937?style=flat-square&labelColor=1F2937&logo=qgis&logoColor=8BC34A" alt="QGIS" /> <img src="https://img.shields.io/badge/OGC_WMS_%2F_WFS-1F2937?style=flat-square&labelColor=1F2937" alt="OGC WMS / WFS" /> <img src="https://img.shields.io/badge/Vekt%C3%B6r_Karo_%28MVT%29-1F2937?style=flat-square&labelColor=1F2937" alt="Vektör Karo (MVT)" /> <img src="https://img.shields.io/badge/SLD-1F2937?style=flat-square&labelColor=1F2937" alt="SLD" /> <img src="https://img.shields.io/badge/EPSG_%2F_CRS-1F2937?style=flat-square&labelColor=1F2937" alt="EPSG / CRS" /> <img src="https://img.shields.io/badge/GeoPackage-1F2937?style=flat-square&labelColor=1F2937" alt="GeoPackage" /></td>
</tr>
<tr>
<td valign="middle" width="26%"><b>İstemci &amp; Arayüz Katmanı</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/Next.js-1F2937?style=flat-square&labelColor=1F2937&logo=nextdotjs&logoColor=E6EDF3" alt="Next.js" /> <img src="https://img.shields.io/badge/React-1F2937?style=flat-square&labelColor=1F2937&logo=react&logoColor=61DAFB" alt="React" /> <img src="https://img.shields.io/badge/TypeScript-1F2937?style=flat-square&labelColor=1F2937&logo=typescript&logoColor=3178C6" alt="TypeScript" /> <img src="https://img.shields.io/badge/MUI-1F2937?style=flat-square&labelColor=1F2937&logo=mui&logoColor=007FFF" alt="MUI" /> <img src="https://img.shields.io/badge/Tailwind_CSS-1F2937?style=flat-square&labelColor=1F2937&logo=tailwindcss&logoColor=06B6D4" alt="Tailwind CSS" /> <img src="https://img.shields.io/badge/OpenLayers-1F2937?style=flat-square&labelColor=1F2937&logo=openlayers&logoColor=4FC3F7" alt="OpenLayers" /> <img src="https://img.shields.io/badge/Leaflet-1F2937?style=flat-square&labelColor=1F2937&logo=leaflet&logoColor=7CB342" alt="Leaflet" /></td>
</tr>
<tr>
<td valign="middle" width="26%"><b>Dağıtım &amp; Sürüm Yönetimi</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/Docker-1F2937?style=flat-square&labelColor=1F2937&logo=docker&logoColor=2496ED" alt="Docker" /> <img src="https://img.shields.io/badge/GitHub_Actions-1F2937?style=flat-square&labelColor=1F2937&logo=githubactions&logoColor=58A6FF" alt="GitHub Actions" /> <img src="https://img.shields.io/badge/NGINX-1F2937?style=flat-square&labelColor=1F2937&logo=nginx&logoColor=2ECC71" alt="NGINX" /> <img src="https://img.shields.io/badge/Mavi--Ye%C5%9Fil_Ge%C3%A7i%C5%9F-1F2937?style=flat-square&labelColor=1F2937" alt="Mavi-Yeşil Geçiş" /> <img src="https://img.shields.io/badge/GHCR-1F2937?style=flat-square&labelColor=1F2937" alt="GHCR" /> <img src="https://img.shields.io/badge/Kapal%C4%B1_A%C4%9F_Paketleme-1F2937?style=flat-square&labelColor=1F2937" alt="Kapalı Ağ Paketleme" /></td>
</tr>
<tr>
<td valign="middle" width="26%"><b>Gözlemlenebilirlik &amp; Sistem Yönetimi</b></td>
<td valign="middle"><img src="https://img.shields.io/badge/Linux-1F2937?style=flat-square&labelColor=1F2937&logo=linux&logoColor=FCC624" alt="Linux" /> <img src="https://img.shields.io/badge/Ubuntu-1F2937?style=flat-square&labelColor=1F2937&logo=ubuntu&logoColor=E95420" alt="Ubuntu" /> <img src="https://img.shields.io/badge/Grafana-1F2937?style=flat-square&labelColor=1F2937&logo=grafana&logoColor=F46800" alt="Grafana" /> <img src="https://img.shields.io/badge/Sentry_%2F_GlitchTip-1F2937?style=flat-square&labelColor=1F2937&logo=sentry&logoColor=A78BFA" alt="Sentry / GlitchTip" /> <img src="https://img.shields.io/badge/MinIO_%2F_S3-1F2937?style=flat-square&labelColor=1F2937&logo=minio&logoColor=F87171" alt="MinIO / S3" /> <img src="https://img.shields.io/badge/Postfix_%2F_Dovecot-1F2937?style=flat-square&labelColor=1F2937" alt="Postfix / Dovecot" /> <img src="https://img.shields.io/badge/Let%27s_Encrypt-1F2937?style=flat-square&labelColor=1F2937&logo=letsencrypt&logoColor=5EA9E8" alt="Let's Encrypt" /></td>
</tr>
</table>

<img src="assets/divider.svg" width="100%" height="4" alt="" />

## Yakından

<details>
<summary><b>Çok kiracılı platform</b></summary>

Her kurum kendi PostgreSQL veritabanında duruyor, global yapılandırma ayrı bir master
veritabanında. İstek başlığındaki kiracı kimliği ara katmanda çözülüyor; bağlantı,
modeller ve izinler oradan üretiliyor. Yeni bir belediye eklemek yeni bir sürüm değil,
yeni bir kayıt.

- 200'ü aşkın modülün tamamı aynı iskelet üzerinde: model, denetleyici, rota.
- Yetki sayfa bazında oku/oluştur/güncelle/sil. Menü ağacı veritabanından üretiliyor ve
  menü, izin, rota tek bir kısa ad üzerinden hizalı duruyor.
- Para hesapları `Decimal` ile. Birden fazla tabloya dokunan iş tek transaction içinde,
  hata olursa geri alınıyor.
- Otomatik şema senkronizasyonu kapalı. Her değişiklik sürümlenmiş bir migration ve
  aktif kiracıların hepsine sırayla uygulanıyor.
- Denetim kanıtı olabilecek hiçbir kayıt otomatik silinmiyor. Yer sorunu olursa çözüm
  arşivleme ve bölümleme.

</details>

<details>
<summary><b>Jeo-uzamsal hat</b></summary>

CAD ortamında üretilmiş 1/1000 imar planlarını GeoPackage'a çevirip koordinat sistemi ve
karakter kodlaması sorunlarını düzelttikten sonra PostGIS'e taşıdım. Oradan tarayıcıdaki
haritaya kadar hattın tamamı bende.

- GeoServer üzerinden WMS/WFS servisleri ve vektör karo yayını, stiller SLD ile.
- Stil kataloğu referans imar yazılımıyla piksel düzeyinde kıyaslanarak eşitlendi. Nizam,
  ada ve yapılaşma koşulu katmanları ham veriden türetildi.
- Renge göre ayrım gereken katmanlarda stil kararını istemciden alıp sunucuda karoya
  gömdüm. Ağır katmanlarda istemci yükü belirgin düştü.
- OpenLayers panelinde 3B bina görselleştirme var. Harita konumu, açık katmanlar, altlık
  ve filtreler kullanıcı bazında saklanıyor; bir sonraki girişte yerinde duruyor.
- Görüntüden üretilen kaçak yapı tespitleri, kurumun kendi kayıtlarıyla aynı ekranda.

</details>

<details>
<summary><b>Dağıtım ve işletim</b></summary>

Aday slot hazırlanıyor, migration'lar koşuyor, doğrulama geçerse ters vekilin yukarı
akışı devrediliyor, ardından duman testi. Başarısızlıkta geri alma otomatik. Elle
konteyner yeniden başlatmak yasak; o yol bayat yukarı akış ve 502 demek.

- Kendi barındırdığım koşucular, sürümlenmiş imajlar, etiketle tetiklenen yayın.
- Metrik toplayıcıdan alarm kurallarına, oradan anlık bildirime giden bir izleme zinciri.
  Hata takibi ayrı bir serviste, olay müdahale kılavuzları yazılı.
- Gerçek bir veri kaybı olayında üretim veritabanlarını yedekten ayağa kaldırdım, sonra
  aynı şeyin tekrarını engelleyen düzeltmeyi hatta ekledim.
- Sertifika otomasyonu, ters vekil yapılandırması, posta sunucusu ve nesne depolama.
- İnternete kapalı kurumlar için USB ile taşınan kurulum paketi. Tek komutluk sihirbaz,
  imajlar ve şema dâhil, sahada uçtan uca çalıştığı görüldü.

</details>

<details>
<summary><b>Entegrasyon ve yan servisler</b></summary>

- Vatandaş mobil uygulaması için REST API ve gerçek zamanlı bildirim.
- Tek oturum açma vekilleri, araç takip entegrasyonu, haber akışı vekili.
- GTFS beslemeli toplu taşıma rota planlayıcı, üretimde kurulu.
- Görüntü işleme hattını besleyen ayrı bir FastAPI servisi ve dijital kütüphane altyapısı.

</details>

<img src="assets/divider.svg" width="100%" height="4" alt="" />

## Nasıl çalışırım

| | |
|:--|:--|
| **Varsayma, ölç** | Üretimle ilgili her iddiayı canlı sistemden kanıtla doğrularım. "Muhtemelen öyledir" bir cevap değil. |
| **Veri silinmez** | Denetim kanıtı olabilecek kayıt otomatik silinmez. Yer sıkışıyorsa arşivle, bölümle, pasife al. |
| **Tek göz yetmez** | Geri dönüşü olmayan işlerde biten işi bağımsız gözlerle kırmaya çalışırım. Bir kere yedeksiz kaybettiğin şey geri gelmiyor. |
| **Şema değişikliği migration'dır** | Otomatik senkronizasyon yok. Her değişiklik sürümlenmiş, izlenebilir, geri alınabilir. |
| **Kesinti tasarım hatasıdır** | Hat düzgün kurulmuşsa dağıtım fark edilmez. Elle müdahale düzeltme değil, yeni bir arıza kaynağı. |

<img src="assets/divider.svg" width="100%" height="4" alt="" />

<div align="center">

<img src="assets/footer.svg" width="100%" alt="kanıta dayan, ölç, sonra dağıt" />

</div>

<!--
  AKTİVİTE BÖLÜMÜ — kapalı.

  Commit'ler ekinakkaya1@hotmail.com ile atılıyor ama bu adres GitHub hesabına doğrulanmış
  olarak ekli değil, dolayısıyla katkılar hiçbir profile yazılmıyor (ölçüm 20.08.2026:
  son 1 yıl 36 katkı, gizli katkı 0, güncel seri 0). Kartlar sıfır gösterdiği için kapalı.

  Açmak için: (1) Settings > Emails'e o adresi ekle ve doğrula, (2) Settings > Public
  profile > Include private contributions on my profile, (3) aşağıyı yorumdan çıkar.

  <img src="https://github-readme-activity-graph.vercel.app/graph?username=ekinakkaya0&bg_color=0D1117&color=E6EDF3&line=A855F7&point=22D3EE&area=true&area_color=8B5CF6&title_color=22D3EE&hide_border=true&radius=10" width="100%" alt="katkı grafiği" />
  <img src="https://streak-stats.demolab.com?user=ekinakkaya0&locale=tr&hide_border=true&background=0D1117&stroke=1F2937&ring=A855F7&fire=FBBF24&currStreakLabel=22D3EE&sideLabels=E6EDF3&dates=8B949E&sideNums=E6EDF3&currStreakNum=E6EDF3" alt="katkı serisi" />
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ekinakkaya0/ekinakkaya0/output/github-snake-dark.svg" />
    <img src="https://raw.githubusercontent.com/ekinakkaya0/ekinakkaya0/output/github-snake.svg" width="100%" alt="katkı yılanı" />
  </picture>
-->
