# ASB-Random-LSB-Steganography
Random LSB (Least Significant Bit) steganography algorithm to encrypt any image file with desired message and decrypt back. 

## [TR] Açıklama

### ÖZET

Dijital ortamda her türlü bilgi 1 ve 0 değerlerinde bir bitlik değerler bütünü ile saklanır. Resimler de bu bilgilerle oluşturulur. Piksellerden oluşan ve her bir pikselin değerlerinin de bu şekilde bitler halinde tutulan resimler, aslında çok boyutlu birer matris olduklarından bu verinin boyutunu ve kalitesini istenilen düzeyde tutabilmek için, resmin saklanmasında farklı yöntemler kullanan dosya formatları geliştirilmiştir. Bu yöntemler, veriyi makul boyutlarda saklamayı amaçladığından şifreleme yöntemlerini kullanır ve bu yöntemler kayıplı veya kayıpsız olabilir.
PNG,JPG,TIFF,GIF olarak isimleri kısaltılan formatlar da birer resim dosyası formatıdır. Her birinin kendine has özellikleri ve uygun kullanım alanları vardır.
Her dosya formatı ilk olarak formatın imzası olarak kabul edilen ve kendisine has olan “File Header” bitleri ile başlar. Bilgisayarda bu dosyalar çalıştırılırken hangi formatta olduğunu sistem bu şekilde anlar.
Steganografi, bir bilginin içine başka bir bilgiyi gizlemek olduğundan, dijital resimleri de bir bilgi bütünü kabul edip bu bilginin içine herhangi bir başka bilgiyi gizleyebiliriz. Bu bilgi gizlenirken, okuyucu tarafından hatasız okunabilmesi için belirli bir algoritmaya sadık kalması gereklidir.
Dijital resim üzerinde bilgi gizlemenin birçok farklı yolu vardır. Fakat bu makalede bilginin doğrusal bir yol ile resmin piksel değerlerinin en önemsiz son bitine gizlendiği “Doğrusal LSB Steganografi” incelenecektir.

### 1.	GİRİŞ

#### 1.1	Çalışmanın Amacı

Bu çalışmanın amacı ,dijital ortamda resimlerin nasıl saklandığını, neden farklı resim dosyası formatlarının var olduğunu, GIF,BMP,JPG,TIFF,PNG resim dosya formatlarının çalışma prensiplerini ve bunların aralarındaki farkları açıklamak, dijital bir resme gizli bir bilgi eklemek için kullanılan rastgele LSB steganografi yönteminin nasıl kullanılacağını incelemek ve anlatmaktır.

#### 1.2	Dijital Ortamda Resimler Nasıl Temsil Edilir?

Dijital ortamda bir resmi ayrık olarak pikseller bütünlüğü ile temsil etmek zorundayız. Her bir piksel, kendi değerini temsil eden sıralı bitlerden oluşur. Bunlar ile gri resimlerde gri seviyesi, renkli resimlerde renk kanallarının değeri ve istenilirse şeffaflık değeri belirtilebilir. Bir resim tüm bu bilgilerin tümünün belirli bir formatla bir araya gelmesiyle oluşturulur.
Resmin bilgisayar tarafından uygun şekilde okunup yorumlanması için hangi formatta kaydedildiği bilinmelidir. Bu sebeple her resim dosyasının kodunun başında, o formata özel olarak yazılmış ve dosya hakkında bilgiler içeren “File Header” kısmı bulunur.

#### 1.3	Steganografi Nedir?

Steganografi, eski Yunanca’da “gizlenmiş yazı” anlamına gelen bilgiyi gizleme bilimine verilen isimdir. 
Steganografi her türlü alanda uygulanabileceği gibi çağımızın en önemli unsurlarından biri olan dijital ortamda da steganografi uygulanabilir. Bilginin dijital olarak taşındığı ve saklandığı bu ortamda yazı,resim,ses ve video formatlarındaki bilgilere çeşitli yöntemlerle istenen bilgi gizlice saklanabilir. Bu yöntemlerin uygulanmasında çeşitlilik sonsuz denebilir.

#### 1.4	Dijital Resim Formatlarının Karşılaştırılması ve Değerlendirilmesi

Her bir resim formatının öne çıkan yanları mevcut ve amaca uygun şekilde seçim yapılmalıdır. Resim üzerinde bit seviyesinde çalışmalar yapılıyorsa ya da herhangi bir şekilde resimde hiçbir kayıp ve değişiklik istenmiyorsa kayıpsız sıkıştırma yöntemi sunabilen PNG,BMP,TIFF gibi formatlar kullanılmalıdır. Resimleri saklarken önceliğimiz boyutların küçük olması ise JPG gibi kayıplı sıkıştırma kullanan formatlar uygun olabilir. Bu formatlar özellikle çok fazla resmin saklanması gerektiği durumlarda ya da internet sayfasında resim gösterimi yapıldığı durumlarda sayfanın yükünü azaltmak için iyi bir seçenek olacaktır. 
Dijital resim formatlarına steganografi uygulanmak istenirse, dijital resmin bu işlem sırasında hiçbir şekilde istenilenin dışında değişim geçirmemesi gerekir. Yani resmin içine bilgi gizlendiğinden itibaren resimde hiçbir şekilde kayıp olmamalıdır. Bu sebeple dijital resimlerde steganografi uygulanırken kesinlikle kayıplı sıkıştırma yöntemi kullanan resim formatları tercih edilmemelidir.

#### 2.	METOT VE MATERYAL

Dijital resimler bilgisayar ortamında belli kurallar içeren matrislerdir denebilir. Her bir piksel, gösterdiği değeri temsilen kendisine ait bir sayı tutar. Bu ondalık sayılar, düşük seviye bilgisayar sisteminde 0 ve 1 lerden oluşan bitlerle temsil edilir. 8-bit ile temsil edilen bir piksel 0 ile 255 arası 256 farklı değer alabilir. 
(bit8)2*(bit7)2*(bit6)2*(bit5)2*(bit4)2*(bit3)2*(bit2)2*(bit1)2 = 2^8 = 256		        
Dijital resmin içine bilgi gömmek için bu piksel değerleri manipüle edilir. Bu değerleri belirleyen bitler istenilen kurala göre değiştirilerek içerisine bilgi saklanabilir.
Piksel değerleri resmin ilk halinden uzaklaştıkça bu değerler gürültü olarak algılanmaya başlar. Dijital resim dosyalarında gürültü fazla olursa insan gözü ile fark edilebilir. LSB yöntemi bu bitlerden en değersiz olan bitlere bilgiyi gömüp, dijital resmi ilk halinden olabildiğince az farklılaştırmaya dayanıyor. En değersiz bitteki değişim, değerli bitlerdeki değişime göre ondalık tabanda çok daha az fark yaratır. En anlamsız bitlerin değişmesi ile oluşan gürültü miktarı, anlamlı bitlerin değişmesi ile oluşan gürültü miktarından çok daha azdır.<br>
(MSB değişimi farkı) 11111111 – 01111111 = 255 – 127 = 128<br>
(LSB değişimi farkı)  11111111 – 11111110 = 255 – 254 = 1<br>
Bilginin gömülmesi için ne kadar anlamlı bitlerin kullanılacağı, resmin kapasitesi ve oluşan gürültünün fark edilme oranı arasında bir takas oluşturur. 
Eğer daha fazla anlamlı bit kullanılırsa resme gömülecek bilginin boyunu (bit sayısı) artar fakat bunun karşılığında resim ilk halinden daha farklı olur ve resmin gürültü miktarı da artar.<br>
Değiştirilecek olan bitlerin seçim algoritması, sonuç değerlendirmesinde önemli farklar yaratacağı için, şifrelenecek piksellerin seçiminde farklı teknikler kullanılabilir. Bu teknikler arasından Doğrusal ve Rastgele LSB steganografi algoritmaları incelenecektir.
Dijital ortamda her türlü bilgi 0 ve 1 bitleri ile temsil edilip saklanabilir. Eğer bit tabanında bir yazı bilgisi saklanmak isterse, her bir karakteri temsil eden binary kodu tekil bitler halinde gömülerek saklanabilir. Her bir yazı karakteri için 8-bit binary kodonun bulunduğu bir standart olan ascii tablosundaki karakter karşılıkları kullanılarak her bir yazı karakteri anlaşılır şekilde bit seviyesinde saklanabilir.

#### 2.1	Doğrusal LSB Steganografi

LSB steganografi yönteminin doğrusal kullanılması, bilginin gömüleceği piksellerin okunma sırasının belirli bir doğrultuda doğrusal olarak devam etmesini gerektirir. Mesela bir bilginin, resmin soldan sağa ve aşağıdan yukarı sıralanan piksellerine belirli ve sabit bir aralıkla sırayla gömülmesi doğrusal bir steganografi tekniğidir.
Dijital resimlerde doğrusal LSB steganografi kullanılarak, bilginin her pikselin en anlamsız tek bir bitine saklandığı bir yöntem için algoritma şu şekildedir:
Gönderici Tarafından:<br>
Adım 1: Bilgi gömülecek resmin kapasitesi tespit edilir.<br>
Adım 2: Bu kapasiteden daha küçük boyutta bilgi, resme gömülmek üzere işleme alınır.<br>
Adım 3: Bilgi eğer karakter halinde ise, ascii tablosundaki binary karşılığı kullanılarak binary formatına çevrilir.<br>
Adım 4: Her bir karakterin binary karşılığını oluşturan bitler, gömülecek mesaja uygun biçimde sıralanır.<br>
Adım 5: Sıralanan bitler, resmin sol üst noktasından başlayıp doğrusal olarak ilerleyerek ele alınan tüm piksellerin değerlerinin en anlamsız biti ile birer birer yer değiştirir.<br>
Adım 6: Bilgiyi gömme işlemi tamamlanınca, yeni oluşturulan resim, toplam gömülü bit sayısını temsil eden bir anahtar ile alıcıya yollanır.<br>
Alıcı Tarafından:<br>
Adım 1: Gönderici tarafından yollanan anahtar yardımıyla, resme gömülü kaç adet bit olduğu belirlenir.<br>
Adım 2: Resmin sol üst köşesinden başlayarak, doğrusal olarak her bir pikselin en anlamsız biti saklanır. Bu işlem gömülen bilginin uzunluğu kadar devam eder.<br>
Adım 3: Saklanan tüm bitler ascii tablosunda bir karakter için gerekli bit sayısı kadar uzun gruplara ayrılır ve her grup, bir karakteri temsil eden binary kodu olarak sayılıp ascii tablosunda karşılık geldiği karakter bulunur. Bu sayede gömülü metin çıkarılıp çözülmüş olur.<br>

#### 2.2	Rastgele LSB Steganografi

Şifrelenecek pikselleri belirleyen algoritmanın istenildiğinde farklı şekilde rastgele pikseller seçebilmesini sağlamak için, verici tarafından belirlenen ve vericiye iletilmesi gereken, rastgele piksel seçimi yapan algoritma için bir başlangıç değeri oluşturacak olan bir anahtar değer kullanılabilir. Bu anahtar değer, üçüncül kişilerin eline geçse dahi çalıştırılacak algoritma bilinmediği taktirde gizlenmek istenen mesaj üçüncül kişiler tarafından bulunamaz. 
Anahtar değer belirlendiği taktirde, şifrenin gizlenmesi için seçilen rastgele bir pikselin konumu mod işlemi sayesinde belirli bir aralıkta tahmin edilemeyen değerler üreten bir algoritma ile bulunabilir ve şifre gömülmesi istenen piksel sayısı kadar tekrar ettirilebilir. Bu algoritma tersine mühendislik ile çözülmesinin zor olması gerekçesiyle üstel ve logaritmik işlemler içeren karmaşık bir algoritma olmalıdır. Bu tarz bir algoritmaya örnek olarak aşağıdaki işlem sırası gösterilebilir :<br>
x1 = (anahtar2)+(2*anahtar)+1997<br>
x2 = x1 + log2(anahtar)<br>
x3 = x2 + log5(x2)<br>
x4 = x3 + anahtar2<br> 
x5 = log10(x4)<br>
x6 = x42 + x5<br>
x7 = x6 + resim_boyu + resim_eni<br>
y = x7 % (resim_boyu*resim_eni)<br>
piksel_sıra_numarası = y<br>
(piksel_sıra_numarası == daha önce bulunan piksel_sıra_numarası) olduğu sürece{piksel_sıra_numarası = piksel_sıra_numarası + 1 }<br>
piksel_konum_Y = piksel_sıra_numarası / resim_boyu<br>
piksel_konum_X = piksel_sıra_numarası % resim_eni<br>
Dijital resimlerde doğrusal LSB steganografi kullanılarak, bilginin her pikselin en anlamsız tek bir bitine saklandığı bir yöntem için adımlar şu şekildedir:
Gönderici tarafından :<br>
Adım 1: Bilgi gömülecek resmin kapasitesi tespit edilir.<br>
Adım 2: Bu kapasiteden daha küçük boyutta bilgi, resme gömülmek üzere işleme alınır.<br>
Adım 3: Bilgi eğer karakter halinde ise, ascii tablosundaki binary karşılığı kullanılarak binary formatına çevrilir.<br>
Adım 4: Her bir karakterin binary karşılığını oluşturan bitler, gömülecek mesaja uygun biçimde sıralanır.<br>
Adım 5: Rastgele piksel seçimi yapan algoritma, belirli bir başlangıç değeri ile gömülmesi gereken bilginin bit uzunluğu kadar çalıştırılır ve bilginin temsil edildiği toplam bit sayısı kadar farklı piksel konumları belirlenir.<br>
Adım 6: Belirlenen piksel konumlarında bulunan piksellerin en anlamsız bitine (LSB) sırası ile gömülecek mesaj bitleri yazılır.<br>
Adım 7: Alıcıya gönderilmek üzere değiştirilen stego resim ile birlikte mesajın uzunluğunu ve mesajın gömüldüğü piksellerin konumunun belirlenmesi için rastgele piksel seçim algoritmasına başlangıç noktası sağlayacak sayısal değeri içeren anahtar değeri yollanır.<br>
Alıcı Tarafından:<br>
Adım 1: Gönderici tarafından yollanan anahtardan rastgele piksel seçim algoritması için başlangıç değeri ve gömülü mesajın bit uzunluğu bilgileri edinilir.<br>
Adım 2: Rastgele piksel seçim algoritması, anahtardan elde edilen değer ile başlatılarak gerekli bit sayısı kadar çalıştırılır ve mesajın hangi piksel koordinatlarında gömülü olduğu belirlenir.<br>
Adım 3: Belirlenen piksellerin hepsinin en anlamsız biti (LSB) sırası ile kaydedilir.<br>
Adım 4: Sıralı olarak kaydedilen mesaj bitleri, ascii tablosundaki kurala göre birleştirilerek yazı karakterlerine dönüştürülür. Bu işlemlerden sonra resme gömülen mesaj ortaya çıkar.<br>

#### 3.	DEĞERLENDİRME

Örnek olarak uygulamada hedef resim dosyası olarak 512x512 piksel boyutlarında lena.bmp kullanılmıştır.
Bu resmin kapasite (512*512)/8 = 32768 Byte = 32 kiloByte olarak belirlenmiştir. 
Örnekte kullanılacak olan yazılım, gömülecek mesajı belirtirken en fazla 37449 karakter yazmaya izin vermektedir.
Steganografi işleminden sonra resim kalitesi ölçümünde kullanılacak olan değerler ve förmülleri :
-Mean Square Error (MSE), resmin ilk ve son (bilgi gömülmüş) hali arasındaki farkı oranlayan bir ölçüdür.Gömülen mesaj boyutu arttıkça MSE oranının da artması beklenir. 
-Peak Signal-to-noise Ratio (PSNR), resimdeki gürültü oranını veren bir ölçüdür.
-Structure Similarity Index Measure (SSIM), iki resim arasındaki benzerlik oranını veren bir ölçüdür.


 

 

 


