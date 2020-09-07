from collections import Counter as ctr
from operator import itemgetter
import binascii
from kvantizacija import noviSignal, x
import matplotlib.pyplot as plt

lista = ''

def Shannon_Fano(signal):
    znakovi = ctr(signal)
    lista = sorted([(b,'') for b,a in znakovi.items()], key=itemgetter(0), reverse=True)
    Shannon_Fano_Pomocna(0, len(lista)-1, lista)
    rjecnikKodovaFun = dict((key, value) for key,value in lista)

    kodiraniSignal = ''
    for karakter in signal:
        kodiraniSignal += rjecnikKodovaFun[karakter]
    

    #print(kodiraniSignal)
    return kodiraniSignal, rjecnikKodovaFun
    
def Shannon_Fano_Pomocna(donjiDio, gornjiDio, lista):

    size = gornjiDio - donjiDio + 1
    if size > 1:
        mid = int(size / 2 + donjiDio)
        for i in range(donjiDio, gornjiDio + 1):
            tup = lista[i]
            if i < mid:
                lista[i] = (tup[0], tup[1] + '0')
            else:
                lista[i] = (tup[0], tup[1] + '1')
        Shannon_Fano_Pomocna(donjiDio, mid - 1, lista)
        Shannon_Fano_Pomocna(mid, gornjiDio, lista)

def dekodiraj(kodiraniSignal, rjecnikKodova):

    inverzniRijecnik = dict([(value, key) for key,value in rjecnikKodova.items()])
    
    zaDekodiranje = kodiraniSignal
    
    dekodiraniSignal=[]
    trenutniSimboli = ""
    indexZadnjeg = 0
    while len(zaDekodiranje)>0:
        trenutniSimboli = trenutniSimboli + zaDekodiranje[indexZadnjeg]
        if(trenutniSimboli in inverzniRijecnik):
            dekodiraniSignal.append(inverzniRijecnik.get(trenutniSimboli))
            zaDekodiranje=zaDekodiranje[indexZadnjeg+1:]
            indexZadnjeg = 0
            trenutniSimboli=""
        else :
            indexZadnjeg =indexZadnjeg +1

    return dekodiraniSignal

def izvjestaj():

    brojBitaOrginalnogSignala = len(ulazniSignal)*32
    brojBitaKodiranogSignala = len(kodiraniSignal)
    znakovi = ctr(ulazniSignal)
    lista_ponavljanja = [a for b,a in znakovi.items()]
    
    print('Rjecnik vrijednosti:')
    for karakter in rjecnikKodova:
        print("Vrijednost:" + str(karakter) + ", Kod: " + rjecnikKodova[karakter])
    
    print(" ")
    print("Broj bita potreban za prikaz nekodiranog signala: " + str(brojBitaOrginalnogSignala))
    print("Broj bita potreban za prikaz kodiranog signala: " + str(brojBitaKodiranogSignala))
    print("Stepen kompresije iznosi: " + str(brojBitaOrginalnogSignala/brojBitaKodiranogSignala))
    
    if(ulazniSignal == dekodiraniSignal).all():
        print("Ulazni i dekodirani signal su identicni.")
    else:
        print("Ulazni i dekodirani signal nisu identicni.")

    print('Ulazni signal:', ulazniSignal)
    datoteka = open('kodiraniSignalShannonFano.txt','a+')
    datoteka.write(kodiraniSignal)
    datoteka.close()
    print('Kodirani signal je upisan u datoteku kodiraniSignalShannonFano.txt')

    fig, pt = plt.subplots(2)
    fig.tight_layout(pad=3.0)

    fig.suptitle('Shannon-Fano kompresija')
    pt[0].plot(x, ulazniSignal)
    pt[0].set_title('Ulazni signal')

    pt[1].plot(x, dekodiraniSignal)
    pt[1].set_title('Dekodirani signal: ')

    plt.show()

ulazniSignal = noviSignal
kodiraniSignal, rjecnikKodova = Shannon_Fano(ulazniSignal)
dekodiraniSignal = dekodiraj(kodiraniSignal, rjecnikKodova)
izvjestaj()
