import datetime


class ListViewTablesObj:

    def __init__(self):
        self.__data = dict()  # Map of <Sensor, Data>
        self.__sensor_ids_list = list() # List of all available sensors
        self.__selected_sensor_ids = list()  # List of sensors selected in the selected view
        self.__selected_sensors_grouped_data = dict()  # Map of <Selected sensor, grouped data>

    def get_data(self):
        return self.__data

    def set_data(self, data):
        for i in range(len(data)):
            self.__data['Sensor ' + str(i+1)] = data[i]
            self.__sensor_ids_list.append('Sensor ' + str(i+1))

    def get_all_sensor_ids(self):
        return self.__sensor_ids_list

    def get_selected_sensor_ids(self):
        return self.__selected_sensor_ids

    def get_selected_sensors_grouped_data(self):
        return self.__selected_sensors_grouped_data

    ## Method to add a sensor to selected list
    def add_sensor_to_selected_list(self, sensorId):
        if sensorId in self.__sensor_ids_list and sensorId not in self.__selected_sensor_ids:
            grouped_data = self.__group_data_by_period(self.__data[sensorId])
            self.__selected_sensor_ids.append(sensorId)
            self.__selected_sensors_grouped_data[sensorId] = grouped_data

    ## Method to remove a sensor from selected list
    def remove_sensor_from_selected_list(self, sensorId):
        if sensorId in self.__sensor_ids_list and sensorId in self.__selected_sensor_ids:
            self.__selected_sensor_ids.remove(sensorId)
            del self.__selected_sensors_grouped_data[sensorId]

    # Method which checks if the data lies in the period of interest
    # TODO - Currently returns true for all data, once current data is provided the method return true if datapoint lies within the specified period
    def __does_date_lie_in_period(self, curr_date, earlier_date, period):
        return True

    # Method which when given a time period, groups the data by the time period for each sensor
    # and returns the value of the latest group
    def __group_data_by_period(self, data_one_sensor, period="weekly"):
        grouped_data = dict()
        total_temp = 0
        total_data_points = 1
        curr_date = datetime.datetime.now()

        # 1. Temperature data
        grouped_data['max_temp'] = 0
        grouped_data['min_temp'] = 1000  # some high value
        air_quality = 'NA'

        for ind, row in data_one_sensor.iterrows():
            print('here')
            try:
                data_modified = dict()
                earlier_date = datetime.datetime.strptime(data_one_sensor.Date[ind] + ' ' + data_one_sensor.Time[ind],
                                                          '%Y/%m/%d %H:%M:%S')

                if self.__does_date_lie_in_period(curr_date, earlier_date, period):
                    # Add to total and increase count for average caclculation
                    total_temp += row[['Temp(C)']]
                    total_data_points += 1

                    # Get max and min temp
                    grouped_data['max_temp'] = max(grouped_data['max_temp'], row['Temp(C)'])
                    grouped_data['min_temp'] = min(grouped_data['min_temp'], row['Temp(C)'])
                    air_quality = 'GOOD'

            except Exception as e:
                print(e)
                continue
                # grouped_data['max_temp'] = 'NA'
                # grouped_data['min_temp'] = 'NA'
                # grouped_data['avg_temp'] = 'NA'

        grouped_data['avg_temp'] = 'NA' if air_quality == 'NA' else float(total_temp / total_data_points)
        # 2. Air Quality
        # TODO - Implement logic to denote air quality
        grouped_data['air_quality'] = air_quality

        # 3. Selected feature graph of over 1 week time
        # TODO - Make the overall period configurable
        grouped_data['max_temp'] = 'NA' if grouped_data['max_temp'] == 0 else grouped_data['max_temp']
        grouped_data['min_temp'] = 'NA' if grouped_data['min_temp'] == 1000 else grouped_data['min_temp']
        print(grouped_data)
        return grouped_data