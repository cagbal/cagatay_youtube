from io import BytesIO
from flask import send_file, request
from PIL import Image

# bunu direkt https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser 
# buradan aldım
def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def imgeyi_al():
    dosya = request.files["imge"]
    imge = Image.open(dosya.stream)
    imge = imge.convert("RGB")
    return imge