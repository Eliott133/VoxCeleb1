#!/bin/bash
#SBATCH --job-name=f0_extraction        # Nom du job
#SBATCH --output=f0_extraction.out      # Fichier de sortie
#SBATCH --error=f0_extraction.err       # Fichier d'erreurs
#SBATCH --time=04:00:00                 # Temps maximal d'exécution (hh:mm:ss)
#SBATCH --cpus-per-task=8               # Nombre de processeurs alloués
#SBATCH --gpus=1                        # Nombre de GPU alloués
#SBATCH --mem=16G                       # Mémoire allouée
#SBATCH --partition=gpu                 # Partition GPU (ou autre partition spécifique)
#SBATCH --mail-user=Eliott.Maubert.Etu@univ-lemans.fr
#SBATCH --mail-type=ALL

# Charger les modules nécessaires
module load python/3.9  # Exemple, ajustez selon votre système
module load cuda/11.8   # Exemple, ajustez selon la version CUDA
module load anaconda/2023

# Activer l'environnement virtuel si nécessaire
source activate f0_env

# Exécuter le script Python
python audio_feature_flow.py
