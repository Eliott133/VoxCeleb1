import numpy as np
import os
import pandas as pd


def get_path_audio(pkl_file: pd.DataFrame, max_path=10) -> str:
    paths = []
    for path in np.array(pkl_file.index):
        parentPath = os.path.dirname(path)
        paths.append(parentPath + ".wav")
    return paths[:max_path]
