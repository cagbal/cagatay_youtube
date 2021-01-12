
# Çok güvensiz yeni nesil mesajlaşma programı

# kullanici ekleme: python robotikApp.py --ad ayse --mod olustur
# mesaj gonderme: python robotikApp.py --ad cagatay --mod gonderici --mesaj mesaj --kanal /ortam --acik_anahtar cagatay_acik_anahtar.pem
# mesaj alma: python robotikApp.py --ad cagatay --mod alici --gizli_anahtar cagatay/gizli_anahtar.pem

import argparse
import os 
import base64

import rospy 
from std_msgs.msg import String

import asymcrypt

def arguman_okuyucu():
    okuyucu = argparse.ArgumentParser()
    okuyucu.add_argument("--ad", help="kullanici adi")
    okuyucu.add_argument("--mod", help="gonderici mi alici mi olustur mu?")
    okuyucu.add_argument("--mesaj", help="gonderici mod'u icin gondermek istediğiniz mesaj")
    okuyucu.add_argument("--kanal", default = "ortam", help="kanal adi")
    okuyucu.add_argument("--gizli_anahtar", default = "gizli_anahtar.pem", help ="gizli anahtar dosya adi")
    okuyucu.add_argument("--acik_anahtar", default = "acik_anahtar.pem", help ="acik anahtar dosya adi")
    args = okuyucu.parse_args()
    
    return args 

def mesaj_gonder(kanal, msj, acik_anahtar):
    
    pub = rospy.Publisher(kanal, String, queue_size=1)
    
    rospy.sleep(1)
    
    msj = asymcrypt.encrypt_data(msj, acik_anahtar, out_format='base64') 
    
    pub.publish(msj.decode("utf-8"))
    
    
def mesaj_al(kanal, gizli_anahtar):
    
    while not rospy.is_shutdown():
        msj = rospy.wait_for_message(kanal, String)
        
        veri = msj.data
        
        msj = asymcrypt.decrypt_data(veri, gizli_anahtar, in_format='base64')
    
        print(msj)
        

def kullanici_olustur(ad):
    os.mkdir(ad)
    asymcrypt.generate_keys(ad + '/gizli_anahtar.pem', ad + '_acik_anahtar.pem')
        

def main():
    args = arguman_okuyucu()
    rospy.init_node(args.ad, anonymous=True)
    
    if args.mod == "gonderici":
        mesaj_gonder(args.kanal, args.mesaj, args.acik_anahtar)
    elif args.mod == "alici":
        mesaj_al(args.kanal, args.gizli_anahtar)
    elif args.mod == "olustur":
        kullanici_olustur(args.ad)
    else:
        raise "Cok yanlis arguman cok :("
 
if __name__ == "__main__":
    main()