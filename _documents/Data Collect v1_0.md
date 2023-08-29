# Data Collect V1.0
# 1- Collect Data from MITRE ATT&CK
- `enterprise-attack.json` is MITRE ATT&CK data, downloaded from [cti/enterprise-attack/enterprise-attack.json at master · mitre/cti (github.com)](https://github.com/mitre/cti/blob/master/enterprise-attack/enterprise-attack.json)
	- Current version: **ATT&CK v13.1 Enterprise**
- Load the data from `enterprise-attack.json` into stix2's `MemoryStore` Object. It is an interface through which we can obtain MITRE ATT&CK data. [document](https://stix2.readthedocs.io/en/latest/api/datastore/stix2.datastore.memory.html)
```
from stix2 import MemoryStore
attackdata = MemoryStore ()
attackdata.load_from_file ( 'data/enterprise-attack.json')
```
# 2- Extract data
- Using module from [`mitreattack.attackToExcel.stixToDf`](https://github.com/mitre-attack/mitreattack-python/blob/master/mitreattack/attackToExcel/README.md#stixtodf), multiple data from MITRE ATT&CK can be processed as [Pandas](https://pandas.pydata.org/) DataFrames
```
import mitreattack.attackToExcel.stixToDf as stixToDf
```
## 2-a Technique data
```
techniques_data = stixToDf.techniquesToDf(attackdata, "enterprise-attack")
```
- `techniques_data` is a python `dict` that stores multiple DataFrames of different Technique data. The keys in `techniques_data` include:
	- `'techniques'`: list of all different Techniques, *we will use this table*
	- `'procedure examples'`
	- `'associated mitigations'`: list of all Mitigations that can prevent each Technique, *we will use this table*
	- `'citations'`
- we will extract and save the DataFrames for `'techniques'` and `'associated mitigations'` 
```
techniques_df = techniques_data["techniques"]
techniques_mitigations_df = techniques_data['associated mitigations']
```
## 2-b Group data
```
groups_data = stixToDf.groupsToDf (attackdata)
```
- `groups_data` is a python `dict` that stores multiple DataFrames of different Group data. The keys in `groups_data` include:
	- `'groups'`: list of all different Groups, *we will use this table*
	- `'associated software'`, list of all Software used by each Group, *we will use this table*
	- `'techniques used'`, list of all Techniques used by each Group, *we will use this table*
	- `'attributed campaigns'`
	- `'citations'`
- we will extract and save the DataFrames for `'group'`, `'associated software'`, and `'techniques used'`
```
groups_df = groups_data['groups']
groups_techniques_df = groups_data['techniques used']
groups_software_df = groups_data['associated software']
```

> SUMMARY
> 
> After downloading MITRE ATT&CK data (v13.1 Enterprise), we extract the following pandas DataFrames and save as csv files:
> 1. `technique_df.csv`: list of all Techniques
> 2. `techniques_mitigations_df.csv`: list of all Mitigations for each Techniques
> 3. `groups_df.csv`: list of all Groups
> 4. `groups_techniques_df.csv`: list of all Techniques used by each Group
> 5. `groups_software_df.csv`: list of all Software used by each Group