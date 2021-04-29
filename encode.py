#%%
#importe as bibliotecas
import sys
sys.path.append('')
import numpy as np
from suaBibSignal import *
import sounddevice as sd
import matplotlib.pyplot as plt

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    c = signalMeu()
    print("Inicializando encoder")
    print("Aguardando usuário")

    freqMatrix = [
        {"row": [1209,1336,1477,1633]},
        {"col": [697,770,852,941]}
    ] 

    digitMatrix = [
        ["1",  "2",  "3",  "A"],
        ["4",  "5",  "6",  "B"],
        ["7",  "8",  "9",  "C"],
        ["X",  "0",  "#",  "D"]
    ]

    respectiveFreqs = []

    digitChosen = input("Digite um algarismo ou um desses * # A B C D: ")
    print("Digito pressionado:", digitChosen)
    
    if (digitChosen in digitMatrix[0]):
        for idx, val in enumerate(digitMatrix[0]):
            if digitChosen == val:
                respectiveFreqs.append(freqMatrix[1]['col'][0])
                respectiveFreqs.append(freqMatrix[0]['row'][idx])
    elif digitChosen in digitMatrix[1]:
        for idx, val in enumerate(digitMatrix[1]):
            if digitChosen == val:
                respectiveFreqs.append(freqMatrix[1]['col'][1])
                respectiveFreqs.append(freqMatrix[0]['row'][idx])
    elif digitChosen in digitMatrix[2]:
        for idx, val in enumerate(digitMatrix[2]):
            if digitChosen == val:
                respectiveFreqs.append(freqMatrix[1]['col'][2])
                respectiveFreqs.append(freqMatrix[0]['row'][idx])
    elif digitChosen in digitMatrix[3]:
        for idx, val in enumerate(digitMatrix[3]):
            if digitChosen == val:
                respectiveFreqs.append(freqMatrix[1]['col'][3])
                respectiveFreqs.append(freqMatrix[0]['row'][idx])
    
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    
    sampleRate = 44100
    Te = 1
    
    sd.default.samplerate = sampleRate
    sd.default.channels = 1
    

    print("Gerando Tom referente ao símbolo : {}".format(digitChosen))
    print(respectiveFreqs[0], respectiveFreqs[1])
    x, y =  c.generateSin(respectiveFreqs[0], 1, Te, sampleRate)
    xis, ipslom = c.generateSin(respectiveFreqs[1], 1, Te, sampleRate)
    sine = y + ipslom
    sd.play(sine, sampleRate)
    sd.wait()

    xf, yf = c.calcFFT(sine, sampleRate)
    plt.figure("F(y)")
    plt.plot(xf, yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()
    
    time = np.linspace(-Te, Te, Te*sampleRate)
    plt.plot(time, y, "b--", label="Frequencia {} Hz".format(respectiveFreqs[0]))
    plt.plot(time, ipslom, "r--", label="Frequencia {} Hz".format(respectiveFreqs[1]))
    plt.plot(time, sine, "g-.", label="Freq 1 ({0}) + Freq 2 ({1})".format(y, ipslom))
    plt.title("Grafico do som gerado pelo digito ecolhido {}".format(digitChosen))
    plt.ylabel("Amplitude")
    plt.xlabel("Tempo (s)")
    plt.xlim(0,0.015)
    plt.legend()
    plt.show()
    
    
    #plotFFT(self, signal, fs)
    
    #plt.savefig('img/graph_digit_{}.png'.format(digitChosen), format='png')
    
if __name__ == "__main__":
    main()

# %%
