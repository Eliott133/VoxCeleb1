import numpy as np
import pandas as pd

from app.services.erreur import InvalidParameter
#pandas version '2.2.3' 

def encode_genre(meta,data,gender,file="data.pkl"):
    gender = gender.lower()
    genderMetaAvailable = meta['Gender'].unique()
    if gender in genderMetaAvailable:
        filtered_meta = meta[meta['Gender'] == gender]
        idVox = np.array(filtered_meta['VoxCeleb1 ID'])
        filtered_data = data[data['speaker_id'].isin(idVox)]
        return filtered_data
    elif gender == "all":
        return data
    else: 
        raise InvalidParameter(f"gender must be in {genderMetaAvailable} (Capital except)")

"""
meta = pd.read_csv("../data/data/voxceleb1/meta.csv",delimiter="\t" )
data= pd.read_pickle("../data/data/voxceleb1/train.pkl")
encode_genre(meta,data,"m","../data/data/voxceleb1/trainM.pkl")
encode_genre(meta,data,"f","../data/data/voxceleb1/trainF.pkl")
"""