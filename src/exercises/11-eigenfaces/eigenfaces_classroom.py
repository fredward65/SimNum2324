#!/usr/bin/env python3

import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib.widgets import Slider


def rgb2gray(rgb):
    gray = rgb if not len(rgb.shape)>2 else np.dot(rgb[...,:3], [.2989, .5870, .1140])
    return gray


def basis_from_eigens(cov_mat):
    # Eigenvalues and Eigenvectors
    eigvals, eigvecs = np.linalg.eig(cov_mat)
    eig_idx = np.flip(eigvals.argsort())
    eigvals = eigvals[eig_idx]
    eigvecs = eigvecs[:, eig_idx]

    return eigvecs, eigvals


def basis_from_svd(matrix):
    # Singular Value Decomposition X = U Sigma V*
    u, s, v = np.linalg.svd(matrix, full_matrices=False)

    return u, s


def main():
    """ Eigenfaces - https://silanus.fr/sin/?p=785 """
    dir_path = os.path.dirname(os.path.abspath(__file__)) + '/datasets/classroom/'
    img_names = os.listdir(dir_path)

    # Load and show all faces
    fig = plt.figure()
    fig.suptitle("Faces")
    dim = 0
    faces = []
    for i, file_name in enumerate(img_names):
        img_i = rgb2gray(plt.imread(dir_path + file_name))
        dim = img_i.shape
        faces.append(img_i.ravel())
        fig.add_subplot(3, len(img_names)//3, i+1)
        plt.imshow(img_i, cmap=plt.get_cmap('gray'))
        plt.xticks([])
        plt.yticks([])
    plt.show()

    faces = np.array(faces).reshape((len(img_names), -1))
 
    # Mean Face
    mean_face = np.mean(faces, axis=0)
    plt.imshow(mean_face.reshape((dim[0], dim[1])), cmap=plt.get_cmap('gray'))
    plt.xticks([])
    plt.yticks([])
    plt.title("Mean/Average face")
    plt.show()

    # Normalised Faces
    fig = plt.figure()
    fig.suptitle("Normalised faces")
    faces_normalised = faces - mean_face
    for i, face_normalised in enumerate(faces_normalised):
        fig.add_subplot(3, len(img_names)//3, i+1)
        plt.imshow(face_normalised.reshape((100, 100)), cmap=plt.get_cmap('gray'))
        plt.xticks([])
        plt.yticks([])
    plt.show()

    # Covariance Matrix
    cov_mat = np.corrcoef(faces_normalised)
    plt.imshow(cov_mat.reshape((faces_normalised.shape[0], -1)), cmap=plt.get_cmap('gray'))
    plt.xticks(range(12), [name.split('_')[0] for name in img_names], rotation=90)
    plt.yticks(range(12), [name.split('_')[0] for name in img_names])
    plt.title("Covariance Matrix")
    plt.show()

    # Basis
    u_l, s_l = [], []
    # BasisFrom Eigens
    eigvecs, eigvals = basis_from_eigens(cov_mat)
    u_l.append(eigvecs)
    s_l.append(eigvals)
    # Basis from SVD (Principal Component Analysis)
    u, s = basis_from_svd(faces_normalised)
    u_l.append(u)
    s_l.append(s)

    for u_i, s_i in zip(u_l, s_l):
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.title("Singular values - Semilog Y")
        plt.semilogy(s_i, '-x')
        plt.subplot(1, 2, 2)
        plt.title("Singular values - Cumulative Sum")
        plt.plot(np.cumsum(s_i), '-x')
        plt.hlines(.9 * np.sum(s_i), 0, s_i.shape[0])
        plt.tight_layout()
        plt.show()

        # Reduced basis from Eigens
        idx_lim = np.where(np.cumsum(s_i) < .9 * np.sum(s_i))[0][-1] + 1
        u_r = u_i[:, :idx_lim]

        # Project faces on reduced basis
        proj_faces = np.dot(u_r.T, faces_normalised)
        fig = plt.figure()
        fig.suptitle("Eigenfaces")
        for i, proj_face in enumerate(proj_faces):
            cols = proj_faces.shape[0]
            fig.add_subplot(cols//3, 3 + cols%3, i+1)
            plt.imshow(proj_face.reshape((dim[0], dim[1])), cmap=plt.get_cmap('gray'))
            plt.title('Eigenface %i' % (i+1))
            plt.xticks([])
            plt.yticks([])
        plt.show()

        # Compute weights for each face
        w = np.array([np.dot(proj_faces, face) for face in faces_normalised])

        w_idx = w[:,0].argsort()
        w = w[w_idx]
        img_names = [img_names[w_idx_i] for w_idx_i in w_idx]

        # Reconstruct faces
        fig = plt.figure()
        fig.suptitle("Closest face: " + img_names[0])
        rec_face = np.dot(w[0], proj_faces) + mean_face
        fig.add_subplot(121)
        fig.subplots_adjust(bottom=.2)
        plt.xticks([])
        plt.yticks([])
        img_handle = plt.imshow(rec_face.reshape((dim[0], dim[1])), cmap=plt.get_cmap('gray'))
        
        fig.add_subplot(122)
        bar_handle = plt.bar(1 + np.arange(len(w[0])), w[0])
        plt.xticks([])
        plt.ylim(np.min(w), np.max(w))
        ax_w = fig.add_axes([.15, .05, .75, .1])
        w_slider = Slider(ax=ax_w, label='W Mix', valmin=0, valmax=len(w)-1, valinit=0)
        
        def update(val):
            lo, hi = int(np.floor(val)), int(np.ceil(val))
            fac = val - lo
            w_i = (1-fac) * w[lo] + fac * w[hi]
            rec_face = np.dot(w_i, proj_faces) + mean_face
            img_handle.set_data(rec_face.reshape((dim[0], dim[1])))
            for bar, w_i_j in zip(bar_handle, w_i):
                bar.set_height(w_i_j)
            fig.suptitle("Closest face: " + img_names[int(np.round(val))])

        w_slider.on_changed(update)
        plt.show()
    

if __name__ == '__main__':
    main()
