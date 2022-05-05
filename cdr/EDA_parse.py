from pathlib import Path
import os, glob
import pandas as pd, numpy as np, matplotlib.pyplot as plt

# Python program to find difference between two numbers

def difference(a, b):
    # a is greater than b
    if a > b:
        diff = a - b
    # a is less than b
    else:
        diff = b - a
    # return value
    return diff

# Establish directories for EDA and onset data
root = Path.cwd()
eda_dir = os.path.join(root, 'EDA')
ons_dir = os.path.join(root, 'outputs')

# Grab all related files in these directories
eda_data = glob.glob(os.path.join(eda_dir, '*.csv'))
ons_data = glob.glob(os.path.join(ons_dir, '*onsets.csv'))
all_eda = pd.DataFrame([np.nan]*1280000)
for e, o in zip(eda_data, ons_data):
    
    eda = pd.read_csv(e, header=None); ons = pd.read_csv(o, header=None)
    
    # Label onset data and identify sound triggers
    ons['id'] = [0]*len(ons)
    for idx, row in ons.iterrows():
        if idx <= 9:
            row['id'] = 0
        else:
            if idx == 10:
                row['id'] = 1
                counter = 0
            else:
                if idx == len(ons)-1:
                    row['id'] = 4
                else:
                    if counter <50:
                        if counter%2 == 0:
                            row['id'] = 2
                            counter+=1
                        else:
                            row['id'] = 3
                            counter+=1
                    else:
                        row['id'] = 1
                        counter = 0
    sounds = ons[0][ons['id'] == 1]
    end = ons[0][ons['id'] == 4]
    
    # Map sound triggers onto EDA data
    sound_df = pd.DataFrame([min(eda[0])]*len(eda[0]))    
    for row in sounds:
        sound_df.iloc[row] = max(eda[0])
    
    # Plot EDA data and sound triggers
    # plt.plot(eda, color='r', label='EDA', linewidth=0.5)
    # plt.plot(sound_df, color='g', label='Onsets', linewidth=0.1)
    # plt.show()

    # Zero EDA data for means plotting
    temp_eda = eda[0].iloc[sounds.iloc[0]:end.iloc[0]]
    temp_eda.reset_index(drop=True, inplace=True)

    if len(temp_eda) > len(all_eda):
        print([e[-10:][:-8]])
        print('missed_case')
        
        
        
        
    last = temp_eda[0]    
    for i, row in enumerate(temp_eda):
        if difference(temp_eda[i], last) > 0.005:
            temp_eda[i] = last
        last = temp_eda[i]
        
        
        
        
    # # Remove outliers using Quartiles
    # temp_eda = pd.to_numeric(temp_eda, errors='coerce')
    # Q1 = temp_eda.quantile(0.25)
    # Q3 = temp_eda.quantile(0.75)
    # IQR = Q3 - Q1    
    # temp_eda = np.where(temp_eda < (Q1 - 1.5 * IQR), temp_eda.quantile(0.50), temp_eda)

    # plt.plot(temp_eda, color='r', label='EDA', linewidth=0.5)
    # plt.plot(sound_df, color='g', label='Onsets', linewidth=0.1)
    # plt.show()

    all_eda[e[-10:][:-8]] = pd.Series(temp_eda)
    

a = all_eda.mean(axis=1)    
a = a[a > -100]

c = sounds-sounds.iloc[0]
b = sound_df.iloc[sounds.iloc[0]:]
b.reset_index(drop=True, inplace=True)
plt.plot(a, color='r', label='EDA', linewidth=0.5)
plt.plot(b, color='g', label='Onsets', linewidth=0.1)
plt.show()
