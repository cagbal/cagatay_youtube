#!/usr/bin/python

import boto3

def duygu_bul(cumle_turkce, cevirici, dil_isleyici):
    cevrim_sonucu = cevirici.translate_text(Text=cumle_turkce,
                SourceLanguageCode="tr", TargetLanguageCode="en")

    cevrilmis_cumle = cevrim_sonucu['TranslatedText']

    duygu_sonucu = dil_isleyici.detect_sentiment(
        Text=cevrilmis_cumle,
        LanguageCode='en'
    )

    return duygu_sonucu, cevrilmis_cumle

def duygu_sonucu_gorsellestir(duygu_sonucu):
    pozitif_duygu_skoru = duygu_sonucu['SentimentScore']['Positive']
    negatif_duygu_skoru = duygu_sonucu['SentimentScore']['Negative'] 
    notr_duygu_skoru = duygu_sonucu['SentimentScore']['Neutral']
    
    duygu = ""

    if duygu_sonucu['Sentiment'] == "POSITIVE": 
        duygu = "iyi :)"
    elif duygu_sonucu['Sentiment'] == "NEGATIVE":
        duygu = "kotu :("
    elif duygu_sonucu['Sentiment'] == "NEUTRAL":
        duygu = "ne iyi ne kotu"

    print("\n-----------------------------------------------")
    print("Muhtemelen {} bir şey soyledin!".format(duygu))
    print('Pozitif Skor: {}'.format(pozitif_duygu_skoru))
    print('Negatif Skor: {}'.format(negatif_duygu_skoru))
    print('Notr Skor: {}'.format(notr_duygu_skoru))
    print("===============================================\n")
    

cevirici = boto3.client(service_name='translate', use_ssl=True)
dil_isleyici = boto3.client(service_name='comprehend', use_ssl=True)


while True:
    cumle_turkce = input("Turkce bir cümle girin: ")
    
    duygu_sonucu, cevrilmis_cumle = duygu_bul(cumle_turkce, cevirici, dil_isleyici)

    print(cumle_turkce ,cevrilmis_cumle)

    duygu_sonucu_gorsellestir(duygu_sonucu)