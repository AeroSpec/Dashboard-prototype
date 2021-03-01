import datetime


def stats_one_parameter_all_sensors(data_obj):
    return None


def stats_one_sensor_all_parameters(data_obj):
    return None


def stats_all_sensors_all_parameters(data_obj):
    return None


"""
Object to store and manipulate list view information
"""


class ListViewTablesObj:
    def __init__(self, data, settings, default_attribute):
        self.__data = dict() # Map of <Sensor, Data>
        self.__sensor_ids_list = list()  # List of all available sensors
        self.__selected_attribute = default_attribute # Default attribute selected
        self.__selected_sensor_ids = (
            list()
        )  # List of sensors selected in the selected view
        self.__selected_sensors_grouped_data = (
            dict()
        )  # Map of <Selected sensor, grouped data>
        self.__settings = settings
        self.__set_data(data)
        for sensor_id in self.__sensor_ids_list:
            self.add_sensor_to_selected_list(sensor_id)

    def get_data(self):
        return self.__data

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

    """
    Method to add a sensor to selected list
    """

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

    """
    Method to remove a sensor from selected list
    """

    def remove_sensor_from_selected_list(self, sensorId):
        if (
            sensorId in self.__sensor_ids_list
            and sensorId in self.__selected_sensor_ids
        ):
            self.__selected_sensor_ids.remove(sensorId)
            del self.__selected_sensors_grouped_data[sensorId]

    """
    Method to remove a sensor from selected list
    """

    def remove_all_sensors_from_selected_list(self):
        self.__selected_sensor_ids = list()
        self.__selected_sensors_grouped_data = dict()

    """
    Method to set input data
    """

    def __set_data(self, data):
        for i in range(len(data)):
            self.__data["Sensor " + str(i + 1)] = data[i]
            self.__sensor_ids_list.append("Sensor " + str(i + 1))

    """
    Method to get the air quality for a given value of a metric
    """

    def __get_air_quality(self, attribute_name, attribute_value):
        if attribute_name not in self.__settings.keys():
            raise Exception(
                "Threshold not set for attribute in constants to calculate air_quality"
            )
        else:
            for (quality, threshold, _) in self.__settings[attribute_name]:
                if attribute_value <= float(threshold):
                    return quality

        return ("nan")

    """
    Method to reset all selected data
    """

    def __reset_selected_data(self):
        self.__selected_sensor_ids = list()
        self.__selected_sensors_grouped_data = dict()

    """
    Method to filter out the datapoints to only the given time period
    """

    def __filter_data_by_period(self, data_one_sensor, start_date, end_date):
        return True

    """
    Method which when given a time period, groups the data by the time period for each sensor
    and returns the value of the latest group
    """

    def __group_data_by_period(self, data_one_sensor, attribute, period="weekly"):
        grouped_data = dict()
        grouped_data["max"] = max(data_one_sensor[attribute].astype(float))
        grouped_data["min"] = min(data_one_sensor[attribute].astype(float))
        grouped_data["avg"] = round(sum(data_one_sensor[attribute].astype(float))/len(data_one_sensor[attribute]),2)
        grouped_data["air_quality"] = self.__get_air_quality(attribute, grouped_data["avg"])
        return grouped_data
