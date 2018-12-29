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


# calc largest multiple
def lcm(m, n):
    if m == n:
        return m
    elif m > n:
        divisor = n
        dividend = m
    else:
        divisor = m
        dividend = n

    remainder = divisor % dividend

    while remainder > 0:
        divisor = dividend
        dividend = remainder
        remainder = divisor % dividend

    return m*n/dividend


# convolve
def convolve(wave1, wave2):
    wave = [0]*(len(wave1)+len(wave2))
    for i in range(len(wave1)):
        for j in range(len(wave2)):
            wave[i+j] = wave1[i]*wave2[j]+wave[i+j]
    return wave[0:len(wave1)]


# hd
def sa(wc, n):
    phase = np.arange(0, n, 1) - n/2
    print(phase[31])
    if phase[int(n/2)] == 0:
        phase[int(n/2)] = 1e-20
    wave = np.sin(wc*phase)/(np.pi*phase)
    return wave


def normalize(h):
    max_value = np.max(h)
    wave = h/max_value
    return wave


#  window type selector and order calculate
def calc_window_order(wp, win_type):
    if win_type == 'hanning':
        wn = 6.2 * np.pi
        i = round(wn / wp) + 1
    elif win_type == 'hamming':
        wn = 6.6 * np.pi
        i = round(wn / wp) + 1
    elif win_type == 'blackman':
        wn = 11 * np.pi
        i = round(wn / wp) + 1
    elif win_type == 'nuttal':
        wn = 15.4 * np.pi
        i = round(wn / wp) + 1
    else:
        print('No window type found')
    return i


#  hanning window
def hanning_win(m):
    phase = np.arange(0, m, 1)/m
    hanning = 0.5 + 0.5*np.cos(2*np.pi*phase-np.pi)
    return hanning


#  hamming window
def hamming_win(m):
    a = 0.54
    phase = np.arange(0, m, 1)/m
    hamming = a + (1-a)*np.cos(2*np.pi*phase-np.pi)
    return hamming


#  blackman window
def blackman_win(m):
    a0 = 0.42
    a1 = 0.5
    a2 = 0.08
    phase = np.arange(0, m, 1)/m
    blackman = a0 - a1*np.cos(2*np.pi*phase)+a2*np.cos(4*np.pi*phase)
    return blackman


#  nuttal window
def nuttal_win(m):
    a0 = 0.355768
    a1 = 0.487396
    a2 = 0.144232
    a3 = 0.012604
    phase = np.arange(0, m, 1)/m
    nuttal = a0 - a1*np.cos(2*np.pi*phase)+a2*np.cos(4*np.pi*phase )-a3*np.cos(6*np.pi*phase)
    return nuttal


if __name__ == '__main__':
    # M = 10
    # Fs = 1000
    # N = 8000
    # t = np.arange(0, N / Fs, 1 / Fs)
    # real = 0.01 * np.cos(2 * np.pi * 100 * t) + 0.5 * np.cos(2 * np.pi * 50 * t)
    """load waveform"""
    # wave = np.loadtxt("C:\\Users\\gonghaiq\\Desktop\\Temp\\20181026_5GNR100M\\4G-LTE"
    #                   "\\LTE_12_0_DL_20MHz_BW_256QAM_FDD_FS_122880000_Real.txt")

    Fs = 1000
    N = 1000
    t = np.arange(0, N / Fs, 1/Fs)
    noise = 0.0001*np.random.randint(0, 100, N)
    wave = 0.01 * np.cos(2*np.pi*100*t) + 0.02*np.cos(2*np.pi*200*t) + noise

    fft_plot(wave, Fs)

    # length = int(len(wave) / 10)
    # wave = wave[length:length*2]
    # print(length)
    # fft_plot(wave, 122880000)

    """set parameter"""
    fs = 1000
    fr = 2400
    k = lcm(fs, fr)
    L = int(k/fs)
    M = int(k/fr)
    print("L=", L)
    print("M=", M)

    '''interpolating'''
    wave0 = []
    for i in range(len(wave)):
        wave0.append(wave[i])
        for j in range(L-1):
            wave0.append(0)

    fft_plot(wave0, Fs*L)
    '''LPF design'''
    bw = np.pi/20
    N = calc_window_order(bw, 'hanning')
    print("N=", N)
    win = hanning_win(N)

    wp1 = np.pi/2/L
    wp2 = np.pi/2/M
    wp = np.fmin(wp1, wp2)
    wc = (2*wp+bw)/2
    hd = sa(wc, N)
    fft_plot(hd, 12000)
    h = hd * win

    h_normal = normalize(h)

    fft_plot(h_normal, 12000)

    wave1 = convolve(wave0, h_normal)
    factor = (len(wave1)/len(wave))

    fft_plot(wave1, 12000)

    del wave0

    '''Decimating'''
    wave2 = []
    for i in range(0, len(wave1), M):
        point = wave1[i] #* factor
        wave2.append(point)

    # hd = sa(np.pi/2, 100)
    # win = nuttal_win(100)
    # h = hd * win
    # plt.subplot(2, 2, 1)
    # plt.plot(hd)
    # plt.subplot(2, 2, 2)
    # plt.plot(win)
    # plt.subplot(2, 2, 3)
    # plt.plot(h)
    # plt.subplot(2, 2, 4)
    # plt.plot(abs(np.fft.rfft(h)))
    # plt.show()
    # fft_plot(h, 1)
    # fft_plot(real, 1000)
    fft_plot(wave2, fr)
    # fig1 = np.abs(np.fft.rfft(real))
    # fig2 = np.abs(np.fft.rfft(wave2))
    # plt.subplot(2, 1, 1)
    # plt.plot(fig1)
    # plt.subplot(2, 1, 2)
    # plt.plot(fig2)
    # plt.show()










