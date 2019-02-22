import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


#  easy plot time domain and freq domain base on real fft
def fft_plot(wave, fs, name='waveform'):
    n = len(wave)
    t = np.linspace(0, n/fs, n)
    f = np.linspace(0, fs/2, round(n/2))
    m1 = np.fft.rfft(wave)

    '''normalize FFT results'''
    m2 = np.abs(m1)/(n/2)
    size = round(n/2)
    m3 = m2[:size]

    '''convert 2 dbm '''
    m4 = 20*np.log10(np.clip(m3, 1e-20, 1e100)) + 10

    '''plot time domain and freq domain'''
    plt.figure(name, figsize=[10, 8])

    plt.subplot(2, 1, 1)
    # plt.xlabel("time(s)")
    # plt.ylabel("volt(v)")
    plt.plot(t, wave, 'g')

    plt.subplot(2, 1, 2)
    # plt.grid()
    # plt.xlabel("freq(Hz)")
    # plt.ylabel("power(dbm)")
    plt.bar(range(len(m3)),m3,width=1,color='b')
    plt.show()


x = np.arange(0, 100*np.pi, np.pi/10)
wave = np.cos(x)
fft_plot(wave,1)

pulse = np.linspace(0,0,1000)
for i in range(500,617,1):
    pulse[i] = 1
fft_plot(pulse,1)

wave1 = np.multiply(pulse, wave)
wave2 = wave1[500:617]
fft_plot(wave2,1)



