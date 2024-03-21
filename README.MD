# Simulation Numérique 2023-2024
Le repo officiel du module.

<p float="left">
    <img src="https://www.tetras.univ-smb.fr/themes/custom/tetras_b5/logo.svg" width="30%" alt="Logo Tetras"/>
    <img src="https://www.univ-smb.fr/iut-annecy/wp-content/uploads/sites/98/2022/09/logo-iut-annecy-233x86px1.svg" width="30%" alt="Logo IUT"/>
    <img src="https://www.univ-smb.fr/wp-content/themes/usmb/assets/img/logo.svg" width="30%" alt="Logo USMB"/>
</p>

⚠ Ce code est à exécuter sur un Dev Container ⚠

## Contenu
Dans ce Dev Container, vous trouverez :
- Exercices à développer sur **JavaScript** en utilisant **p5.js**
- Fichiers de base pour simuler et contrôler un bras UR3 sur ROS/Gazebo
- Autres fichiers et documents de support

## Mode d'emploi
Suivez les instructions pour garantir le bon fonctionnement du code.

### Préparation
1. Téléchargez et installez [Docker Desktop](https://www.docker.com/products/docker-desktop/) et [Visual Studio Code](https://code.visualstudio.com/download)
2. Lancez Docker
3. Lancez VSCode et installez l'extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Lancement du Container
1. Clonez ce projet sur votre disque local.
   - Téléchargement ZIP : Décompressez le .zip sur un emplacement local (e.g. Bureau, Documents, Téléchargement sur Disque C)
2. Ouvrez le dossier décompressé avec VSCode. Assurez-vous d'être bien placé sur le dossier racine `SimNum2324`.
3. Lancez le container avec la palette de commandes : \
`Ctrl+Shift+P > "Dev Container: Rebuild and Reopen in Container"`

### Serveur HTTP (code JavaScript/p5.js)
Pour explorer et lancer les exercises p5.js: \
- Ouvrez le code avec Live Server : \
`Ctrl+Shift+P > "Live Server: Open with Live Server"` \
où
- Appuyez `Go live` en bas à droite.

### Interface noVNC (fenêtres Python et ROS/Gazebo)
Pour visualizer l'interface du container, ouvrez l'adresse suivante sur un Simple Browser : \
`Ctrl+Shift+P > "Simple Browser: Show > "http:\\localhost:6080"` \
Tapez `vscode` pour le mot de passe du noVNC.

#### Lancement du robot
1. Pour lancer le robot, ouvrez un terminal bash (`Ctrl+Shift+ù`) et executez : \
`roslaunch modmat_toolbox basic_arm_bringup.launch`
2. Pour vérifier le bon fonctionnement du robot, ouvrez un autre terminal et executez : \
`rosrun modmat_toolbox planar_demo.py` \
Le robot devra faire un mouvement basique.
