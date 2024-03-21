#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

np.set_printoptions(precision=3)
plt.rcParams.update({"text.usetex": True})

# Gravity acceleration
g = 9.80665
# Double Pendulum parameters
m_1 = .5
m_2 = .5
l_1 = .1
l_2 = .2

def compute_dot_omega(th_1, th_2, om_1, om_2):
    """
    myPhysicsLab Double Pendulum
    https://www.myphysicslab.com/pendulum/double-pendulum-en.html
    """
    
    dw_1 = 0
    dw_2 = 0

    return dw_1, dw_2

def main():
    # Initial conditions
    th_1 = .25*np.pi
    th_2 = .30*np.pi
    om_1 = 0
    om_2 = 0

    # Time period
    t_f = 1
    t = np.linspace(0, t_f, num=t_f*30)
    dt = np.diff(t)
    dt = np.append(dt, [dt[-1]])

    # Compute system
    th_1_l = []
    th_2_l = []
    plt.xlim(-.5, .5)
    plt.ylim(-.5, .5)
    plt.title(r'Double Pendulum Simulation - $t_f = %5.2f$' % t_f)
    plt.gca().set_aspect(1)

    # Lambda expressions for x_1, y_1, x_2, and y_2
    x_1 = lambda th_1: l_1 * np.sin(th_1)
    y_1 = lambda th_1: l_1 * np.cos(th_1) * -1
    x_2 = lambda th_1, th_2: x_1(th_1) + l_2 * np.sin(th_2)
    y_2 = lambda th_1, th_2: y_1(th_1) - l_2 * np.cos(th_2)

    # Plot elements for animation
    line_data = [[x_2(th_1, th_2)], [y_2(th_1, th_2)]]
    line = plt.plot(line_data[0], line_data[1], 'k', alpha=.25)[0]
    
    arm_1 = plt.plot([0, x_1(th_1)], [0, y_1(th_1)], 'b', lw=2)[0]
    arm_2 = plt.plot([x_1(th_1), x_2(th_1, th_2)], [y_1(th_1), y_2(th_1, th_2)], 'r', lw=2)[0]
    
    bob_1 = plt.plot([x_1(th_1)], [y_1(th_1)], 'ob', lw=2)[0]
    bob_2 = plt.plot([x_2(th_1, th_2)], [y_2(th_1, th_2)], 'or', lw=2)[0]

    # Animation
    for dt_i in dt:
        # Append angles to list
        th_1_l.append(th_1)
        th_2_l.append(th_2)

        # Compute angular acceleration
        dw_1, dw_2 = compute_dot_omega(th_1, th_2, om_1, om_2)

        # Euler integration
        om_1 += dw_1 * dt_i
        om_2 += dw_2 * dt_i
        th_1 += om_1 * dt_i
        th_2 += om_2 * dt_i

        c_x = x_2(th_1, th_2)
        c_y = y_2(th_1, th_2)
        line_data[0].append(c_x)
        line_data[1].append(c_y)
        line.set_data(line_data[0], line_data[1])

        arm_1.set_data([0, x_1(th_1)], [0, y_1(th_1)])
        arm_2.set_data([x_1(th_1), x_2(th_1, th_2)], [y_1(th_1), y_2(th_1, th_2)])
        bob_1.set_data([x_1(th_1)], [y_1(th_1)])
        bob_2.set_data([x_2(th_1, th_2)], [y_2(th_1, th_2)])

        plt.pause(dt_i)
    plt.show()
    
    # Plot system
    plt.plot(t, th_1_l, t, th_2_l)
    plt.ylim(-np.pi, np.pi)
    plt.xlabel(r'$t$ (s)')
    plt.ylabel(r'$\theta_1, \theta_2$ (rad)')
    plt.title(r'Double Pendulum angles - $\theta$ vs $t$')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
