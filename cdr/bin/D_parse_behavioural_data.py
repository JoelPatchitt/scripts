from pathlib import Path
import pandas as pd, numpy as np
import os, glob, re

# Identify relevant data paths
root = Path.cwd()
data_path = os.path.join(root, 'behavioural', 'sub*.csv')
b_data = glob.glob(data_path)
output_path = os.path.join(root, 'outputs')
output_path2 = os.path.join(root, 'r-inputs')
for data in b_data:
    subj = pd.read_csv(data)
    bmp = subj['imageFile']
    imageFile = pd.DataFrame()
    
################### OLD SCRIPT (very poor code, cba to change) ################   
    for item in subj['imageFile']:
        temp = item[-6:]
        temp2 = temp[:2]
        temp3 = re.sub(r'\D', "", temp2)
        temp3_series = pd.Series(temp3)
        imageFile = imageFile.append(temp3_series, ignore_index=True)   
    imageFile.columns = ['imageFile']
    
    # Classify face type & gender
    faceclass = pd.DataFrame()
    genclass = pd.DataFrame()
    for item in bmp:
        facetemp = item[:2]
        facetemp_series = pd.Series(facetemp)
        faceclass = faceclass.append(facetemp_series, ignore_index=True)
        gentemp = facetemp
        if gentemp == 'jj':
            gentemp2 = 1
        elif gentemp == 'em':
            gentemp2 = 1
        elif gentemp == 'mo':
            gentemp2 = 0
        elif gentemp == 'sw':
            gentemp2 = 0
        gentemp_series = pd.Series(gentemp2)
        genclass = genclass.append(gentemp_series, ignore_index=True)
    faceclass.columns = ['facetype']
    genclass.columns = ['gendertype']

        
    # Classify emotion type
    emotionclass = pd.DataFrame()
    intensityclass = pd.DataFrame()
    for item in bmp:
        emotemp = item[3:]
        emotemp2 = emotemp[:3]
        if emotemp2 == 'hap':
            emotemp3 = 1
        elif emotemp2 == 'ang' or 'fea':
            emotemp3 = 0
        emotemp_series = pd.Series(emotemp3)
        emotionclass = emotionclass.append(emotemp_series, ignore_index=True)
        intensity_series = (pd.Series(item[11:][:-4]))
        intensityclass = intensityclass.append(intensity_series, ignore_index=True)
    emotionclass.columns = ['emotiontype']
    
    
    # Calculate stim&resp times
    start = subj['stimStart'].iloc[0]
    stimtime = pd.DataFrame()
    resptime = pd.DataFrame()
    lasttime = pd.DataFrame()
    for item in subj['stimStart']:
        itemtemp = item - start
        stimtime = stimtime.append(pd.Series(itemtemp), ignore_index=True)
    stimtime.columns = ['stimStart']
     
    for item in subj['responseStart']:
        itemtemp = item - start
        resptime = resptime.append(pd.Series(itemtemp), ignore_index=True)
    resptime.columns = ['responseStart']
    
    for item in subj['lastSound']:
        itemtemp = item - start
        lasttime = lasttime.append(pd.Series(itemtemp), ignore_index=True)
    lasttime.columns = ['lastSound']
    
    subj['responseStart'] = resptime
    subj['stimStart'] = stimtime
    subj['lastSound'] = lasttime
    subj['emotion'] = emotionclass
    subj['face'] = faceclass
    subj['gender'] = genclass
    subj['intensity'] = intensityclass
    del subj['stimEnd']
    del subj['responseEnd']
    del subj['imageFile']
    ################################ NEWER, FANCIER CODE #####################
    subj['stimT-lastSound'] = [np.nan]*len(subj)
    subj['respT-lastSound'] = [np.nan]*len(subj)
    subj['sound_factor'] = [np.nan]*len(subj)
    subj['repetition_factor'] = [np.nan]*len(subj)
    sound = 1
    rep = 0
    for idx, row in subj.iterrows():
        subj['stimT-lastSound'].iloc[idx] = row['stimStart'] - row['lastSound']
        subj['respT-lastSound'].iloc[idx] = row['responseStart'] - row['lastSound']
        if (idx%25) == 0:
            rep += 1
        if rep == 4:
            sound +=1
            rep = 1
        subj['sound_factor'].iloc[idx] = sound
        subj['repetition_factor'].iloc[idx] = rep
    
    subj.to_csv(os.path.join(output_path, os.path.split(data)[1][:-4]) +
                '_behaviourals.csv', index=False)
    subj.to_csv(os.path.join(output_path2, os.path.split(data)[1][:-4]) +
                '_behaviourals.csv', index=False)