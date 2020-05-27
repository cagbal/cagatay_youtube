#!/usr/bin/python3

# pip install tqdm
# pip install colored

from tqdm import tqdm
from time import sleep
from colored import fg, bg, attr

sayilar_str = ["ILK", "IKINCI", "UCUNCU", "DORDUNCU"]

print("\n{}{}NERD POMODOROSUNA HOS GELDINIZ{}\n".format(fg('red'), bg('white'), attr('reset')))

sleep(2)

print("{}{}POMODORO 25 DAKİKA CALISMA + 5 DAKIKA DINLENME SEKLINDE ILERLEYECEK{}\n".format(fg('red'), bg('white'), attr('reset')))

sleep(5)

print("{}{}VE TOPLAMDA 4 SET YAPACAGIZ{}\n".format(fg('red'), bg('white'), attr('reset')))

sleep(5)



print("{}{}HAZIRSAN, BASLIYORUZ{}\n".format(fg('red'), bg('white'), attr('reset')))

sleep(1)

for i in range(3, 0, -1):
    # boyle cok guzel gorunmuyor
    #bastiralacak_str = str("{}{}"+str(i) + "{}\n").format(fg('red'), bg('white'), attr('reset'))
    bastiralacak_str = str(i) + "\n"
    print(bastiralacak_str)
    sleep(1)

for el in sayilar_str:

    print("\n{0}{1} {2} 25 DAKIKALIK ODAKLANMA SURECI{3}\n".format(fg('white'), bg('red'), el, attr('reset') ))

    for char in tqdm(range(1500)):
        sleep(1)

    print("\n{0}{1} {2} 5 DAKIKALIK DINLENME SURECI{3}\n".format(fg('white'), bg('blue'), el, attr('reset') ))

    for char in tqdm(range(300)):
        sleep(1)

print("\nIYI CALISTIN, TEBRIKLER!\n")
