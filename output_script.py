'''
Script permettant de nettoyer les fichiers de sortie
ou de crée le dossier de sortie à la première execution du projet
'''

import os, shutil

output_folder = './app/output/'

if(os.path.exists(output_folder)):
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Problème lors de la supression %s. Raison: %s' % (file_path, e))
else:
    os.makedirs(output_folder)