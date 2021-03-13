# referans: https://hackernoon.com/10-common-security-gotchas-in-python-and-how-to-avoid-them-e19fbe265e03
import subprocess 

dosya_adi = input("Dosya adini giriniz:" )

subprocess.call("touch " + dosya_adi, shell=True)