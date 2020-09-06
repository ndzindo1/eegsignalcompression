import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from bitarray import bitarray


def izracunajDeltu(signal):
    return 12


def deltaModulacija(signal, i):
    pocetnaVrijednost = int(round(signal[0]))
    ###delta = izracunajDeltu(signal)
    delta = i
    nizBita = bitarray()
    deltaSignal = [pocetnaVrijednost]

    for i in range(len(signal) - 1):
        if (signal[i + 1] > deltaSignal[i]):
            deltaSignal.append(deltaSignal[i] + delta)
            nizBita.append(1)
        else:
            deltaSignal.append(deltaSignal[i] - delta)
            nizBita.append(0)

    return pocetnaVrijednost, delta, nizBita, deltaSignal


def inverznaDeltaModulacija(pocetnaVrijednost, delta, nizBita):
    noviSignal = [pocetnaVrijednost]

    for i in range(len(nizBita)):
        if (nizBita[i] == True):
            noviSignal.append(noviSignal[i] + delta)
        else:
            noviSignal.append(noviSignal[i] - delta)

    return noviSignal


def main():
    signali_mat = sio.loadmat('signali.mat')
    signali = signali_mat['data']
    signal = signali[0]

    for i in range(30):
        pocetnaVrijednost, delta, nizBita, deltaSignal = deltaModulacija(signal, i)
        noviSignal = inverznaDeltaModulacija(pocetnaVrijednost, delta, nizBita)

        x = np.linspace(0, len(signali[0]), len(signali[0]))
        fig, pt = plt.subplots(1)
        plt.title('Usporedba signala sa deltom ' + str(i))
        plt.plot(x, signal)
        plt.plot(x, deltaSignal)
        plt.show()

main()