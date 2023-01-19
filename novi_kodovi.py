import codecs
from bs4 import BeautifulSoup
import requests
import urllib.parse

access = open('novi_kodovi','r')
lines = access.readlines()

suma =  0
for line in lines:
    nema = "gas"
    #print(line)
    #print(access.readline())
    start = line.find('content=https')
    if start == -1:
        continue
    start += 8

    stop = line.find('&format=QR_CODE&error')
    if stop == -1:
        stop = line.find(' HTTP')
    if stop == -1:
        continue
    
    #print(line[start:stop])
    link_sajta = line[start:stop]
    lnk = urllib.parse.unquote(link_sajta)
    
    try:
        sajt = requests.get(lnk).text;
        racun = sajt.split("=======================")[1]
        linije_racuna = racun.split('\n')
        linije_racuna = linije_racuna[2:]
        ukupan_iznos = linije_racuna[-3]
        linije_racuna = linije_racuna[:-4]

        counter= 0
        print(line.split(']')[0].split('[')[1])
        for lin in linije_racuna:
            if counter % 2 == 0:
                # ime
                print(lin)
            else:
                # cena
                # check all chars, if there aren't any digits
                if lin[0:2] != "  ":
                    counter += 2
                    continue
                spaces = lin.rfind(' ')
                cena = float(lin[spaces+1:].replace(',','.'))
                print("Cena: "+str(cena)+" RSD")
                suma += cena


            counter += 1
    except:
        print("ups")

print("Ukupno potrošeno " + str(suma))
