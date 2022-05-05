from pathlib import Path
import pandas as pd, numpy as np
import os, glob

# Identify relevant data paths
root = Path.cwd()
peaks_path = os.path.join(root, 'outputs', '*peaks.csv')
onsets_path = os.path.join(root, 'outputs', '*onsets.csv')
beh_path = os.path.join(root, 'outputs', '*behaviourals.csv')
output_path = os.path.join(root, 'r-inputs')
peak_data = glob.glob(peaks_path)
onset_data = glob.glob(onsets_path)
beh_data = glob.glob(beh_path)
exclusion_factor = pd.read_csv('exclusion_factor.csv', index_col=0)
onsets = pd.DataFrame()
qual_check_01 = pd.DataFrame()
qual_check_02 = pd.DataFrame()
qual_check_03 = pd.DataFrame()
saved_data = pd.DataFrame()
#exclusion_limit = int(input('exclusion factor = '))
###############################ECG_FILE#######################################
# Loop around participants
for loop in range(len(peak_data)):
    onsets = pd.DataFrame()
    # Load in and and label data
    peaks = pd.read_csv(peak_data[loop], names=['r-peak', 'IBI'], header=None)
    subj = pd.read_csv(beh_data[loop])
    onsets['onsets_ms'] = pd.read_csv(onset_data[loop], header=None)
    onsets['id'] = [0]*len(onsets)
    # Identify trigger labels
    # print(max(peaks['IBI'][1:]))
    # print(peaks[peaks.IBI > 1000])
    # print(peaks['IBI'].nlargest(n=10))
    # exclusion_limit = int(input('exclusion_limit = '))#
    exclusion_limit = int(exclusion_factor.iloc[loop])
    saved_data = saved_data.append(pd.Series(exclusion_limit), ignore_index=True)
    for idx, row in onsets.iterrows():
        if idx <= 9:
            row['id'] = 0
        else:
            if idx == 10:
                row['id'] = 1
                counter = 0
            else:
                if idx == len(onsets)-1:
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
    temp = pd.DataFrame(onsets['id'].value_counts())
    temp = temp.transpose()
    qual_check_01 = qual_check_01.append(temp)
    
    # Attach trigger labels to data
    final = pd.DataFrame()
    for ons in onsets['onsets_ms']:
        final = final.append(pd.Series(peaks['r-peak'].sub(ons).abs().idxmin()),
                             ignore_index=True) # Finds closest R-peak to trigger
        
    peaks['onsets_id'] = [np.nan]*len(peaks)
    peaks['onsets_ms'] = [np.nan]*len(peaks)
    for i in range(len(onsets)):
        while True:
            if np.isnan(peaks['onsets_id'].iloc[int(final.iloc[i])]) == False:
                final.iloc[i]+=1
            else:
                break
        peaks['onsets_id'].iloc[int(final.iloc[i])] = onsets['id'].iloc[i]
        peaks['onsets_ms'].iloc[int(final.iloc[i])] = onsets['onsets_ms'].iloc[i]
    
    temp = peaks['onsets_id'].value_counts()
    temp = temp.transpose()
    qual_check_02 = qual_check_02.append(temp)
    
    # Create condition for Sounds, Repetition number, responses & exclusions
    peaks['sound_factor'] = [np.nan]*len(peaks)
    peaks['repetition_factor'] =[np.nan]*len(peaks) 
    peaks['response'] = [np.nan]*len(peaks)
    peaks['exclusion_factor'] = [np.nan]*len(peaks)
    peaks['T_last-sound'] = [np.nan]*len(peaks)
    sound = 0
    rep = 0
    x = 0
    last_sound = 0
    for idx, row in peaks.iterrows():
        if row['onsets_id'] == 1:
            if sound == 0:
                sound +=1
            rep +=1
            last_sound = peaks['onsets_ms'].iloc[idx]
            continue
        if rep == 4:
            sound +=1
            rep = 1
        if row['onsets_id'] == 4:
            sound = np.nan
            rep = np.nan
        
        peaks['sound_factor'].iloc[idx] = sound
        peaks['repetition_factor'].iloc[idx] = rep
        
        if row['onsets_id'] == 3:
            peaks['response'].iloc[idx] = subj['response'].iloc[x]
            x +=1
        if row['IBI'] >= exclusion_limit and not type(row['IBI']) == str:
            peaks['exclusion_factor'].iloc[idx] = 1
        else:
            peaks['exclusion_factor'].iloc[idx] = 0

        if peaks['onsets_id'].iloc[idx] == 1:
            print('here')
            last_sound = peaks['onsets_ms'].iloc[idx]
        if last_sound == 0:
            continue
        else:
            peaks['T_last-sound'].iloc[idx] = (int(row['r-peak'])-int(last_sound))
        
        
        
    temp = pd.DataFrame(peaks['exclusion_factor'].value_counts())
    temp = temp.transpose()
    qual_check_03 = qual_check_03.append(temp)
    

    # Add participant number
    peaks['px'] = [os.path.split(peak_data[loop])[1][4:][:-10]]*len(peaks)
    
    #peaks.to_csv(os.path.join(output_path, os.path.split(peak_data[loop])[1]))
    sd
    del peaks, subj, onsets        
    
        
    
    
        
    
    

        
            