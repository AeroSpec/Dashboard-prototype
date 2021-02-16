

import load_data
import datetime
import random
import pandas as pd

random.seed(0)

data_size = 60
lower_cutoff = '2020-10-16 09:00:00'
upper_cutoff = '2020-10-16 12:30:00'
building_size = (100, 100)


class DataObj:
    """
    The DataObj loads input data from the specified path
    and creates a dictionary with datapoints in the
    self.data object.
    """
    def __init__(self, input_data_path):
        """
        self.data is where the usable data is stored.
        self.loaded_data is a list of dataframes from
        which new data is populated to create the illusion
        of new data being passed to the object.
        """
        self.idx = data_size

        self.data = {}
        self.loaded_data = load_data.load_folder(input_data_path)
        self.params = self.get_params()

        self.prep_data()

    def get_params(self):
        """
        Return a list of parameters

        Notes
        -----
        Uses the first data frame columns to determine parameters.
        """
        params = []
        df = self.loaded_data[0]
        for i in df.columns:
            if i in [
                'Dp > 0.3',
                'Dp > 0.5',
                'Dp > 1.0',
                'Dp > 2.5',
                'Dp > 5.0',
                'Dp > 10.0',
                'PM1_Std',
                'PM2.5_Std',
                'PM10_Std',
                'PM1_Env',
                'PM2.5_Env',
                'PM10_Env',
                'Temp(C)',
                'RH( %)',
                'P(hPa)',
                'Alti(m)',
                'Noise (dB)'
            ]:
                params.append(i)
        return params

    def prep_data(self):

        self.now = datetime.datetime.now()
        date_list = [self.now - datetime.timedelta(seconds=i*1) for i in range(data_size)]

        for df in self.loaded_data:
            df.drop(df.loc[df.index < lower_cutoff].index, inplace=True)
            df.drop(df.loc[df.index > upper_cutoff].index, inplace=True)
            df.drop(columns=['Date', 'Time','Battery','Fix','Latitude','Longitude'], inplace=True)

        for i,df in enumerate(self.loaded_data):
            id = self.get_id()
            self.data[id] = self.get_sensor_metadata(i)
            self.data[id]['data'] = df.copy(deep=True).iloc[0:data_size]
            self.data[id]['data']['Timestamp'] = pd.to_datetime(date_list, errors='coerce')
            self.data[id]['data'].set_index('Timestamp', inplace=True)

    def get_id(self):
        return '{:05}'.format(random.randint(1, 99999)) # random 5 digit number

    def get_sensor_metadata(self, source_idx):

        metadata = {}
        metadata['location'] = (random.randint(0, building_size[0]),
                                random.randint(0, building_size[1]))
        metadata['source'] = source_idx

        return metadata

    def increment_data(self):
        """
        Increments the data by 1 item

        Notes
        -----
        Uses the loaded_data to get the next item in the data frame
        and appends it to the true data.
        """

        self.idx += 1

        for id in self.data.keys():
            source_df = self.loaded_data[self.data[id]['source']]

            new_row_idx = self.idx%source_df.shape[0]
            entry = source_df.iloc[new_row_idx: new_row_idx+1]
            entry.index = [datetime.datetime.now()]
            new_df = pd.concat([entry, self.data[id]['data']])
            new_df.drop(new_df.tail(1).index, inplace=True)

            self.data[id]['data'] = new_df # concat cannot be done in place, so new dataframe created regardless
