#!/usr/bin/env python3

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import colormaps as cm
from mpl_toolkits.mplot3d import axes3d

from scipy import optimize as opt

np.set_printoptions(precision=3)
plt.rcParams.update({"text.usetex": True})

color_map = 'coolwarm'
cmap = cm.get_cmap(color_map)

dir = os.path.dirname(os.path.abspath(__file__))


def get_params(t, x_mes):
    """
    C'est la fonction à modifier
    Considérez une optimisation en minimisant la somme quadratique
        S = Σ(x_mesuré - x_calculé)^2
    Considérez aussi l'utilisation du module Optimize dans SciPy (à installer si besoin)
        https://docs.scipy.org/doc/scipy/tutorial/optimize.html
        https://hernandis.me/2020/04/05/three-examples-of-nonlinear-least-squares-fitting-in-python-with-scipy.html
    """
    E = 1
    tau = 1
    f = 1
    phi = 0
    res = [E, tau, f, phi]
    return res


def main():
    file_name = '/v_ski_data.csv'
    
    # Load data from file
    data = np.genfromtxt(dir + file_name, delimiter=';', names=True)

    t = data[:]['temps_s']
    V_exp = data[:]['déplacement_mesuré_V']

    # Physic Model: V(t) = E exp(-t / tau) sin(2 pi f t + phi)
    E, tau, f, phi = get_params(t, V_exp)
    V_thr = E * np.exp(-t / tau) * np.sin(2*np.pi * f * t + phi)

    plt.plot(t, V_exp, label='$V_{exp}$')
    plt.plot(t, V_thr, label='$V_{thr}$')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
