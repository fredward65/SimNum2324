#!/usr/bin/env python3

import numpy as np


def linear_trajectory(p_0:list, p_f:list, angle:float, t_f:float=1, n:int=100) -> "tuple[np.ndarray, np.ndarray]":
    """
    Generate a linear trajectory with constant angle for a UR Arm in XZ planar configuration
    """
    t_vec = np.linspace(0, t_f, num=n)

    x_0, z_0 = p_0
    x_f, z_f = p_f
    x = np.linspace(x_0, x_f, num=n)
    z = np.linspace(z_0, z_f, num=n) 
    theta = angle * np.ones(n)
    
    trajectory = np.c_[x, z, theta]
    return t_vec, trajectory


def circular_trajectory(p_0:list, radius:float, angle:float, t_f:float=1, n:int=100) -> "tuple[np.ndarray, np.ndarray]":
    """
    Generate a circular trajectory with constant angle for a UR Arm in XZ planar configuration
    """
    t_vec = np.linspace(0, t_f, num=n)
    
    # Modify these lines
    x_0 = p_0[0]
    z_0 = p_0[1]
    x = np.linspace(x_0, x_0, num=n)
    z = np.linspace(z_0, z_0, num=n) 
    theta = angle * np.ones(n)
    
    trajectory = np.c_[x, z, theta]
    return t_vec, trajectory


def square_trajectory(p_0:list, side:float, angle:float, t_f:float=1, n:int=100) -> "tuple[np.ndarray, np.ndarray]":
    """
    Generate a square trajectory with constant angle for a UR Arm in XZ planar configuration
    """
    t_vec = np.linspace(0, t_f, num=n)
    
    p_l = [p_0]
    x_0, z_0 = p_0 
    for i in range(3):
        x_0 += side * np.cos(angle + .5*np.pi*i)
        z_0 += side * np.sin(angle + .5*np.pi*i)
        p_l.append([x_0, z_0])
    p_l.append(p_0)

    l_p = len(p_l) - 1
    x = np.array([np.linspace(p_l[i][0], p_l[i+1][0], num=n//l_p) for i in range(l_p)]).ravel()
    z = np.array([np.linspace(p_l[i][1], p_l[i+1][1], num=n//l_p) for i in range(l_p)]).ravel()

    theta = angle * np.ones(n)
    
    trajectory = np.c_[x, z, theta]
    return t_vec, trajectory


def polygon_trajectory(p_0:list, edges:float, radius:float, angle:float, t_f:float=1, n:int=100) -> "tuple[np.ndarray, np.ndarray]":
    """
    Generate a regular polygon trajectory with constant angle for a UR Arm in XZ planar configuration
    """
    t_vec = np.linspace(0, t_f, num=n)
    
    # Modify these lines
    x_0 = p_0[0]
    z_0 = p_0[1]
    x = np.linspace(x_0, x_0, num=n)
    z = np.linspace(z_0, z_0, num=n) 
    theta = angle * np.ones(n)
    
    trajectory = np.c_[x, z, theta]
    return t_vec, trajectory


def main():
    pass


if __name__ == "__main__":
    main()
