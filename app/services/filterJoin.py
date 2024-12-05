from app.services.filterGender import encode_genre
from app.services.filterLength import encode_length
import numpy as np
import pandas as pd
#pandas version '2.2.3' 

#Permet de faire un trie avec plusieurs elements 
def filterJoin(meta,data,file,genre=None,seuil=None,path_audio=""):
    modif=False
    if genre is not None :
        modif=True
        ##encode_genre(meta,data,genre,file=file)
        data = encode_genre(meta,data,genre,file=file)
    if seuil is not None :
        modif=True
        data = encode_length(data,seuil,file_save=file,path_audio=path_audio)
    if not modif:
        data.to_pickle(file)
    data.to_pickle(file)
    return data


#filterJoin(meta,data,"../data/data/voxceleb1/trainTcM.pkl",genre='M',seuil='tl',path_audio='../data/data/voxceleb1/')