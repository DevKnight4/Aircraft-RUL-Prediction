import os
import pandas as pd
import numpy as np

def get_cmapss_columns():
    """Returns the standard column names for the CMAPSS dataset."""
    return ['engine_id', 'cycle', 'op_setting_1', 'op_setting_2', 'op_setting_3'] + \
           [f'sensor_{i}' for i in range(1, 22)]

def load_cmapss_data(data_path, dataset_type='train', dataset_id='FD002'):
    """
    Loads a CMAPSS dataset file (train or test).
    
    Args:
        data_path (str): Path to the directory containing the data files.
        dataset_type (str): 'train' or 'test'
        dataset_id (str): e.g. 'FD002'
        
    Returns:
        pd.DataFrame: The loaded and formatted dataframe.
    """
    filename = f"{dataset_type}_{dataset_id}.txt"
    filepath = os.path.join(data_path, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}. Please ensure the dataset is placed in {data_path}.")
        
    columns = get_cmapss_columns()
    
    # Read the text file. CMAPSS is space-separated.
    df = pd.read_csv(filepath, sep=r'\s+', header=None, names=columns)
    
    return df

def load_rul_data(data_path, dataset_id='FD002'):
    """
    Loads the true RUL values for the test set.
    
    Args:
        data_path (str): Path to the directory containing the data files.
        dataset_id (str): e.g. 'FD002'
        
    Returns:
        pd.DataFrame: The loaded RUL dataframe.
    """
    filename = f"RUL_{dataset_id}.txt"
    filepath = os.path.join(data_path, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}. Please ensure the dataset is placed in {data_path}.")
    
    df = pd.read_csv(filepath, sep=r'\s+', header=None, names=['RUL'])
    
    return df
