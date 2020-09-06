import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import copy

brojPragova = 32

def kvatiziraj(signal, brojPragova):
    kSignal = copy.deepcopy(signal)
    minSig = min(signal)
    maxSig = max(signal)
    ukupniRaspon = abs(maxSig - minSig)
    jedinicniRaspon = ukupniRaspon / brojPragova

    pragovi = []
    for i in range(brojPragova):
        minPragTmp = minSig + (i * jedinicniRaspon) - (jedinicniRaspon / 2)
        maxPragTmp = minSig + (i * jedinicniRaspon) + (jedinicniRaspon / 2)
        meanPragTmp = round((maxPragTmp + minPragTmp) / 2)
        pragovi.append(meanPragTmp)
        for j in range(len(kSignal)):
            if(kSignal[j] > minPragTmp and kSignal[j] < maxPragTmp):
                kSignal[j] = meanPragTmp

    return kSignal, pragovi

def kvantizirajLog(signal, brojPragova):
    noviSignal = copy.deepcopy(signal)
    minSig = min(signal)
    maxSig = max(signal)
    ukupniRaspon = abs(maxSig - minSig)
    jedinicniRaspon = ukupniRaspon / brojPragova

    pragovi = []
    for i in range(brojPragova):
        minPragTmp = minSig + (i * jedinicniRaspon) - (jedinicniRaspon / 2)
        maxPragTmp = minSig + (i * jedinicniRaspon) + (jedinicniRaspon / 2)
        meanPragTmp = int(round((maxPragTmp + minPragTmp) / 2))
        pragovi.append(meanPragTmp)

    for i in range(len(noviSignal)):
        rasponIndeksaZaSkokPretrage = int(brojPragova / 4)
        indeksPretrage = int(brojPragova / 2)
        if(noviSignal[i] >= pragovi[-1]):
            noviSignal[i] = int(pragovi[-1])
        while(True):
            # da li je u dobrom opsegu
            if(noviSignal[i] >= pragovi[indeksPretrage - 1]-1 and noviSignal[i] <= pragovi[indeksPretrage]+1):
                # zaokruzi na manje
                if(noviSignal[i] - pragovi[indeksPretrage - 1] < pragovi[indeksPretrage] - noviSignal[i]):
                    noviSignal[i] = int(pragovi[indeksPretrage - 1])
                # zaokruzi na vece
                else:
                    noviSignal[i] = int(pragovi[indeksPretrage])
                break
            # pretrazi za vece pragove
            if(noviSignal[i] > pragovi[indeksPretrage - 1]):
                indeksPretrage = indeksPretrage + rasponIndeksaZaSkokPretrage
            # pretrazi za manje pragove
            else:
                indeksPretrage = indeksPretrage - rasponIndeksaZaSkokPretrage
            rasponIndeksaZaSkokPretrage = int(rasponIndeksaZaSkokPretrage / 2)
            if(rasponIndeksaZaSkokPretrage == 0 and indeksPretrage >= 2):
                rasponIndeksaZaSkokPretrage = rasponIndeksaZaSkokPretrage + 1

    return noviSignal, pragovi

def main():
    signali_mat = sio.loadmat('signali.mat')
    signali = signali_mat['data']
    signal = signali[0]

    noviSignal, pragovi = kvantizirajLog(signal, brojPragova)

    x = np.linspace(0, len(signali[0]), len(signali[0]))
    fig, pt = plt.subplots(2)
    fig.tight_layout(pad=3.0)
    pt[0].plot(x, signal)
    pt[0].set_title('Originalni signal')
    pt[1].plot(x, noviSignal)
    pt[1].set_title('Kvantizirani signal sa brojem pragova: ' + str(brojPragova))

    plt.show()

    return noviSignal, x

noviSignal, x = main()

