import numpy as np
import pandas as pd
import librosa
import os 
from app.services.erreur import InvalidParameter
from app.services.pkl_service import get_path_audio


#Tranche correspond aux limites pour la repartition des temps

def encode_length(data,seuil,tranche={'tc':(0,4.75),'c' :(4.75,6),'m':(6,8),'l':(8,13),'tl':(13,100)},path_audio="",file_duration="audio_time.pkl",file_save="data.pkl"):
    seuil=seuil.lower()
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "..", "static", "wav")
    if(seuil in tranche.keys()):
        if(5 == 0): # verifie si le fichier avec les durées de chaque audio existe deja 
            duration=pd.read_pickle(file_duration)
        else :
            duration=pd.DataFrame(columns=["audio", "time", "timeSlice"])    #creer le fichier avec les durées de chaque audio
            pathsAudio = get_path_audio(data, 10000)
            for path in pathsAudio:
                full_path = os.path.join(STATIC_DIR, path)  # Construit le chemin absolu
                full_path = os.path.normpath(full_path)

                try:
                    y, fs = librosa.load(full_path)
                    time=len(y)/fs
                    print(f"Fichier chargé : {full_path}")

                    for k in tranche.keys():
                        if(time > tranche[k][0] and time <=tranche[k][1]):
                            timeSlice=k
                        
                    base_path, ext = os.path.splitext(path)
                    speaker_id = base_path.split('/')[2] 
                    pathReformed = f"{base_path}/{speaker_id}"
                    row=pd.DataFrame({"audio": [pathReformed],"time" : [time],"timeSlice":[timeSlice]})
                    
                    duration=pd.concat([duration,row],ignore_index=True)  
                except FileNotFoundError:
                    print(f"Fichier introuvable : {full_path}")

            duration.to_pickle(file_duration)
        
        res=data[data.index.isin(duration[duration["timeSlice"]==seuil]["audio"])]   #cherche les datas qui on pour timeSlice le seuil voulu 
        return res
    elif seuil == "all":
        return data
    else: 
        raise InvalidParameter(f"seuil must be in {tranche.keys()} (Capital except)")