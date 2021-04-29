#%%
from suaBibSignal import *
import peakutils  # alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    signal = signalMeu()
    fs = 44100
    duration = 2
    numAmostras = duration * fs

    
    sd.default.samplerate = fs  
    sd.default.channels = 1  

   
    print('A GRAVACAO SERA INICIADA EM 5 SEGUNDOS')
    time.sleep(5)
    print('GRAVACAO INICADA')
    
    audio = sd.rec(int(numAmostras), dtype='float32')
    sd.wait()
    print("FIM DA GRAVACAO")
    
    dados = []
    for i in audio:
        dados.append(i)
    
    print("TAMANHO DOS DADOS: ", len(dados))
    
    t = np.linspace(-1, 1,1*fs*duration)
   

    plt.plot(t, dados, "b--", label="Dados gravacao x tempo")
    
    amp = audio[:,0]

   
    xf, yf = signal.calcFFT(amp, fs)
    plt.figure("F(y)")
    plt.plot(xf, yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()
    #plt.savefig('img/fourier.png', format="png")

    indexes = peakutils.indexes(yf, thres=0.1, min_dist=50)
    print("INDEX DOS PICOS {}" .format(indexes))

    temp = []
    for frequency in xf[indexes]:
        if frequency >0:
            print('PICO DE FREQUENCIA ENCONTRADO: {} Hz'.format(np.round(frequency,2)))
            temp.append(int(frequency))
    
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

    idxs = []
    errMargin= 10

    if len(temp)<=1:
        print("SOMENTE UM PICO FOI DETECTADO, FAVOR TENTAR NOVAMENTE")
    else:
        for freq in temp:
            if freq>1000:
                for idx, val in enumerate(freqMatrix[0]['row']):
                    if (val-errMargin)<freq<(val+errMargin):
                        idxs.append(idx)
            elif freq <1000:
                for idx, val in enumerate(freqMatrix[1]['col']):
                    if (val-errMargin)<freq<(val+errMargin):
                        idxs.append(idx)
        decodedDigit = digitMatrix[idxs[0]][idxs[1]]
        print("DECODIFICACAO COMPLETA\nDIGITO CLICADO: ", decodedDigit)
        

if __name__ == "__main__":
    main()

# %%
