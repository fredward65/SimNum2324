#!/usr/bin/env python3

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import colormaps as cm
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import axes3d

np.set_printoptions(precision=3)
plt.rcParams.update({"text.usetex": True})

color_map = 'coolwarm'
cmap = cm.get_cmap(color_map)

dir = os.path.dirname(os.path.abspath(__file__))


def find(data, txt_1, txt_2):
    idx_0 = np.where(data[0] == txt_1)[0]
    idx_1 = np.where(data[1] == txt_2)[0]
    idx_2 = [idx_0[idx_0 == idx_i][0] for idx_i in idx_1 if idx_0[idx_0 == idx_i].size > 0][0]
    return idx_2


def primitive(dx, t, x0=0):
    dt = np.diff(t)
    dt = np.append(dt, [dt[-1]])
    x = []
    for dx_i, dt_i in zip(dx, dt):
        x.append(x0)
        x0 += dx_i * dt_i
    return np.array(x)


def main():
    """
    Le fichier 'mesures_shimmer_équilibre.csv' contient des enregistrements de l'accélération d'une personne qui reste debout sans bouger.
    On peut visualiser si on trace l'accélération suivant z en fonction du temps une courbe sinusoidale sur laquelle se superposent la respiration et les battements du coeur.
    """
    file_name = '/mesures_shimmer_équilibre.csv'
    
    # Load data from file
    data = np.genfromtxt(dir + file_name, delimiter='\t', skip_header=1, dtype=str)

    # Select acceleration data
    idx_t = find(data, 'Timestamp', 'CAL')
    idx_ddx = find(data, 'Low Noise Accelerometer X', 'CAL')
    idx_ddy = find(data, 'Low Noise Accelerometer Y', 'CAL')
    idx_ddz = find(data, 'Low Noise Accelerometer Z', 'CAL')
    t = np.array(data[3:, idx_t]).astype('float') / 1000
    ddx = np.array(data[3:, idx_ddx]).astype('float')
    ddy = np.array(data[3:, idx_ddy]).astype('float')
    ddz = np.array(data[3:, idx_ddz]).astype('float')

    # Cartesian Coordinates Plot
    ddv = np.c_[ddx, ddy, ddz]
    fig = plt.figure()
    for i in range(3):
        ax = fig.add_subplot(3, 3, 0 + 3*i + 1)
        ax.plot(t, ddv[:, i])

    # 3D Plot
    dx = primitive(ddx, t)
    dy = primitive(ddy, t)
    dz = primitive(ddz, t)
    x = primitive(dx, t)
    y = primitive(dy, t)
    z = primitive(dz, t)
    plt.figure()
    plt.plot(t, np.c_[x, y, z])

    ax_3d = fig.add_subplot(3, 3, (2, 6), projection='3d')
    ax_3d.set_title('3D Plot')
    ax_3d.set_proj_type('ortho')
    ax_3d.view_init(15, -30)
    ax_3d.plot(x, y, z)

    # Use Discrete Fourier Transform module from numpy
    # https://numpy.org/doc/stable/reference/routines.fft.html
    ax = fig.add_subplot(3, 3, (8, 9))
    freq = np.fft.fftfreq(t.shape[0])
    four = np.fft.fft(ddz)
    ax.set_title('Frequency Analysis')
    ax.plot(freq, np.c_[four.real, four.imag])

    four_ = np.copy(four)
    four_[:four_.size//3] *= 0
    inv_four = np.fft.ifft(four_)
    fig = plt.figure()
    fig.add_subplot()
    plt.plot(t, ddz, alpha=0.5)
    ddz_handler = plt.plot(t, inv_four)
    ax_handler_1 = fig.add_axes([.15, .05, .75, .1])
    ax_handler_2 = fig.add_axes([.15, .10, .75, .1])

    f_l_slider = Slider(ax=ax_handler_1, label='F Lo', valmin=0, valmax=four_.size - 1, valinit=0)
    f_h_slider = Slider(ax=ax_handler_2, label='F Hi', valmin=0, valmax=four_.size - 1, valinit=four_.size - 1)

    def update(val):
        four_ = np.copy(four)
        lo = int(f_l_slider.val)
        hi = int(f_h_slider.val)
        if lo < hi:
            four_[:lo] *= 0
            four_[hi:] *= 0
        else:
            four_[lo:hi] *= 0
        inv_four = np.fft.ifft(four_)
        ddz_handler[0].set_data(t, inv_four.real)

    f_l_slider.on_changed(update)
    f_h_slider.on_changed(update)

    plt.tight_layout(pad=1)
    plt.show()


if __name__ == "__main__":
    main()
