from collections import Counter
from queue import PriorityQueue
from kvantizacija import noviSignal, x
import matplotlib.pyplot as plt

class cvor:
    def __init__(self,karakter=None, frekvencija=None):
        self.karakter = karakter
        self.frekvencija = frekvencija
        self.desni = None
        self.lijevi = None


    def __lt__(self, cvor2):
        return self.frekvencija < cvor2.frekvencija

rjecnikStabla = dict()
inverzniRijecnik = dict()

def kodirajVrijednostiStabla(trenutni_cvor, dekompresovani_string):
    if trenutni_cvor is None:
        return
    if trenutni_cvor.lijevi is None and trenutni_cvor.desni is None:
        rjecnikStabla[trenutni_cvor.karakter] = dekompresovani_string
        return
    kodirajVrijednostiStabla(trenutni_cvor.lijevi, dekompresovani_string+"0")
    kodirajVrijednostiStabla(trenutni_cvor.desni, dekompresovani_string+"1")

def dekodiraj(kodiraniSignal):
    inverzniRijecnik = dict([(value, key) for key,value in rjecnikStabla.items()])
    
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
    
    print('Rjecnik simbola:')
    for karakter in rjecnikStabla:
        print(karakter,'->',rjecnikStabla[karakter])

    duzinaKodiranogSignala = len(kodiraniSignal)
    print("Broj bita kodiranog signala: ", duzinaKodiranogSignala)
    #Pošto se za ascii reprezentaciju uzima 8bita tako da ćemo stepen računati na sljedeći način
    stepen_kompresije = 32*len(ulazniSignal)/duzinaKodiranogSignala
    print('Stepen kompresije:', stepen_kompresije)


    print('Ulazni signal:', ulazniSignal)
    datoteka = open('kodiraniSignal.txt','a+')
    datoteka.write(kodiraniSignal)
    datoteka.close()
    print('Kodirani signal je upisan u datoteku kodiraniSignal.txt')

    if(ulazniSignal == dekodiraniSignal).all():
        print('Ulazni i dekodirani signali su identicni.')

    fig, pt = plt.subplots(2)
    fig.tight_layout(pad=3.0)

    fig.suptitle('Huffman')
    pt[0].plot(x, ulazniSignal)
    pt[0].set_title('Ulazni signal')

    pt[1].plot(x, dekodiraniSignal)
    pt[1].set_title('Dekodirani signal: ')

    plt.show()


def kodiraj(signal):
    frekvencija=Counter(signal).most_common()
    Qsize = len(frekvencija)
    Q = PriorityQueue()

    print("Broj pojavljivanja vrijednosti:")
    print(frekvencija)
    for key,value in frekvencija:
        element = cvor(key, value)
        Q.put(element)

    #Kreiranje stabla
    while(Qsize!= 1):
        novicvor = cvor()
        lijevi = Q.get()
        desni = Q.get()
        novicvor.lijevi = lijevi
        novicvor.desni = desni
        novicvor.frekvencija = lijevi.frekvencija + desni.frekvencija
        Q.put(novicvor)
        Qsize-=1

    #Pretvaranje stabla u rjecnik
    for i in range (0,len(frekvencija)):
        dekompresovani_karakter = {frekvencija[i][0]:0}
        rjecnikStabla.update(dekompresovani_karakter)
    kodirajVrijednostiStabla(Q.get(), '')

    kodiraniSignal = ''
    for karakter in signal:
        kodiraniSignal += rjecnikStabla[karakter]
    
    return kodiraniSignal

ulazniSignal = noviSignal
kodiraniSignal = kodiraj(ulazniSignal)
dekodiraniSignal = dekodiraj(kodiraniSignal)
izvjestaj()