import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from bitarray import bitarray

koeficijentDesetkovanja = 4
delta = 12

def deltaModulacija(signal):
    pocetnaVrijednost = int(round(signal[0]))
    nizBita = bitarray()
    deltaSignal = [pocetnaVrijednost]

    for i in range(len(signal) - 1):
        if(signal[i+1] > deltaSignal[i]):
            deltaSignal.append(deltaSignal[i] + delta)
            nizBita.append(1)
        else:
            deltaSignal.append(deltaSignal[i] - delta)
            nizBita.append(0)

    return pocetnaVrijednost, delta, nizBita, deltaSignal


def inverznaDeltaModulacija(pocetnaVrijednost, delta, nizBita):
    noviSignal = [pocetnaVrijednost]

    for i in range(len(nizBita)):
        if(nizBita[i] == True):
            noviSignal.append(noviSignal[i] + delta)
        else:
            noviSignal.append(noviSignal[i] - delta)

    return noviSignal

def smanjiFrekvencijuUzorkovanjaSignala(signal, koeficijentDesetkovanja):
    noviSignal = []

    for i in range(len(signal)):
        if(i % koeficijentDesetkovanja == 0):
            noviSignal.append(signal[i])

    return noviSignal

def povecajFrekvencijuUzorkovanjaSignala(signal, koeficijentDesetkovanja):
    noviSignal = []

    for i in range(len(signal)):
        noviSignal.append(signal[i])
        for j in range(koeficijentDesetkovanja - 1):
            noviSignal.append(noviSignal[-1])

    return noviSignal

def main():
    signali_mat = sio.loadmat('signali.mat')
    signali = signali_mat['data']
    signal = signali[0]

    pocetnaVrijednost, delta, nizBita, detlaSignal= deltaModulacija(signal)
    noviSignal = inverznaDeltaModulacija(pocetnaVrijednost, delta, nizBita)

    x = np.linspace(0, len(signali[0]), len(signali[0]))
    fig, pt = plt.subplots(3)
    fig.tight_layout(pad=1.8)

    pt[0].set_ylim([-250, 250])
    pt[0].plot(x, signal)
    pt[0].set_title('Originalni signal')

    pt[1].set_ylim([-250, 250])
    pt[1].plot(x, noviSignal)
    pt[1].set_title('Signal dobijen inverznom delta modulacijom sa deltom ' + str(delta))

    desetkovaniSignal = smanjiFrekvencijuUzorkovanjaSignala(signal, koeficijentDesetkovanja)
    pocetnaVrijednost, delta, nizBita, deltaSignal = deltaModulacija(desetkovaniSignal)
    noviSignal = inverznaDeltaModulacija(pocetnaVrijednost, delta, nizBita)
    noviSignal = povecajFrekvencijuUzorkovanjaSignala(noviSignal, koeficijentDesetkovanja)

    pt[2].set_ylim([-250, 250])
    pt[2].plot(x, noviSignal)
    pt[2].set_title('Signal dobijen inverznom delta modulacijom desetkovanog signala sa deltom ' + str(delta))

    plt.show()

main()