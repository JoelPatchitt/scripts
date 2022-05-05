from pathlib import Path
import os, glob
import pandas as pd
import numpy as np

root = Path.cwd()

data_path = glob.glob(os.path.join(root, 'r-inputs', 'sub-*behaviourals.csv'))
data_path2 = glob.glob(os.path.join(root, 'r-inputs', 'sub-*peaks.csv'))

actual_responses = pd.DataFrame()
for sub in data_path:
    
    data = pd.read_csv(sub)
    data['condition'] = [np.nan]*len(data)
    print(data['px'], data['emotion'].value_counts())
    rep = 1
    base = 0
    for idx, row in data.iterrows():
        if np.isnan(row['sound_factor']) == True:
            continue
        else:
            new_rep = row['repetition_factor']  
            if rep == 3 and new_rep == 1:
                base +=3
            rep = row['repetition_factor']      
            cond = base+rep    
            cond = int(cond)
            data['condition'].iloc[idx] = cond
    for idx, row in data.iterrows():            
        if np.isnan(row['response']) == False:
            actual_responses = actual_responses.append(row)
responsidable = pd.DataFrame()
for sub in data_path2:
    data = pd.read_csv(sub)
    temp = data[np.isnan(data['response']) == False]
    
actual_responses.to_csv('response_all.csv', index = None)    
    










# responses = dict({'S01R01':[], 'S01R02':[], 'S01R03':[],
#               'S02R01':[], 'S02R02':[], 'S02R03':[],
#               'S03R01':[], 'S03R02':[], 'S03R03':[],
#               'S04R01':[], 'S04R02':[], 'S04R03':[],
#               })
# for idx, row in actual_responses.iterrows():
#     if row['sound_factor'] == 1:
#         if row['repetition_factor'] == 1:
#             responses['S01R01'].append(row)
#         if row['repetition_factor'] == 2:
#             responses['S01R02'].append(row)
#         if row['repetition_factor'] == 3:
#             responses['S01R03'].append(row)
#     if row['sound_factor'] == 2:
#         if row['repetition_factor'] == 1:
#             responses['S02R01'].append(row)
#         if row['repetition_factor'] == 2:
#             responses['S02R02'].append(row)
#         if row['repetition_factor'] == 3:
#             responses['S02R03'].append(row)
#     if row['sound_factor'] == 2:
#         if row['repetition_factor'] == 1:
#             responses['S03R01'].append(row)
#         if row['repetition_factor'] == 2:
#             responses['S03R02'].append(row)
#         if row['repetition_factor'] == 3:
#             responses['S03R03'].append(row)
#     if row['sound_factor'] == 2:
#         if row['repetition_factor'] == 1:
#             responses['S04R01'].append(row)
#         if row['repetition_factor'] == 2:
#             responses['S04R02'].append(row)
#         if row['repetition_factor'] == 3:
#             responses['S04R03'].append(row)

# keys = list(responses.keys())
# for key in keys:
#     temp = pd.DataFrame()
#     for item in responses[key]:
#         temp = temp.append(item)
#     responses[key] = temp
    
