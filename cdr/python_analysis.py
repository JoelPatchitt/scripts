from pathlib import Path
import pandas as pd
import os, glob, copy

participant_number = 49
subj_data = list(glob.glob(os.path.join(Path.cwd(), 'r-inputs', 'sub-*peaks.csv')))
condition_idx = pd.DataFrame()

peaks = dict({'S01R01':pd.DataFrame(),'S01R02':pd.DataFrame(),'S01R03':pd.DataFrame(),
              'S02R01':pd.DataFrame(),'S02R02':pd.DataFrame(),'S02R03':pd.DataFrame(),
              'S03R01':pd.DataFrame(),'S03R02':pd.DataFrame(),'S03R03':pd.DataFrame(),
              'S04R01':pd.DataFrame(),'S04R02':pd.DataFrame(),'S04R03':pd.DataFrame(),})



plots = copy.copy(peaks)
meanHR = pd.DataFrame()
averageHR = pd.DataFrame()
split_CDR = copy.copy(peaks)

for sub in subj_data:
    # Read in subject data
    data = pd.read_csv(sub, index_col=0)
    
    # Separate data into conditions (peaks & plots)
    sound = [1,2,3,4]
    rep = [1,2,3]
    temp = []
    temp_plot = []
    for s in sound:
        for r in rep:
            col_name = ''.join(['S0', str(s), 'R0', str(r)])
            meanHR[col_name] = []
            temp = data[data['sound_factor'] == s]
            temp = temp[temp['repetition_factor'] == r]
            temp_plot = temp[temp['exclusion_factor'] != 1]
            peaks[col_name] = peaks[col_name].append(temp)
            plots[col_name] = plots[col_name].append(temp_plot)
            
#plots.to_csv('plot_data.csv', index=False)
# Calculate B2B HR and Get means by factor 
cur_key = 0
for key, val in plots.items():
    plots[key].reset_index(drop=True, inplace=True)
    val['hr'] = (((1-(val['IBI']/1000))*60)+60)
    # Grab means for all participants in each factor
    lower = 0
    upper = 1000
    seconds = pd.DataFrame()
    for sec in range(104):
        temp2 = val[val['T_last-sound'] >= lower]
        temp2 = temp2['hr'][temp2['T_last-sound'] <= upper]
        
        if len(temp2) > 1:
            temp2 = temp2.mean()
        elif len(temp2) == 1:
            pass
        else:
            temp2 = temp2
        seconds = seconds.append(pd.Series(temp2), ignore_index=True)
        lower+=1000
        upper+=1000 
    meanHR[key] = seconds
    cur_key+=1
    
    # average HR per condition
    hrmean = pd.DataFrame()
    px = 0
    for part in range(1, participant_number+1):
        temp_HR = val['hr'][val['px'] == part]
        hrmean = hrmean.append(pd.Series(temp_HR.mean()), ignore_index = True)
        hrmean = hrmean.dropna(how='all')
    averageHR[key] = hrmean
    px+=1
    tempx = []
for part in range(42):
    tempx.append(subj_data[part][-12:][:2])
averageHR['px'] = pd.Series(tempx)
    
#averageHR.to_csv('average_HR.csv', index=False)
    
for key, val in plots.items():
    t1 = pd.DataFrame()
    t2 = pd.DataFrame()
    t3 = pd.DataFrame()
    t4 = pd.DataFrame()
    for p in range(42):
        pmate = int(subj_data[p][-12:][:2])
        part = val[val['px'] == pmate]
        t1sub = part['hr'][part['T_last-sound'] <= 10000]
        temp = part[part['T_last-sound'] >= 10001]; t2sub = temp['hr'][temp['T_last-sound'] <= 25000]
        temp = part[part['T_last-sound'] >= 25001]; t3sub = temp['hr'][temp['T_last-sound'] <= 45000]
        temp = part[part['T_last-sound'] >= 45001]; t4sub = temp['hr'][temp['T_last-sound'] <= 100001]
        t1 = t1.append(pd.Series(t1sub.mean()),ignore_index=True)
        t2 = t2.append(pd.Series(t2sub.mean()),ignore_index=True)
        t3 = t3.append(pd.Series(t3sub.mean()),ignore_index=True)
        t4 = t4.append(pd.Series(t4sub.mean()),ignore_index=True)
    split_CDR[key]['0_10'] = t1; split_CDR[key]['10_25'] = t2
    split_CDR[key]['25_45'] = t3; split_CDR[key]['45_100'] = t4

split_output = pd.DataFrame()
for key, val in split_CDR.items():
    for col in val.columns:
        col_name = ''.join([key, '_', col])
        split_output[col_name] = val[col]
split_output['px'] = tempx
split_output = split_output.drop(11)
#split_output.to_csv('split_CDR_proper.csv', index=False)  
    
        
    
    
    
    
    
            
