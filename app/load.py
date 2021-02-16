import os
import numpy as np
import pandas as pd


def load_sensor_csv_to_data_frame(path, verbose=False):
    """
    Return a Dataframe of the csv provided in the path.
    
    Notes
    -----
    This assumes the csv is properly formatted.
    This creates a Timestamp column.
    This drops NA Timestamp rows.
    This sets Timestamp to the index (use df.index to access)
    """
    # https://numpy.org/doc/stable/user/basics.types.html
    data_types = {
            'Date':str,
            'Time':str,
            'Battery':np.float64,
            'Fix':np.int32, # <- always zero?
            'Latitude':np.float64,
            'Longitude':np.float64,
            'Dp>0.3':np.int32,
            'Dp>0.5':np.int32,
            'Dp>1.0':np.int32,
            'Dp>2.5':np.int32,
            'Dp>5.0':np.int32,
            'Dp>10.0':np.int32,
            'PM1_Std':np.int32,
            'PM2.5_Std':np.int32,
            'PM10_Std':np.int32,
            'PM1_Env':np.int32,
            'PM2.5_Env':np.int32,
            'PM10_Env':np.int32,
            'Temp(C)':np.float64,
            'RH(%)':np.float64, 
            'P(hPa)':np.float64, 
            'Alti(m)':np.float64,
            }
    if verbose:
        print("Reading {}".format(path))
    df = pd.read_csv(path, 
                     dtype=data_types)
    
    df.attrs['name'] = os.path.splitext(os.path.split(path)[1])[0]
    
    df['Timestamp'] = df['Date'] + ' ' + df['Time']
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    
    
    na_count = df[df['Timestamp'].isnull()].shape[0]

    if na_count > 0:
        count = df.shape[0]
        if verbose:
            print(" - Dropping {} null rows out of {} rows, {:.3}%".format(na_count, count, na_count/count/100.))
        df = df[df['Timestamp'].notnull()]
    df.set_index('Timestamp', inplace=True)
    
    return df


def load_folder(folder):
    """
    Return a list of Dataframe from csv files in the folder path.
    
    Notes
    -----
    This assumes the csv is properly formatted.
    This creates a Timestamp column.
    This drops NA Timestamp rows.
    This sets Timestamp to the index (use df.index to access)
    """
    data = []
    for _, _, files in os.walk(folder):
        for file_name in files:
            if os.path.splitext(file_name)[-1] == '.csv':
                filepath = os.path.join(folder, file_name)
                data.append(load_sensor_csv_to_data_frame(filepath))
    return data