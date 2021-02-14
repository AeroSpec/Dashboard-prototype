import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime


def list_view_table(df_list):
    x = df_list.index
    y = df_list['PM2.5_Std']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x, y=y,
                             mode='lines',
                             name='lines'),
                             secondary_y=True,
             )
    return fig


def __does_date_lie_in_period(curr_date, earlier_date, period):
        return True


# Method which when given a time period, groups the data by the time period for each sensor
# and returns the value of the latest group
def __group_data_by_period(data_one_sensor, period):
    grouped_data = dict()
    total_temp = 0
    total_data_points = 1
    curr_date = datetime.datetime.now()

    # 1. Temperature data
    grouped_data['max_temp'] = 0
    grouped_data['min_temp'] = 1000  # some high value
    air_quality = 'NA'

    for ind, row in data_one_sensor.iterrows():
        try:
            data_modified = dict()
            earlier_date = datetime.datetime.strptime(data_one_sensor.Date[ind] + ' ' + data_one_sensor.Time[ind],
                                                      '%Y/%m/%d %H:%M:%S')

            if __does_date_lie_in_period(curr_date, earlier_date, period):
                # Add to total and increase count for average caclculation
                total_temp += row[['Temp(C)']]
                total_data_points += 1

                # Get max and min temp
                grouped_data['max_temp'] = max(grouped_data['max_temp'], row['Temp(C)'])
                grouped_data['min_temp'] = min(grouped_data['min_temp'], row['Temp(C)'])
                air_quality = 'GOOD'

        except Exception as e:
            continue
            # print(e)
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
    return grouped_data


def get_data_table(df_list):
    # Create a dummy data table using Dash & Plotly
    curr_sensor_id = 1
    df_grouped_by_sensor = dict()
    for data_sensor in df_list:
        df_grouped_by_sensor["Sensor " + str(curr_sensor_id - 1)] = __group_data_by_period(data_sensor, 'weekly')
        # print("Successfully grouping data for sensor: " + str(curr_sensor_id) + str(
        #     df_grouped_by_sensor["Sensor " + str(curr_sensor_id - 1)]['avg_temp']))
        curr_sensor_id = curr_sensor_id + 1

    df1 = pd.DataFrame.transpose(pd.DataFrame(df_grouped_by_sensor))
    df1 = df1.reset_index()
    df = df1

    return df
