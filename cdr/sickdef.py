from pathlib import Path
import os
import pandas as pd

def by_condition(*args, dataset=None, output=None):
    import math
    import pandas as pd
    
    # Create condition name list
    condition_names = [arg.name for arg in args]
    
    # Use condition names to create a condition:level dataframe
    conditions = pd.DataFrame(columns=condition_names)
    for i in condition_names:
        conditions[i] = data[i]
        
    # Merge all conditions into line by line tuples and add to dataset
    tup_list = list(tuple(conditions.itertuples(index=False, name=None)))
    data['all_conds'] = tup_list
    
    # Remove nan values and zero tuples (if any exist)
    nonan = [t for t in tup_list if not any(isinstance(n, float) and math.isnan(n) for n in t)]
    nozero = [i for i in nonan if 0 not in i]
    
    # Define and sort the unique iterations of your conditions
    unique = list(set(nozero)); unique.sort()
    
    keys = list(output.keys())
    for i, level in enumerate(unique):
        output[keys[i]] = data[data['all_conds'] == level]
    
    return output

# Load in your data
data = pd.read_csv(os.path.join(Path.cwd(), 'r-inputs', 'sub-01_peaks.csv'))

# Create a Dictionary of DataFrames for your split data
peaks = dict({'S01R01':pd.DataFrame(),'S01R02':pd.DataFrame(),'S01R03':pd.DataFrame(),
              'S02R01':pd.DataFrame(),'S02R02':pd.DataFrame(),'S02R03':pd.DataFrame(),
              'S03R01':pd.DataFrame(),'S03R02':pd.DataFrame(),'S03R03':pd.DataFrame(),
              'S04R01':pd.DataFrame(),'S04R02':pd.DataFrame(),'S04R03':pd.DataFrame(),})

# Call function listing each of your conditions, full dataset, and new output dict
split_data = by_condition(data['sound_factor'], data['repetition_factor'], dataset=data, output=peaks)