import os
import pandas as pd

def save_df_to_csv (path, filename: str, df: pd.DataFrame ):
    """save pandas DataFrame as csv file within specified path

    Args:
        path (string)
        df (pandas DataFrame)
    """
    if not filename.endswith (".csv"): filename+= ".csv"
    
    os.makedirs (path, exist_ok= True)
    output_file = os.path.join(path, filename)
    df.to_csv (output_file, index= False)