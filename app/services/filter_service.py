import numpy as np
import pandas as pd
import os
import json

FILTER_FILE = os.path.join(os.path.dirname(__file__), "filters.json")

def filters_pkl(meta, data, gender, fileName, time_filter=None):
    # Filtrage par genre
    print(fileName)
    gender = gender.lower()
    genderMetaAvailable = meta['Gender'].unique()
    if gender in genderMetaAvailable:
        filtered_meta = meta[meta['Gender'] == gender]
        idVox = np.array(filtered_meta['VoxCeleb1 ID'])
        filtered_data = data[data['speaker_id'].isin(idVox)]
    else:
        return f"gender must be in {genderMetaAvailable} (Capital except)"

    # Filtrage par durée (si time_filter est fourni)
    if time_filter and time_filter != "indifferent":
        # Dictionnaire des tranches de durée
        tranche = {
            'tc': (0, 3),
            'c': (3, 5),
            'm': (5, 8),
            'l': (8, 20),
            'tl': (20, 55)
        }
        
        time_filter = time_filter.lower()  # Convertir en minuscule pour correspondre au dictionnaire
        if time_filter in tranche:
            # Calculer la durée totale de chaque audio pour chaque speaker
            duration = pd.DataFrame(columns=["speaker_id", "time", "timeSlice"])
            for val in filtered_data["speaker_id"].unique():
                time = len(filtered_data[filtered_data['speaker_id'] == val]) / 16  # fs = 16 (échantillonnage)
                if time > 0:
                    if tranche['tc'][0] < time <= tranche['tc'][1]:
                        timeSlice = 'tc'
                    elif tranche['c'][0] < time <= tranche['c'][1]:
                        timeSlice = 'c'
                    elif tranche['m'][0] < time <= tranche['m'][1]:
                        timeSlice = 'm'
                    elif tranche['l'][0] < time <= tranche['l'][1]:
                        timeSlice = 'l'
                    elif time > tranche['tl'][0]:
                        timeSlice = 'tl'
                    else:
                        timeSlice = None
                    
                    # Ajout du speaker_id et de la tranche de temps
                    row = pd.DataFrame({"speaker_id": [val], "time": [time], "timeSlice": [timeSlice]})
                    duration = pd.concat([duration, row], ignore_index=True)
            
            # Filtrer les données par tranche de durée
            filtered_data = filtered_data[filtered_data['speaker_id'].isin(duration[duration["timeSlice"] == time_filter]["speaker_id"])]
        else:
            raise f"time_filter must be in {tranche.keys()} (Capital except)"

    # Sauvegarde du fichier filtré
    filtered_data.to_pickle(fileName)
    return fileName

def load_filters():
    if os.path.exists(FILTER_FILE):
        with open(FILTER_FILE, "r") as f:
            return json.load(f)
    return []

def save_filters(filters):
    with open(FILTER_FILE, "w") as f:
        json.dump(filters, f, indent=4)