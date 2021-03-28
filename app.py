import banner
import layouts
import figures
import data

import os
import json

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


data_obj = data.DataObj(os.path.join(".", "data", "InterestingWF"))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.GRID])
app.config.suppress_callback_exceptions = True
server = app.server


def update_timer():
    """
    This element is used to increment the data, every 5 seconds.

    See also: update_figures method.
    """
    return dcc.Interval(
        id="interval-component", interval=5 * 1000, n_intervals=0,  # 5 seconds
    )


def cache_settings(settings):
    """ store the settings in a hidden div """
    # Note: this is not currently used. See settings_callbacks in banner.py
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
    """ Trigger to switch the layout when the tabs are selected """
    if tab_switch == "sensors":
        return layouts.sensor_layout(data_obj)
    elif tab_switch == "overview":
        return layouts.overview_layout(data_obj)
    else:
        return layouts.overview_layout(data_obj)


@app.callback(
    [Output("sensors-selection", "disabled"), Output("sensors-selection", "value"),],
    Input("all-sensors-checkbox", "value"),
)
def all_sensor_checked(checked):
    """ Toggle the sensors boxes on the overview panel """
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
        Output("overview-hist", "figure"),
        Output("overview-status", "children"),
    ],
    [
        Input("interval-component", "n_intervals"),
        Input("sensors-selection", "value"),
        Input("param-drop", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("floorplan-upload", "contents"),
    ],
)
def update_figures(counter, sensors_list, param, start_date, end_date, file_contents):
    """
    Update figures and tables.

    Notes
    -----
    When any of the "Input" items are changed, this function is triggered.
    """
    data_obj.fetch_data()
    map_fig = figures.map_figure(
        data_obj, sensors_list, image=file_contents, param=param
    )
    map_fig.update_layout(transition_duration=500)

    data_table = data.get_data_table(
        data_obj, sensors_list, param, start_date, end_date
    )

    table_data = data_table.to_dict("records")
    table_columns = [{"name": i.upper(), "id": i} for i in data_table.columns]

    overview_hist = figures.overview_histogram(data_obj, param)
    overview_status = figures.overview_status(data_obj, param)

    return (map_fig, table_data, table_columns, overview_hist, overview_status)


@app.callback(Output("play-button", "children"), [Input("play-button", "n_clicks")])
def change_button_text(n_clicks):
    if n_clicks % 2 == 0:
        return "Pause"
    else:
        return "Play"


@app.callback(
    output=Output("line-graph", "figure"),
    inputs=[Input("sensor-drop", "value"), Input("play-button", "n_clicks"),],
)
def update_line_on_interval(sensors, n_clicks):
    dropdown_triggered = "sensor-drop" in str(dash.callback_context.triggered)
    play_button_triggered = "play-button.n_clicks" in str(
        dash.callback_context.triggered
    )
    if n_clicks % 2 == 0:
        data_obj.fetch_data()
        return figures.line_figure(data_obj, sensors, show_timeselector=False)
    elif dropdown_triggered:
        return figures.line_figure(data_obj, sensors, show_timeselector=True)
    elif play_button_triggered:
        return figures.line_figure(data_obj, sensors, show_timeselector=True)
    else:
        raise PreventUpdate


# link the callbacks from other sources
banner.button_callbacks(app)
banner.settings_callbacks(app, data_obj.settings)
# widgets.callbacks(app)
# notifications.callbacks(app)

if __name__ == "__main__":

    # for heroku:
    # * drop the "port=8051
    app.run_server(debug=True, port=8051)
