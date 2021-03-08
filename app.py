import banner
import layouts
import figures
import data
import widgets
import notifications
import tables

import json
import datetime


from tables import ListViewTablesObj

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os
import pandas as pd


data_obj = data.DataObj(os.path.join(".", "data", "InterestingWF"))
## Table object -> stores selected table data
table_object = ListViewTablesObj(data_obj.loaded_data, data_obj.settings, "PM2.5_Std")


data_table = pd.DataFrame.transpose(
    pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data())
)

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
    html.Div(id="setting-cache", style={"display": "none"}, children=settings_json)


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
        return layouts.overview_layout(data_obj)
    else:
        return layouts.overview_layout(data_obj)


@app.callback(
    [
        Output("table-sensors-selection", "disabled"),
        Output("table-sensors-selection", "value"),
    ],
    Input("all-sensors-checkbox", "value"),
)
def all_sensor_checked(checked):
    ids = list(data_obj.data.keys())
    if checked:
        return True, ids
    else:
        return False, ids


@app.callback(
    [
        Output("map-figure", "figure"),
        Output("list_table", "data"),
        Output("list_table", "columns"),
    ],
    [
        Input("interval-component", "n_intervals"),
        Input("table-sensors-selection", "value"),
        State("param-drop", "value"),
        State("date-picker", "start_date"),
        State("date-picker", "end_date"),
    ],
)
def update_figures(counter, table_sensors_list, param, start_date, end_date):
    """
    Call back function to update figures and tables
    """
    data_obj.increment_data()
    map_fig = figures.map_figure(data_obj, param=param)
    map_fig.update_layout(transition_duration=500)

    data_table = tables.get_data_table(data_obj, table_sensors_list, param, start_date, end_date)

    table_data = data_table.to_dict("records")
    table_columns = [{"name": i.upper(), "id": i} for i in data_table.columns]

    return (
        map_fig,
        table_data,
        table_columns,
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
# widgets.callbacks(app)
# notifications.callbacks(app)

if __name__ == "__main__":

    # for heroku:
    # * drop the "port=8051
    # * change build_tabs value to "intro"
    app.run_server(debug=True, port=8051)
