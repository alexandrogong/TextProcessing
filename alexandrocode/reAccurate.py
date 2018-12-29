# cut short wave
import numpy as np
import matplotlib.pylab as plt


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
    plt.xlabel("time(s)")
    plt.ylabel("volt(v)")
    plt.plot(t, wave, 'g')

    plt.subplot(2, 1, 2)
    plt.grid()
    plt.xlabel("freq(Hz)")
    plt.ylabel("power(dbm)")
    plt.plot(f, m4, 'b')
    plt.show()


if __name__ == "__main__":
    path = "C:\\Users\\gonghaiq\\Desktop\\keysight 5gnr waveform\\debug\\" \
           "5gnr_100m_fs2400m_frame_imag_Fs2400m.txt"

    wave = []
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            wave.append(round(float(line), 5))
            line = f.readline()

    # wave1 = []
    # i, j = 0, 0
    # for i in range(len(wave)):
    #     j = i * 10
    #     if j <= len(wave):gongh
    #         wave1.append(wave[j])
    # fft_plot(wave1, 240000000)

    with open("C:\\Users\\gonghaiq\\Desktop\\keysight 5gnr waveform\\debug\\"
              "5gnr_100m_fs2400m_frame_imag_Fs2400m_short.txt", 'w') as f:
        for i in wave:
            f.write(str(i)+'\n')
