import load_data
import datetime
import random
import pandas as pd
import json
import os
import numpy as np

random.seed(0)

data_size = 60
lower_cutoff = "2018-01-01 00:00:00"
upper_cutoff = "2022-01-01 00:00:00"
building_size = (100, 100)

n_sensors = 23


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
        self.load_settings()
        self.get_params()
        self.sensors_count = len(list(self.loaded_data))

        self.prep_data()

    def get_params(self):
        """ Sets the parameters """
        self.params = list(self.settings.keys())

    def load_settings(self):
        """ Load the settings"""
        with open("settings.json") as json_file:
            self.settings = json.load(json_file)

    def prep_data(self):

        self.now = datetime.datetime.now()
        # get the past day in 10 second intervals
        date_list = [
            self.now - datetime.timedelta(seconds=i * 10) for i in range(60)  # 8640)
        ]
        # add a time-point for each day going back 500 days
        date_list += [self.now - datetime.timedelta(days=i + 1) for i in range(500)]
        data_size = len(date_list)

        for df in self.loaded_data:
            df.drop(df.loc[df.index < lower_cutoff].index, inplace=True)
            df.drop(df.loc[df.index > upper_cutoff].index, inplace=True)
            df.drop(
                columns=["Battery", "Fix", "Latitude", "Longitude"],
                inplace=True,
                errors="ignore",
            )

        copied_data = []
        for df in self.loaded_data:
            n_entries = len(df)
            n_copies = round(data_size / n_entries) + 1
            copied_data.append(pd.concat([df.copy(deep=True) for _ in range(n_copies)]))

        for i in range(n_sensors):
            sensor_i = np.random.randint(0, len(copied_data))
            df = copied_data[sensor_i]

            id = "Sensor {}".format(i + 1)
            self.data[id] = self.get_sensor_metadata(sensor_i)
            self.data[id]["data"] = df.copy(deep=True).iloc[0:data_size]
            self.data[id]["data"]["Timestamp"] = pd.to_datetime(
                date_list, errors="coerce"
            )
            self.data[id]["data"].set_index("Timestamp", inplace=True)

    def get_random_id(self):
        return "{:05}".format(random.randint(1, 99999))  # random 5 digit number

    def get_sensor_metadata(self, source_idx):

        metadata = {}
        metadata["location"] = (
            random.randint(0, building_size[0]),
            random.randint(0, building_size[1]),
        )
        metadata["source"] = source_idx

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
            source_df = self.loaded_data[self.data[id]["source"]]

            new_row_idx = self.idx % source_df.shape[0]
            entry = source_df.iloc[new_row_idx : new_row_idx + 1]
            entry.index = [datetime.datetime.now()]
            new_df = pd.concat([entry, self.data[id]["data"]])
            new_df.drop(new_df.tail(1).index, inplace=True)

            self.data[id][
                "data"
            ] = new_df  # concat cannot be done in place, so new dataframe created regardless
