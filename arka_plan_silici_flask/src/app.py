from flask import Flask, request, jsonify

from imge_isleme import imge_isleme

import araclar 

app = Flask(__name__)

@app.route('/arka_plan_silici/sil', methods=['POST'])
def arka_plan_silici_sil():
    try:
        imge = araclar.imgeyi_al()
        arka_plan_silici = imge_isleme.ArkaPlanSilici()
        
        imge = arka_plan_silici.sil(imge)
        
        return araclar.serve_pil_image(imge)
    except Exception as e:
        print("*********", e)
        return jsonify({"hata": "bir sorun oldu ama ne oldu ki?"})

@app.route('/arka_plan_silici', methods=['GET'])
def arka_plan_silici_gui():
    return """
        <h1>Robotikçi arkaplan silici</h1>
        Tamamen denemelik bir websitesidir. Çok ciddiye almayın. <br>
        Model hazır kullanıldığı için insanları algılamada sorunlar çıkabilir. <br>
        Çıkan sorunlardan beni sorumlu tutmayın lütfen.  <br>
        Böyle daha fazla içerik için: <a href="https://www.youtube.com/channel/UCKmkhXwZyrmXnxaCyBXJ-Pw">https://www.youtube.com/channel/UCKmkhXwZyrmXnxaCyBXJ-Pw</a>
        <form action="/arka_plan_silici/sil" method="post" id="form" enctype="multipart/form-data">
            <label for="imge">Arka planını silmek istediğiniz jpeg veya png resmi seçin:</label>
            <br><br>
            <input type="file" name="imge" accept="image/x-png,image/jpeg"/>
            <br><br>
            <input type="submit" value="Gönder gelsin">
        </form>
    
    """
    