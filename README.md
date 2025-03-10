# HateSpeechandOffensiveLanguageDetectionInTurkish
Türkçe Hakaret ve Nefret Söylemi Otomatik Tespit Modeli (Offensive Language and Hate Speech Detection in Turkish)

Bu sayfa Veri bilimi dergisinde yayınlanan "Türkçe Hakaret ve Nefret Söylemi Otomatik Tespit Modeli" makalesi ile ilgili kodlamaları ve veri setlerini içermektedir.

[Makalenin linki](https://dergipark.org.tr/en/download/article-file/3157944)


[Veri Setinin linki](https://drive.google.com/drive/folders/1uF_BxmCP6X29hJXapUCbaW65UGYvn09_?usp=sharing)

Makalede oluşturulma süreci ile ilgili ayrıntılı bilgileri verilen Veri Seti Google Drive içerisinde paylaşılmıştır.

* Hakaret ve Nefret Söylemi Eğitim Seti Otomatik Etiketlenmiş
  * Hakaret ve Nefret Söylemi Eğitim Seti (Twitter - Pozitif Örnekler - Otomatik Etiketlenmiş)_1.67M.pk
  * Hakaret ve Nefret Söylemi Eğitim Seti (Wikipedia - Negatif Örnekler - Otomatik Etiketlenmiş)_2.51M.pk
* Hakaret ve Nefret Söylemi Test Seti Otomatik Etiketlenmiş
  * Hakaret ve Nefret Söylemi Test Seti (Twitter - Pozitif Örnekler - Otomatik Etiketlenmiş)_134K.pk
  * Hakaret ve Nefret Söylemi Test Seti (Wikipedia - Negatif Örnekler - Otomatik Etiketlenmiş)_251K.pk

Not: dosyalar pythonda pickle kütüphanesi kullanılarak kaydedilmiştir. Dosyaların yüklenmesi için python kod örneği:
  * import pickle
  * df = pickle.load(open("veri_seti_1.67M.pk",'rb'))

