#!/usr/bin/env python3

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import colormaps as cm
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
    ax_3d = fig.add_subplot(3, 3, (2, 6), projection='3d')
    ax_3d.set_title('3D Plot')
    ax_3d.set_proj_type('ortho')
    ax_3d.view_init(15, -30)
    ax_3d.plot(ddx, ddy, ddz)

    # Use Discrete Fourier Transform module from numpy
    # https://numpy.org/doc/stable/reference/routines.fft.html
    ax = fig.add_subplot(3, 3, (8, 9))
    freq = np.arange(ddz.shape[0])
    four = np.zeros(ddz.shape[0])
    ax.set_title('Frequential Analysis')
    ax.plot(freq, four)

    plt.tight_layout(pad=1)
    plt.show()


if __name__ == "__main__":
    main()
