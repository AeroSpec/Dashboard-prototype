import datetime

def stats_one_parameter_all_sensors(data_obj):
    return None

def stats_one_sensor_all_parameters(data_obj):
    return None

def stats_all_sensors_all_parameters(data_obj):
    return None


'''
Object to store and manipulate list view information
'''
class ListViewTablesObj:

    def __init__(self):
        self.__data = dict()  # Map of <Sensor, Data>
        self.__sensor_ids_list = list() # List of all available sensors
        self.__selected_sensor_ids = list()  # List of sensors selected in the selected view
        self.__selected_sensors_grouped_data = dict()  # Map of <Selected sensor, grouped data>
        self.__selected_attribute = ''
        self.__settings = dict()

    def set_settings(self, settings):
        self.__settings = settings

    def get_data(self):
        return self.__data

    def set_data(self, data):
        for i in range(len(data)):
            self.__data["Sensor " + str(i + 1)] = data[i]
            self.__sensor_ids_list.append("Sensor " + str(i + 1))

    def get_attr_selected(self):
        return self.__selected_attribute

    def set_attr_selected(self, attribute):
        if attribute != self.__selected_attribute:
            self.__selected_attribute = attribute
            selected_sensors_copy = list(self.__selected_sensor_ids)
            self.__reset_selected_data()
            for sensor_id in selected_sensors_copy:
                self.add_sensor_to_selected_list(sensor_id)

    def get_all_sensor_ids(self):
        return self.__sensor_ids_list

    def get_selected_sensor_ids(self):
        return self.__selected_sensor_ids

    def get_selected_sensors_grouped_data(self):
        return self.__selected_sensors_grouped_data

    '''
    Method to add a sensor to selected list
    '''
    def add_sensor_to_selected_list(self, sensor_id):
        if (
            sensor_id in self.__sensor_ids_list
            and sensor_id not in self.__selected_sensor_ids
        ):
            grouped_data = self.__group_data_by_period(
                self.__data[sensor_id], self.__selected_attribute
            )
            self.__selected_sensor_ids.append(sensor_id)
            self.__selected_sensors_grouped_data[sensor_id] = grouped_data

    '''
    Method to remove a sensor from selected list
    '''
    def remove_sensor_from_selected_list(self, sensorId):
        if (
            sensorId in self.__sensor_ids_list
            and sensorId in self.__selected_sensor_ids
        ):
            self.__selected_sensor_ids.remove(sensorId)
            del self.__selected_sensors_grouped_data[sensorId]

    '''
    Method to get the air quality for a given value of a metric
    '''
    def __get_air_quality(self, attribute_name, attribute_value):
        if attribute_name not in self.__settings.keys():
            raise Exception("Threshold not set for attribute in constants to calculate air_quality")
        else:
            for quality, threshold in self.__settings[attribute_name].items():
                if attribute_value <= float(threshold):
                    return quality

        return "Threshold not defined to determine air_quality for attribute: " +  attribute_name + \
               " and attribute value: " + attribute_value  + ". Please check"

    '''
    Method to reset all selected data
    '''
    def __reset_selected_data(self):
        self.__selected_sensor_ids = list()
        self.__selected_sensors_grouped_data = dict()

    '''
    Method which checks if the data lies in the period of interest
    TODO - Currently returns true for all data, 
    Once current data is provided the method return true if datapoint lies within the specified period
    '''
    def __does_date_lie_in_period(self, curr_date, earlier_date, period):
        return True

    '''
    Method which when given a time period, groups the data by the time period for each sensor
    and returns the value of the latest group
    '''
    def __group_data_by_period(self, data_one_sensor, attribute, period="weekly"):
        grouped_data = dict()
        total_temp = 0
        total_data_points = 1
        curr_date = datetime.datetime.now()

        # 1. Temperature data
        grouped_data["max"] = 0
        grouped_data["min"] = 1000  # some high value
        air_quality = "NA"

        for ind, row in data_one_sensor.iterrows():
            try:
                data_modified = dict()
                earlier_date = datetime.datetime.strptime(
                    data_one_sensor.Date[ind] + " " + data_one_sensor.Time[ind],
                    "%Y/%m/%d %H:%M:%S",
                )

                if self.__does_date_lie_in_period(curr_date, earlier_date, period):
                    # Add to total and increase count for average caclculation
                    total_temp += row[[attribute]]
                    total_data_points += 1

                    # Get max and min temp
                    grouped_data["max"] = max(grouped_data["max"], row[attribute])
                    grouped_data["min"] = min(grouped_data["min"], row[attribute])
                    air_quality = "GOOD"

            except Exception as e:
                print(e)
                continue
        if air_quality == 'NA':
            grouped_data['avg'] = 'NA'
        else:
            grouped_data['avg'] = round(float(total_temp / total_data_points), 2)

            # 2. Air Quality
            grouped_data['air_quality'] = self.__get_air_quality(attribute, grouped_data['avg'])

        # 3. Selected feature graph of over 1 week time
        # TODO - Make the overall period configurable
        grouped_data["max"] = "NA" if grouped_data["max"] == 0 else grouped_data["max"]

        return grouped_data
