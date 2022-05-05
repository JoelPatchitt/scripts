from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import os, glob, copy

def calc_rr_segment(rr_source, b_peaklist):
    
    rr_list = [rr_source[i] for i in range(len(rr_source)) if b_peaklist[i] + b_peaklist[i+1] == 2]
    rr_mask = [0 if (b_peaklist[i] + b_peaklist[i+1] == 2) else 1 for i in range(len(rr_source))]
    rr_masked = np.ma.array(rr_source, mask=rr_mask)
    rr_diff = np.abs(np.diff(rr_masked))
    rr_diff = rr_diff[~rr_diff.mask]
    rr_sqdiff = np.power(rr_diff, 2)

    return rr_list, rr_diff, rr_sqdiff

subj_data = list(glob.glob(os.path.join(Path.cwd(), 'r-inputs', 'sub-*peaks.csv')))

# Split data into conditions
peaks = dict({'S01R01':pd.DataFrame(),'S01R02':pd.DataFrame(),'S01R03':pd.DataFrame(),
              'S02R01':pd.DataFrame(),'S02R02':pd.DataFrame(),'S02R03':pd.DataFrame(),
              'S03R01':pd.DataFrame(),'S03R02':pd.DataFrame(),'S03R03':pd.DataFrame(),
              'S04R01':pd.DataFrame(),'S04R02':pd.DataFrame(),'S04R03':pd.DataFrame(),})
rmssd = copy.copy(peaks)

keyG = list(peaks.keys())
for sub in subj_data:
    # Read in subject data
    i=0
    data = pd.read_csv(sub, index_col=0)
    
    for s in range(1, 5):
        for r in range(1, 4):
            temp = data[data['sound_factor'] == s]
            temp = temp[temp['repetition_factor'] == r]
            peaks[keyG[i]] = temp
            i +=1

    # calculate RMSSD
    for key, val in peaks.items():
        b_peaklist = val['exclusion_factor'].replace({0:1, 1:0})
        b_peaklist = b_peaklist.append(pd.Series(0))
        
        val.reset_index(drop=True, inplace=True)
        b_peaklist.reset_index(drop=True, inplace=True)
        rr, rrd, rr_sqdiff = calc_rr_segment(val['IBI'], b_peaklist)
        
        
        
        rmout = np.sqrt(np.mean(rr_sqdiff))
        rmssd[key] = rmssd[key].append(pd.Series(rmout), ignore_index = True)
        
means = [val.mean() for key, val in rmssd.items()]
plt.plot(rmssd.keys(), means)

a = pd.DataFrame()
for key, val in rmssd.items():
    a[key] = val
        
    

    
    