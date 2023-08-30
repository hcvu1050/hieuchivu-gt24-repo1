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
    
def batch_save_df_to_csv (file_name_dfs: dict, path):
    """
    save the DataFrames stored in a dict as csv file. The filenames are the keys in the dict
    """
    for key in file_name_dfs.keys():
        save_df_to_csv (
            path = path,
            filename = key,
            df = file_name_dfs[key]
        )
    
    print ("files saved to", path)
    for key in file_name_dfs.keys():
        print (key, ".csv")