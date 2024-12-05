# Lancement de l'application web 


## Cloner le projet
```bash
git clone https://git.univ-lemans.fr/s2100554/projet-m1.git
```
## Installation et environnement

1) Assurez-vous que Conda est installé : Si Conda n'est pas déjà installé, téléchargez et installez Miniconda ou Anaconda.
```bash
conda --version
```
2) Créez l'environnement à partir du fichier environment.yaml
```bash
conda env create -f environment.yaml
```
3) Activez l'environnement
```bash
conda activate nom-de-l-environnement
```
4) Vérifiez que les dépendances sont correctement installées :
```bash
conda list
```
5) Mise à jour de l'environnement (si nécessaire) :
```bash
conda env update --file environment.yaml --prune
```

## Lancement du serveur

A la racine du projet
```bash
python run.py
```
Ceci va démarrer le serveur Flask en localhost sur le port 5000 : 
```bash
127.0.0.1:5000
```

En cas de conflit de port :
```bash
flask run --port=8080
```

## Route

1) **/** : Pour télécharger les données filtrées
2) **/audio** : Pour écouter un fichier de données 
3) **/manage_filters** : Pour gérer les filtres
4) **/list_filters** : Pour afficher les filtres
5) **/delete_filter/<filter_name>** : Pour supprimer un filtre en fonction du nom du filtre

## Technologie utilisé 

| Technologie | Version      |
| ----------- | ------------ |
| Flask       | 3.1.0        |
| Python      | 3.9          |
| Conda       | 24.7.1       |
| Pandas      | 2.2.2        |
| Numpy       | 1.26.4       |
| Librosa     | 0.10.2.post1 |

