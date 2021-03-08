import banner
import layouts
import figures
import data
import widgets
import notifications

import json
import datetime


from tables import ListViewTablesObj

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate
import os
import pandas as pd


data_obj = data.DataObj(os.path.join(".", "data", "InterestingWF"))
## Table object -> stores selected table data
table_object = ListViewTablesObj(data_obj.loaded_data, data_obj.settings, "PM2.5_Std")
disable_update_button = True
disable_list_view_dropdown = True
# table_object.set_data(data_obj.loaded_data)
# table_object.set_settings(data_obj.settings)

data_table = pd.DataFrame.transpose(
    pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data())
)
sensors_list = table_object.get_all_sensor_ids()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.GRID])
app.config.suppress_callback_exceptions = True
server = app.server

def update_timer():
    return dcc.Interval(
        id="interval-component", interval=5 * 1000, n_intervals=0,  # 5 seconds
    )

def cache_settings(settings):
    """ store the settings in a hidden div """
    settings_json = json.dumps(settings)
    html.Div(id='setting-cache', style={'display': 'none'}, children=settings_json)

app.layout = html.Div(
    id="outer layout",
    children=[
        layouts.layout_all(app, data_obj),
        # The following are helper components, which are built
        # within the app but not necessarily displayed
        banner.generate_learn_button(),
        banner.generate_settings_button(data_obj),
        update_timer(),
        cache_settings(data_obj.settings),
    ],
)



@app.callback(
    Output("app-content", "children"), [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "sensors":
        return layouts.sensor_layout(data_obj)
    elif tab_switch == "overview":
        return layouts.overview_layout(data_obj, data_table, sensors_list, table_object.get_all_sensor_ids(), disable_update_button, disable_list_view_dropdown)
    else:
        return layouts.overview_layout(data_obj, data_table, sensors_list, table_object.get_all_sensor_ids(), disable_update_button, disable_list_view_dropdown)

@app.callback(
    [
        Output("map-figure", "figure"),
        Output("list_table", "data"),
        Output("list_table", "columns"),
        Output("overview-donut", "figure"),
        Output("overview-donut-all", "figure"),
        Output("overview-hist", "figure"),
        Output("submit-period", "n_clicks"),
        Output("submit-period", "disabled"),
        Output("list-view-senor-drop", "disabled"),
        Output("list-view-senor-drop", "value")
    ],
    [
        Input("interval-component", "n_intervals"),
        State("param-drop", "value"),
        State("list-view-senor-drop", "value"),
        State("start-date-dropdown", "date"),
        State("start-hour-dropdown", "value"),
        State("start-min-dropdown", "value"),
        State("end-date-dropdown", "date"),
        State("end-hour-dropdown", "value"),
        State("end-min-dropdown", "value"),
        State("submit-period", "n_clicks"),
        State("list-view-checklist", "value"),
    ],
)
def update_map(counter,
               param,
               new_selected_sensors_list,
               start_date,
               start_hr,
               start_min,
               end_date,
               end_hr,
               end_min,
               period_button_clicks,
               list_view_dropdown_checklist):
    """
    Call back function to update map and list view table data upon change in drop down value
    """
    data_obj.increment_data()
    map_fig = figures.map_figure(data_obj, param=param)
    map_fig.update_layout(transition_duration=500)

    if start_date is not None and end_date is not None and start_min is not None and start_hr is not None and end_hr is not None and end_min is not None:
        disable_update_button = False
    else:
        disable_update_button = True

    if list_view_dropdown_checklist is not None and len(list_view_dropdown_checklist) and list_view_dropdown_checklist[0] == 'All sensors':
        new_selected_sensors_list = table_object.get_all_sensor_ids()
        disable_list_view_dropdown = True
    else:
        disable_list_view_dropdown = False

    ## Modify period selected
    if period_button_clicks > 0:
        start = datetime.datetime.strptime(str(start_date) + ' ' + str(start_hr) + ':' + str(start_min),
                                           '%Y-%m-%d %H:%M')
        end = datetime.datetime.strptime(str(end_date) + ' ' + str(end_hr) + ':' + str(end_min),
                                           '%Y-%m-%d %H:%M')
        table_object.set_period(start, end)

    ## Modify selected selected sensor ids
    old_selected_sensors_list = table_object.get_selected_sensor_ids()
    if len(new_selected_sensors_list) == 0:
        table_object.remove_all_sensors_from_selected_list()
    elif len(old_selected_sensors_list) < len(new_selected_sensors_list):
        for sensor_id in new_selected_sensors_list:
            table_object.add_sensor_to_selected_list(sensor_id)
    elif len(old_selected_sensors_list) > len(new_selected_sensors_list):
        for sensor_id in old_selected_sensors_list:
            if sensor_id not in new_selected_sensors_list:
                table_object.remove_sensor_from_selected_list(sensor_id)

    ## Modify selected attribute
    table_object.set_attr_selected(param)
    data_table = pd.DataFrame.transpose(
        pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data())
    )
    data_table = data_table.reset_index()
    list_view_columns = [{"name": i.upper(), "id": i} for i in data_table.columns]
    list_view_table_data = data_table.to_dict("records")

    overview_fig = figures.overview_donut(data_obj, param)
    overview_all_fig = figures.overview_donuts_all_param(data_obj)
    overview_hist = figures.overview_histogram(data_obj, param)
    return (
        map_fig,
        list_view_table_data,
        list_view_columns,
        overview_fig,
        overview_all_fig,
        overview_hist,
        0,
        disable_update_button,
        disable_list_view_dropdown,
        new_selected_sensors_list
    )


@app.callback(Output("play-button", "children"), [Input("play-button", "n_clicks")])
def change_button_text(n_clicks):
    if n_clicks % 2 == 0:
        return "Pause"
    else:
        return "Play"


@app.callback(
    output=Output("line-graph", "figure"),
    inputs=[
        Input("interval-component", "n_intervals"),
        Input("sensor-drop", "value"),
        Input("play-button", "n_clicks"),
    ],
)
def update_line_on_interval(counter, sensors, n_clicks):
    dropdown_triggered = "sensor-drop" in str(dash.callback_context.triggered)
    play_button_triggered = "play-button.n_clicks" in str(
        dash.callback_context.triggered
    )
    if n_clicks % 2 == 0:
        data_obj.increment_data()
        return figures.line_figure(data_obj, sensors, show_timeselector=False)
    elif dropdown_triggered:
        return figures.line_figure(data_obj, sensors, show_timeselector=True)
    elif play_button_triggered:
        return figures.line_figure(data_obj, sensors, show_timeselector=True)
    else:
        raise PreventUpdate


banner.button_callbacks(app)
banner.settings_callbacks(app, data_obj.settings)
widgets.callbacks(app)
# notifications.callbacks(app)

if __name__ == "__main__":

    # for heroku:
    # * drop the "port=8051
    # * change build_tabs value to "intro"
    app.run_server(debug=True, port=8051)
