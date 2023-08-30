from stix2 import MemoryStore
import mitreattack.attackToExcel.stixToDf as stixToDf
import pandas as pd

import sys
import os

# Get the root directory of the project
root_folder = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))

file_path = os.path.join(root_folder, 'data', 'enterprise-attack.json')


def data_collect(file_path = file_path):
    
    attackdata = MemoryStore ()
    attackdata.load_from_file (file_path )
    """
    collect_data v1.0
    
    reads 'enterprise-attack.json' from `path`
    
    """
    techniques_data = stixToDf.techniquesToDf(attackdata, "enterprise-attack")
    groups_data = stixToDf.groupsToDf (attackdata)
    
    techniques_df = techniques_data["techniques"]
    techniques_mitigations_df = techniques_data['associated mitigations']
    groups_df = groups_data['groups']
    groups_techniques_df = groups_data['techniques used']
    groups_software_df = groups_data['associated software']
        
    return techniques_df, techniques_mitigations_df, groups_df, groups_techniques_df, groups_software_df