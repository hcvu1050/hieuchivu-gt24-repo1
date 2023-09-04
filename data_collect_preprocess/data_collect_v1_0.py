from stix2 import MemoryStore
import mitreattack.attackToExcel.stixToDf as stixToDf
import pandas as pd

import sys
import os
# Get the root directory of the project
root_folder = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
mitre_attck_file_path = os.path.join(root_folder, 'data', 'enterprise-attack.json')
data_dir = os.path.join(root_folder, 'data')

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
        print (key, ".csv", sep = '')

def data_collect(file_path = mitre_attck_file_path):
    """
    v1.0
    
    Reads 'enterprise-attack.json' from `path`.
    Returns the following DataFrames:
        techniques_df, \n
        techniques_mitigations_df, \n
        groups_df, \n
        groups_techniques_df, \n
        groups_software_df\n
    """
    
    attackdata = MemoryStore ()
    attackdata.load_from_file (file_path )
    techniques_data = stixToDf.techniquesToDf(attackdata, "enterprise-attack")
    groups_data = stixToDf.groupsToDf (attackdata)
    
    techniques_df = techniques_data["techniques"]
    techniques_mitigations_df = techniques_data['associated mitigations']
    groups_df = groups_data['groups']
    groups_techniques_df = groups_data['techniques used']
    groups_software_df = groups_data['associated software']
        
    return techniques_df, techniques_mitigations_df, groups_df, groups_techniques_df, groups_software_df


def data_collect_and_save(data_dir = data_dir):
    """
    v1.0
    
    save the following DataFrames as csv in specifed path:
        techniques_df, \n
        techniques_mitigations_df, \n
        groups_df, \n
        groups_techniques_df, \n
        groups_software_df\n
    
    """
    techniques_df, techniques_mitigations_df, groups_df, groups_techniques_df, groups_software_df = data_collect()
    
    dfs = {
    "techniques_df" : techniques_df,
    "techniques_mitigations_df" : techniques_mitigations_df,
    "groups_df": groups_df,
    "groups_techniques_df" : groups_techniques_df,
    "groups_software_df" : groups_software_df,
    }
    batch_save_df_to_csv (dfs, data_dir)
    return techniques_df, techniques_mitigations_df, groups_df, groups_techniques_df, groups_software_df
    
    