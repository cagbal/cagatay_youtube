# ARKA PLAN SİLİCİ
Resimdeki insanları arka plandan ayırarak arka plan yerine şeffaflık(alfa kanalı) ekleyen çok ufak bir flask ile yazılmış websitesi taslağı. 

# Canlı deneyim
Site şu adreste yayında, isterseniz deneyebilirsiniz. Tabi performans için optimize edilmediği için biraz yavaş çalışıyor.

https://arkaplan-3s77l6k3uq-ew.a.run.app/arka_plan_silici

### Docker ile çalıştırma (En kolay yöntem)
```bash
git clone https://github.com/cagbal/cagatay_youtube
cd cagatay_youtube/arka_plan_silici_flask
docker build --tag arkaplan:test .
docker run --network host arkaplan:test
```
Artık bir web tarayıcıdan http://0.0.0.0:8080/arka_plan_silici adresine gidebilirsiniz.

### Flask ile çalıştırma
```bash
git clone https://github.com/cagbal/cagatay_youtube
cd cagatay_youtube/arka_plan_silici_flask
pip install -r requirements.txt # burada virtual env. kurmanızı tavsiye ederim
FLASK_APP=src/app.py flask run
```
Artık bir web tarayıcıdan http://0.0.0.0:8080/arka_plan_silici adresine gidebilirsiniz.

### Teknolojiler
- Semantic segmentation 

### Kullanılan kütüphaneler ve modeller
- Kütüphaneler ve lisansları için lütfen requirements.txt'ye bakın. 
- Model olarak torchvision modellerinden resnet tabanlı DeepLab3 kullanıyoruz.

# Uyarı
Bu tamamen YouTube kanalım için yaptığım öğrenme içerikli bir uygulamadır. Çıkabilecek hatalardan dolayı sorumlu değilim.