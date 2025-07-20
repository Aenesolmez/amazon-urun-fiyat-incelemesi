Bu Kodu Çalıştırmak İçin Yapmanız Gerekenler:
1. Python bilgisayarınızda kurulu olmalı
2. Terminalde şu komutu çalıştırın: pip install requests beautifulsoup4
3. Kodumuzun 11. Satırında bulunan 'göndericininmaili@example.com' yerine mail gönderecek hesabın adresini yazın. 
4. Kodumuzun 12. Satırında bulunan 'güvenlikkodu' yerine kendi güvenlik şifrenizi giriniz [Bir güvenlik şifreniz yok ise gmail için şuradan ekleyebilirsiniz: https://bit.ly/3Ud3jWw]
5. kodumuzun 13. satırında bulunan 'alıcımaili@example.com' yerine gönderilen mailin kime gideceğini yazın
6. kodumuzun 21. Satırında bulunan "cihazınızın bilgileri" kısmına kendi user agentinizi giriniz [User agentinizi bulmak için google'a 'my user agent' yazınız, ilk başta gözükecektir.]

Kodunuzu ilk çalıştırdığınıza ürününüzün linki fiyatıyla beraber alıcıya bir mail gidecektir ve ürünün fiyatında bir değişiklik olduğunda size bildirim atacaktır. 
kodu açık tutmazsanız eğer bu bildirim sağlanamaz. Ürün fiyatını inceleme döngüsü belli bir süre aralığıyla tutuludur 23. satırdan bu süreyi değiştirebilirsiniz.

Eğer Amazon Kullanmıyorsanız şu ayarlarıda değiştirmelisiniz:
77. Satırda bulunan 'productTitle' yerine sitenizde bulunana ürünün isminin id'sini koymalısınız (İncele sayfasından bulabilirsiniz)
81. Satırda ise fiyatınızın bulunduğu class ismini şunun yerine girin 'a-offscreen' (sayfanızı inceleyerek bulabilirsiniz)
