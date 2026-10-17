# Değişken sözlüğü

Bu dosya `data/` klasöründeki üç veri setinin değişkenlerini tanımlar. Bütün veriler bilgisayar benzetimiyle üretilmiştir; gerçek kişilere ait değildir. Hiçbir veri setinde kayıp değer yoktur.

Ölçme düzeyleri SPSS'teki tanımlarla aynıdır: *nominal* (sınıflama), *ordinal* (sıralama), *scale* (aralık/oran).


## `ogrenci` (120 gözlem, 17 değişken)

Bir üniversitede *Veri Analizi* dersini alan 120 öğrencinin kurgusal verisi. Öğrenciler üç öğretim yöntemine ve iki şubeye dengeli biçimde dağılmıştır (her yöntem–şube hücresinde 20 öğrenci). 57 numaralı öğrenci, kitap boyunca aykırı gözlem örneği olarak kullanılan, bilerek yerleştirilmiş bir uç değerdir.


| Değişken | Etiket | Ölçme düzeyi | Değer kodları / aralık |
|---|---|---|---|
| `id` | Öğrenci numarası | nominal | 1–120 |
| `cinsiyet` | Cinsiyet | nominal | 1 = Kadın, 2 = Erkek |
| `yas` | Yaş (yıl) | scale | 19–25 |
| `yontem` | Öğretim yöntemi | nominal | 1 = Geleneksel, 2 = Proje tabanlı, 3 = Çevrim içi |
| `sube` | Şube | nominal | 1 = Birinci öğretim, 2 = İkinci öğretim |
| `calisma` | Haftalık çalışma süresi (saat) | scale | 0–15 |
| `devamsizlik` | Devamsızlık (hafta) | scale | 0–7 |
| `kaygi` | Sınav kaygısı puanı (20-80) | scale | 27–80 |
| `on_test` | Dönem başı başarı testi | scale | 16–68 |
| `son_test` | Dönem sonu başarı testi | scale | 23–89 |
| `vize` | Ara sınav notu | scale | 26–86 |
| `final` | Final sınavı notu | scale | 15–85 |
| `proje` | Proje notu | scale | 27–84 |
| `donem_notu` | Dönem notu (0,4 vize + 0,6 final) | scale | 20,6–83 |
| `gecti` | Dersi geçme durumu | nominal | 0 = Kaldı, 1 = Geçti |
| `basari` | Başarı düzeyi | ordinal | 1 = Düşük, 2 = Orta, 3 = Yüksek |
| `tercih` | Mezuniyet sonrası tercih | nominal | 1 = İş, 2 = Yüksek lisans, 3 = Kararsız |

## `kaygi_tekrar` (12 gözlem, 4 değişken)

Bir kaygı azaltma programına katılan 12 kişinin program öncesinde, birinci ayda ve üçüncü ayda ölçülen kaygı puanları (tekrarlı ölçümler deseni).


| Değişken | Etiket | Ölçme düzeyi | Değer kodları / aralık |
|---|---|---|---|
| `katilimci` | Katılımcı | nominal | 1–12 |
| `olcum1` | Program öncesi kaygı | scale | 40–68 |
| `olcum2` | 1. ay kaygı | scale | 38–66 |
| `olcum3` | 3. ay kaygı | scale | 31–69 |

## `tutum_olcegi` (300 gözlem, 13 değişken)

300 öğrencinin 12 maddelik istatistiğe yönelik tutum ölçeğine verdiği yanıtlar (5'li Likert). Maddeler üç alt boyutu temsil edecek biçimde üretilmiştir: kaygı (m1–m4), ilgi (m5–m8) ve öz-yeterlik (m9–m12).


| Değişken | Etiket | Ölçme düzeyi | Değer kodları / aralık |
|---|---|---|---|
| `katilimci` | Katılımcı | nominal | 1–300 |
| `m1` | İstatistik sınavlarından önce gerginlik hissederim. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m2` | İstatistik formüllerini görünce zihnim bulanıklaşır. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m3` | İstatistik dersinde soru sormaktan çekinirim. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m4` | Bir analiz sonucunu yorumlamam gerektiğinde endişelenirim. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m5` | İstatistiğin günlük hayattaki kullanımı ilgimi çeker. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m6` | Yeni bir analiz yöntemi öğrenmekten keyif alırım. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m7` | Veriyle ilgili haberleri merakla okurum. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m8` | Ders dışında da istatistikle ilgili içerikleri incelerim. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m9` | Bir veri setini SPSS'te kendi başıma çözümleyebilirim. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m10` | Uygun istatistiksel testi seçebileceğime inanırım. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m11` | Analiz çıktısındaki temel değerleri doğru okuyabilirim. | ordinal | 1–5 (Likert, aşağıya bakınız) |
| `m12` | Karşılaştığım istatistik problemlerini çözebilirim. | ordinal | 1–5 (Likert, aşağıya bakınız) |

Likert kodları: 1 = Kesinlikle katılmıyorum, 2 = Katılmıyorum, 3 = Kararsızım, 4 = Katılıyorum, 5 = Kesinlikle katılıyorum.

