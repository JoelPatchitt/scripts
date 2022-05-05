from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import os, glob
from datamunge import by_condition


subj_data = list(glob.glob(os.path.join(Path.cwd(), 'r-inputs', 'sub-*peaks.csv')))

for sub in subj_data:
    data = pd.read_csv(sub)
    split_data = by_condition(data['sound_factor'], data['repetition_factor'], dataset=data)
    
    cond = split_data['11']
    cond['hr'] = [np.nan]*len(cond)
    for idx, row in cond.iterrows():
        cond['hr'].iloc[idx] = (((1-(row['IBI']/1000))*60)+60)
        
    
    plt.plot(np.arange(len(cond)), cond['hr'], linewidth=0.5)
    
    rolling = cond['hr'].rolling(5, min_periods=1)
    rolling_mean = rolling.mean()
    
    plt.plot(np.arange(len(cond)), rolling_mean)
    
    plt.savefig(os.path.join(Path.cwd(), 'png', sub[32:][:-4]) + '.png')
    plt.close()