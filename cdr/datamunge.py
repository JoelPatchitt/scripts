'''Written by Joel Patchitt 19/04/2022'''
def by_condition(*args, dataset=None, output=None):

    import math
    import pandas as pd
    
    # Handle argument errors
    class InputError(Exception):
        pass
    
    if not args:
        raise InputError('Conditions not defined. Please input arguments as follows: split_data = by_condition(your_data["condition_n"], your_data["condition_n"], dataset = your_data, output = your_output)')
    if dataset is None:
        raise InputError('Dataset not defined. Please input arguments as follows: split_data = by_condition(your_data["condition_n"], your_data["condition_n"], dataset = your_data, output = your_output)')
    if output is None:
        print('Running data split without predefined output variable, by_condition will create one for you.')
    
    # Create condition name list
    condition_names = [arg.name for arg in args]
    
    # Use condition names to create a condition:level dataframe
    conditions = pd.DataFrame(columns=condition_names)
    for i in condition_names:
        conditions[i] = dataset[i]
        
    # Merge all conditions into line by line tuples and add to dataset
    tup_list = list(tuple(conditions.itertuples(index=False, name=None)))
    dataset['all_conds'] = tup_list
    
    # Remove nan values and zero tuples (if any exist)
    nonan = [t for t in tup_list if not any(isinstance(n, float) and math.isnan(n) for n in t)]
    nozero = [i for i in nonan if 0 not in i]
    
    # Define and sort the unique iterations of your conditions
    unique = list(set(nozero)); unique.sort()
    
    # Check if output variable has already been defined
    if output is None:
        output_cols = []
        # Name output columns by level number and ordered by appearance in def arg
        for i in unique:
           temp = []
           [temp.extend(str(int(j))) for j in i]
           new_string = "".join(temp)
           output_cols.append(new_string)
        output = {x:pd.DataFrame() for x in output_cols}
           

    keys = list(output.keys())
    for i, level in enumerate(unique):
        output[keys[i]] = dataset[dataset['all_conds'] == level]
        output[keys[i]].reset_index(drop=True, inplace=True)

    return output