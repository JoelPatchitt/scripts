from pathlib import Path
import pandas as pd, numpy as np#, matplotlib.pyplot as plt, seaborn as sns
import os, glob, statistics
#import plotly.express as px
# Reversing a list using reversed()
def Reverse(lst):
    return [ele for ele in reversed(lst)]

# Identify relevant data paths
root = Path.cwd()
data_path = os.path.join(root, 'r-inputs', '*peaks.csv')
output_path = os.path.join(root, 'r-inputs')
data = glob.glob(data_path)
mean_CDR_split = pd.DataFrame()
seconds = pd.DataFrame()#columns=range(0,41))
graph_loop = 0
sub_ecg = dict({'S01R01':[],
                    'S01R02':[],
                    'S01R03':[],
                    'S02R01':[],
                    'S02R02':[],
                    'S02R03':[],
                    'S03R01':[],
                    'S03R02':[],
                    'S03R03':[],
                    'S04R01':[],
                    'S04R02':[],
                    'S04R03':[],
                    }) 
keys = list(sub_ecg.keys())
ecg_response = dict({'S01R01':[0],
                     'S01R02':[0],
                     'S01R03':[0],
                     'S02R01':[0],
                     'S02R02':[0],
                     'S02R03':[0],
                     'S03R01':[0],
                     'S03R02':[0],
                     'S03R03':[0],
                     'S04R01':[0],
                     'S04R02':[0],
                     'S04R03':[0],
                     })   
for sub in data:
    
    # Grab CDR for each sound    
    split_dat = dict({'0_IBI':[],'0_beat_ms':[],
                      '1_IBI':[],'1_beat_ms':[],
                      '2_IBI':[],'2_beat_ms':[],
                      '3_IBI':[],'3_beat_ms':[],
                      '4_IBI':[],'4_beat_ms':[],
                      '5_IBI':[],'5_beat_ms':[],
                      '6_IBI':[],'6_beat_ms':[],
                      '7_IBI':[],'7_beat_ms':[],
                      '8_IBI':[],'8_beat_ms':[],
                      '9_IBI':[],'9_beat_ms':[],
                      '10_IBI':[],'10_beat_ms':[],
                      '11_IBI':[],'11_beat_ms':[],
                      '12_IBI':[],'12_beat_ms':[],})
    peaks = pd.read_csv(sub)
    rep = 1
    base = 0
    for idx, row in peaks.iterrows():
        if np.isnan(row['sound_factor']) == True:
            continue
        new_rep = row['repetition_factor']  
        if rep == 3 and new_rep == 1:
            base +=3
        rep = row['repetition_factor']      
        cond = base+rep    
        cond = int(cond)
        
        split_dat[(str(cond)+'_IBI')].append(row['IBI'])
        split_dat[(str(cond)+'_beat_ms')].append(row['r-peak'])
    
    # Equalise dictionary lengths with NaN values for DataFrame conversion
    dict_length = []
    for key,val in split_dat.items(): 
        dict_length.append(len(val))
    max_len = max(dict_length)
    for key,val in split_dat.items():
        if key == '12':
            continue
        temp = [np.nan]*(max_len-len(val))
        split_dat[key] = val + temp
    
    split_df = pd.DataFrame(split_dat)

    for items,val in split_df.items():
        if items[-1:] == 's':
            split_df[items] = split_df[items]/1000
            pass
        else:
            idx=0
            for x in val:
                val[idx] = (((1-(x/1000))*60)+60)
                idx+=1

                
        # if items[-1:] == 's' and items[:1] == '0':
        #       split_df[items] = val-val[1]
        # else:
        #       split_df[items] = val-val[0]
        if items[-1:] == 's':
              split_df[items] = val-val[0]
        
    #print(len(split_df[split_df['1_IBI'] > 1]))   
    
##############################################################################
# Seperate CDR by T1-T2-T3-T4
    split_CDR = dict({'0_1-10':[],'0_11-25':[],'0_26-45':[],'0_46-100': [],
                      '1_1-10':[],'1_11-25':[],'1_26-45':[],'1_46-100': [],
                      '2_1-10':[],'2_11-25':[],'2_26-45':[],'2_46-100': [],
                      '3_1-10':[],'3_11-25':[],'3_26-45':[],'3_46-100': [],
                      '4_1-10':[],'4_11-25':[],'4_26-45':[],'4_46-100': [],
                      '5_1-10':[],'5_11-25':[],'5_26-45':[],'5_46-100': [],
                      '6_1-10':[],'6_11-25':[],'6_26-45':[],'6_46-100': [],
                      '7_1-10':[],'7_11-25':[],'7_26-45':[],'7_46-100': [],
                      '8_1-10':[],'8_11-25':[],'8_26-45':[],'8_46-100': [],
                      '9_1-10':[],'9_11-25':[],'9_26-45':[],'9_46-100': [],
                      '10_1-10':[],'10_11-25':[],'10_26-45':[],'10_46-100': [],
                      '11_1-10':[],'11_11-25':[],'11_26-45':[],'11_46-100': [],
                      '12_1-10':[],'12_11-25':[],'12_26-45':[],'12_46-100': []})
    split_CDR_means = dict(split_CDR)
              
    for idx, row in split_df.iterrows():
        rowIdx = 0
        name=0
        for col in row:
            if rowIdx%2 != 0:
                rowIdx+=1
                continue
            
            elif row[rowIdx+1] <= 10:
                split_CDR[str(name)+'_1-10'].append(col)
                rowIdx+=1
                name+=1
            elif row[rowIdx+1] >= 11 and row[rowIdx+1] <= 25:
                split_CDR[str(name)+'_11-25'].append(col)
                rowIdx+=1
                name+=1
            elif row[rowIdx+1] >= 26 and row[rowIdx+1] <=45:
                split_CDR[str(name)+'_26-45'].append(col)
                rowIdx+=1
                name+=1
            elif row[rowIdx+1] >= 46:
                split_CDR[str(name)+'_46-100'].append(col)
                rowIdx+=1
                name+=1
            else:
                rowIdx+=1
                name+=1
                
    CDR_full = dict(split_CDR)
    
    # Calculate means for split CDR items            
    for key, val in split_CDR.items():
        if key[:1] == '0':
            split_CDR[key] = []
            continue
        split_CDR_means[key] = statistics.mean(val)

    # remove last 5 seconds
    entries_to_remove = ('0_1-10','0_11-25','0_26-45','0_46-100')
    for k in entries_to_remove:
        split_CDR_means.pop(k, None)
         
    means = pd.DataFrame(split_CDR_means, index = [0])
    means = means.T
    CDR_means = means.T
    CDR_means['px'] = int(os.path.split(sub)[1][4:][:-10])
    mean_CDR_split = mean_CDR_split.append(CDR_means, ignore_index=True)
    
    IBI = [c for c in split_df.columns if 'IBI' in c]
    ms = [c for c in split_df.columns if 'ms' in c]    
    for o in range(12):
        prevx = split_df[ms[o]][split_df[ms[o]] >= -10000]
        prevx.reset_index(drop=True)
        prevy = split_df[IBI[o]]
        prevy = prevy.reset_index(drop=True)
        
        x = split_df[ms[o+1]][split_df[ms[o+1]] >= -10000]
        y = split_df[IBI[o+1]][split_df[IBI[o+1]] >= -10000]
        
        for nrow in range(len(y)):
            if y.iloc[nrow] < 0:
                y.iloc[nrow] = y.iloc[nrow-1]
            if y.iloc[nrow-1] - y.iloc[nrow] > 20:
                y.iloc[nrow] = y.iloc[nrow-1]
    
        # data1 = pd.DataFrame([x,y])
        # data1 = data1.T
        # data1.reset_index(drop=True)    
        #fig = px.scatter(data1, x="1_beat_ms", y="1_IBI", trendline="rolling", 
         #                trendline_options=dict(window=5), title=str(sub))
        #fig.show(renderer="png", width=800, height=300)
    
        # Create dataset for average plot of first CDR
        secs = []
        prevsecs = []
        lower = 0
        upper = 1
        sec = 1
        prevsec = 1
        pup = int(np.ceil(prevx.iloc[-1]))
        plow = pup-1
        for i in range(104):
            temp = x.loc[x > lower]
            temp = temp.loc[x < upper]
            index = temp.index

           
            if len(y.iloc[index]) > 1:
                sec = statistics.mean(y.iloc[index])
            elif len(y.iloc[index]) == 1:

                sec = y.iloc[index]  
            else:
                sec=sec
            try:
                sec = float(sec)
            except:
                pass
      
                
            secs.append(sec)
            lower+=1
            upper+=1
            # Grab data 5 seconds previous to sound
        #     if i <=4:
        #         temp = prevx.loc[prevx > plow]
        #         temp = temp.loc[temp < pup]
        #         index2 = temp.index
        #         if len(prevy.iloc[index2]) > 1:
        #             prevsec = statistics.mean(prevy.iloc[index2])
        #         elif len(prevy.iloc[index2]) == 1:
        #             prevsec = prevy.iloc[index2]
        #         else:
        #             prevsec = prevsec
        #         try:
        #             prevsec = float(prevsec)
        #         except:
        #             pass
        #         prevsecs.append(prevsec)
        #         plow-=1
        #         pup-=1
        # if len(secs) < 103:
        #     print(sub, o, len(secs))
        #     exit()
        # prevsecs.reverse()
        # prevsecs.extend(secs)
        for idxr in range(len(secs)):
            if secs[idxr] == 1:
                print('1')
                secs[idxr] = secs[idxr-1]
        seconds = pd.Series(secs)
        sub_ecg[keys[o]] = seconds

    ecg_response['S01R01'].append(sub_ecg['S01R01'])
    ecg_response['S01R02'].append(sub_ecg['S01R02'])
    ecg_response['S01R03'].append(sub_ecg['S01R03'])
    ecg_response['S02R01'].append(sub_ecg['S02R01'])
    ecg_response['S02R02'].append(sub_ecg['S02R02'])
    ecg_response['S02R03'].append(sub_ecg['S02R03'])
    ecg_response['S03R01'].append(sub_ecg['S03R01'])
    ecg_response['S03R02'].append(sub_ecg['S03R02'])
    ecg_response['S03R03'].append(sub_ecg['S03R03'])
    ecg_response['S04R01'].append(sub_ecg['S04R01'])
    ecg_response['S04R02'].append(sub_ecg['S04R02'])
    ecg_response['S04R03'].append(sub_ecg['S04R03'])
    
final_keys= list(ecg_response.keys())
final_output = pd.DataFrame()
for keyz in final_keys:
    temp = pd.DataFrame()
    for items in ecg_response[keyz][1:]:
        temp = temp.append(items, ignore_index=True)
    transposed = temp.T
    mean = transposed.mean(axis=1)
    final_output[keyz] = mean
 
final_output.to_csv(os.path.join(output_path, 'CDR_by_cond.csv'), index=None)    
    
        #split_df.to_csv(os.path.join(output_path,
        #                os.path.split(sub)[1][:-4] + '_CDR.csv'), index=None)   
#    for key, val in sub_ecg.items():
#        ecg_response[key] = [ecg_response[key]+val]
#for items in 
# Create average plot  
#boom = seconds.mean(axis=1)
#boom = pd.DataFrame(boom)
#boom['1'] = range(-4,105)

# fig = px.scatter(boom, x='1', y=0, trendline="rolling", trendline_options=dict(window=3),
#             title="change in HR over time")
# fig.data = [t for t in fig.data if t.mode == "lines"]
# #fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
# fig.show(renderer="png", width=350, height=300)

#mean_CDR_split.to_csv(os.path.join(output_path, 'CDR_split.csv'), index=None)

# split_df(CDR = ms & BPM for every IBI across all 12 sounds)
# CDR_full(split CDR = dictionary of all 12 conditions split into 4 time grabs(T's))
# CDR_means(mean split CDR) = means of each T for all 12 conditions