from app.services.filterGender import encode_genre
from app.services.filterLength import encode_length
import numpy as np
import pandas as pd

#Permet de faire un trie avec plusieurs elements 
def filterJoin(meta,data,file,genre=None,seuil=None,path_audio=""):
    modif=False
    if genre is not None :
        modif=True
        data = encode_genre(meta,data,genre,file=file)
    if seuil is not None :
        modif=True
        data = encode_length(data,seuil,file_save=file,path_audio=path_audio)
    if not modif:
        data.to_pickle(file)
    data.to_pickle(file)
    return data