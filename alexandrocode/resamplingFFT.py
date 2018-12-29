
# --uft8--

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


if __name__ == '__main__':
    """load waveform"""
    wave = np.loadtxt("C:\\Users\\gonghaiq\\Desktop\\keysight 5gnr waveform\\debug"
                      "\\5gnr_100m_fs2400m_frame_imag.txt")
    length_wave = len(wave)
    print("start...")
    # cut_length = int(len(wave)/10)
    # wave = wave[:cut_length]
    # Fs = 1000
    # N = 1000
    # t = np.arange(0, N / Fs, 1/Fs)
    # noise = 0.0001*np.random.randint(0, 100, N)
    # wave = 0.01 * np.cos(2*np.pi*100*t) + 0.02*np.cos(2*np.pi*200*t) + noise

    """set parameter"""
    fs = 122880000
    fr = 2400000000

    length = int(len(wave))
    length1 = int(fr*length/fs)

    zero_num = int((length1 - length)/2)

    length2 = int(length/2)
    print("start fft")
    fft_wave = np.fft.rfft(wave)
    print("0")

    zero_wave = np.zeros(zero_num,  dtype=np.complex64)
    print("1")

    # fft_wave_new = np.concatenate([fft_wave[:length2], zero_wave, fft_wave[length2:]])
    fft_wave_new = np.concatenate([fft_wave[:length2], zero_wave])
    print("2")

    del zero_wave
    del fft_wave
    del wave

    # # float 5 to save memory
    # fft_real = fft_wave_new.real
    # fft_imag = fft_wave_new.imag
    #
    # del fft_wave_new
    #
    # fft_wave_new0 = []
    # for i in range(len(fft_real)):
    #     fft_real[i] = round(float(fft_real[i]), 5)
    #     fft_imag[i] = round(float(fft_imag[i]), 5)
    #     fft_wave_new0.append(complex(fft_real[i], fft_imag[i]))
    #
    # del fft_real
    # del fft_imag

    print("3")

    new_wave = np.fft.irfft(fft_wave_new)*(len(fft_wave_new)/length_wave)
    print("4")

    with open("C:\\Users\\gonghaiq\\Desktop\\keysight 5gnr waveform\\debug\\5gnr_100m_fs2400m_frame_imag_Fs2400m.txt", 'w') as f:
        for i in new_wave:
            f.write(str(i)+'\n')

    print("5")
    # fft_plot(wave, fs)
    # fft_plot(new_wave, fr)