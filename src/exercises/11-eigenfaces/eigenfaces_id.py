#!/usr/bin/env python3

import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib.widgets import Slider


def main():
    """ Eigenfaces - https://github.com/jakeoeding/eigenfaces """
    # Olivetti Dataset from https://github.com/lloydmeta/Olivetti-PNG
    dir_path = os.path.dirname(os.path.abspath(__file__)) + '/datasets/olivetti/'
    img_names = os.listdir(dir_path)
    img_names = img_names[:len(img_names)//5]

    # Load and show all faces
    faces = [plt.imread(dir_path + file_name) for file_name in img_names]
    dim = faces[0].shape
    training_faces = []
    test_faces = []
    for x in range(len(faces)//10):
        for i in range(5):
            training_faces.append(faces[i + 10*x])
            test_faces.append(faces[i + 5 + 10*x])

    fig_1 = plt.figure()
    fig_2 = plt.figure()
    fig_1.suptitle("Training Faces")
    fig_2.suptitle("Test Faces")
    for i, (training_face, test_face) in enumerate(zip(training_faces, test_faces)):
        ax_1 = fig_1.add_subplot(4, len(training_faces)//4, i+1)
        ax_1.imshow(training_face.reshape(dim), cmap=plt.get_cmap('gray'))
        ax_1.set_xticks([])
        ax_1.set_yticks([])
        ax_2 = fig_2.add_subplot(4, len(test_faces)//4, i+1)
        ax_2.imshow(test_face.reshape(dim), cmap=plt.get_cmap('gray'))
        ax_2.set_xticks([])
        ax_2.set_yticks([])
    plt.show()

    training_faces = np.array(training_faces).reshape((-1, dim[0]*dim[1]))
    test_faces = np.array(test_faces).reshape((-1, dim[0]*dim[1]))

    # Mean Face
    mean_face = np.mean(training_faces, axis=0)
    plt.imshow(mean_face.reshape((dim[0], dim[1])), cmap=plt.get_cmap('gray'))
    plt.xticks([])
    plt.yticks([])
    plt.title("Mean/Average face")
    plt.show()

    # Normalised Faces
    fig = plt.figure()
    fig.suptitle("Normalised faces")
    faces_normalised = training_faces - mean_face
    for i, face_normalised in enumerate(faces_normalised):
        fig.add_subplot(4, len(faces_normalised)//4, i+1)
        plt.imshow(face_normalised.reshape((dim[0], dim[1])), cmap=plt.get_cmap('gray'))
        plt.xticks([])
        plt.yticks([])
    plt.show()

    # Singular Value Decomposition X = U Sigma V*
    u, s, v = np.linalg.svd(faces_normalised @ faces_normalised.T, full_matrices=False)
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title("Singular values - Semilog Y")
    plt.semilogy(s, '-x')
    plt.subplot(1, 2, 2)
    plt.title("Singular values - Cumulative Sum")
    plt.plot(np.cumsum(s), '-x')
    plt.hlines(.75 * np.sum(s), 0, s.shape[0])
    plt.tight_layout()
    plt.show()

    # Reduced basis from Eigens
    idx_lim = np.where(np.cumsum(s) < .75 * np.sum(s))[0][-1] + 1
    u_r = u[:, :idx_lim]

    # Project faces on reduced basis
    proj_faces = np.dot(u_r.T, faces_normalised)
    fig = plt.figure()
    fig.suptitle("Eigenfaces")
    for i, proj_face in enumerate(proj_faces):
        cols = proj_faces.shape[0]
        fig.add_subplot(4 + cols%4, cols//4, i+1)
        plt.imshow(proj_face.reshape((dim[0], dim[1])), cmap=plt.get_cmap('gray'))
        plt.xticks([])
        plt.yticks([])
    plt.show()

    # Compute weights for each face
    w = np.array([np.dot(proj_faces, face) for face in faces_normalised])
    ax = plt.figure().add_subplot(projection='3d')
    xw, yw = np.meshgrid(np.arange(w.shape[0]), np.arange(w.shape[1]))
    xw, yw, zw = xw.ravel(), yw.ravel(), np.zeros_like(xw).ravel()
    ax.bar3d(xw, yw, zw, 0.5, 0.5, w.ravel())
    plt.show()

    # Identify test faces
    test_idx = [i + 5*x for x in range(w.shape[0]//5) for i in range(2)]
    for test_face in test_faces[test_idx]:
        w_i = np.dot(proj_faces, test_face - mean_face)
        idx_1 = np.linalg.norm(w - w_i, axis=1).argsort()[0]
        idx_2 = np.dot(w, w_i).argsort()[-1]
        matching_face_1 = training_faces[idx_1]
        matching_face_2 = training_faces[idx_2]

        def show_image(image, weights, sp_i, txt):
            plt.subplot(3,2, sp_i)
            plt.title(txt)
            plt.imshow(image.reshape((dim[0], dim[1])), cmap=plt.get_cmap('gray'))
            plt.xticks([])
            plt.yticks([])
            plt.subplot(3, 2, sp_i+1)
            plt.bar(np.arange(weights.shape[0]), weights)
        
        show_image(test_face, w_i, 1, "Test Face")
        show_image(matching_face_1, w[idx_1], 3, "Match - Error Norm")
        show_image(matching_face_2, w[idx_2], 5, "Match - Dot Product")

        plt.show()
    

if __name__ == '__main__':
    main()
