import banner
import layouts
import figures
import data

from tables import ListViewTablesObj

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import os
import pandas as pd


data_obj = data.DataObj(os.path.join(".", "data", "Clean UW"))
id1 = list(data_obj.data.keys())[0]
df = data_obj.data[id1]["data"]

fig1 = figures.map_figure(data_obj, 'PM2.5_Std')
fig2 = figures.line_figure(data_obj)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])
app.config.suppress_callback_exceptions = True
server = app.server

"""
Construct table data for list view
"""
## Table object -> stores selected table data
table_object = ListViewTablesObj()
table_object.set_data(data_obj.loaded_data)

## Default selected attribute
table_object.set_attr_selected("PM10_Std")


## TODO - Remove and add values selected by user in list view
table_object.add_sensor_to_selected_list("Sensor 11")
table_object.add_sensor_to_selected_list("Sensor 12")
table_object.add_sensor_to_selected_list("Sensor 13")
table_object.add_sensor_to_selected_list("Sensor 14")
table_object.add_sensor_to_selected_list("Sensor 15")

data_table = pd.DataFrame.transpose(
    pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data())
)


overview_layout = dbc.Container(
    className="main-layout",
    fluid=True,
    children=[
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            layouts.build_overview_tab(data_obj, data_table),
                            width="auto",
                        ),
                        # dbc.Col(stats_panel(), width=2),
                    ],
                    no_gutters=True,
                ),
            ]
        ),
    ],
)

sensor_layout = dbc.Container(
    className="main-layout",
    fluid=True,
    children=[
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(layouts.build_sensors_tab(data_obj, fig2), width=7),
                        dbc.Col(layouts.stats_panel(), width=5),
                    ],
                    no_gutters=True,
                ),
            ]
        ),
    ],
)


layout_all = html.Div(
    [
        dbc.Row(dbc.Col(banner.build_banner_v3(app), width=12), no_gutters=True),
        dbc.Row(dbc.Col(layouts.build_tabs(), width=12), no_gutters=True),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="app-content", className="main-layout", children=overview_layout
                ),
                width=12,
            ),
            no_gutters=True,
        ),
    ]
)


update_timer = dcc.Interval(
    id="interval-component", interval=5 * 1000, n_intervals=0,  # 5 seconds
)


app.layout = html.Div(
    id="outer layout",
    children=[
        layout_all,
        # The following are helper components, which are built
        # within the app but not necessarily displayed
        banner.generate_learn_button(),
        banner.generate_settings_button(data_obj),
        update_timer,
    ],
)


@app.callback(
    Output("app-content", "children"), [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "sensors":
        return sensor_layout
    elif tab_switch == "overview":
        return overview_layout
    else:
        return overview_layout


@app.callback(
    [   
        Output('map-figure', 'figure'),
        Output("list_table", "data"),
        Output("list_table", "columns"),
    ],
    [Input("interval-component", "n_intervals"),
    Input('param-drop', 'value')]
)
def update_map(counter, params):
    """
    Call back function to update map and list view table data upon change in drop down value
    """
    data_obj.increment_data()
    fig = figures.map_figure(data_obj, params=params)
    fig.update_layout(transition_duration=500)

    table_object.set_attr_selected(params)
    data_table = pd.DataFrame.transpose(
        pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data())
    )
    data_table = data_table.reset_index()
    list_view_columns = [{"name": i.upper(), "id": i} for i in data_table.columns]
    list_view_table_data = data_table.to_dict("records")

    return fig, list_view_table_data, list_view_columns

@app.callback(Output('play-button', 'children'), [Input('play-button', 'n_clicks')])
def change_button_text(n_clicks):
    if n_clicks % 2 == 0:
        return "Pause"
    else:
        return "Play"

@app.callback(
    output=Output("line-graph", "figure"),
    inputs=[Input("interval-component", "n_intervals"), 
    Input("sensor-drop", "value"),
    Input("play-button", "n_clicks")],
)
def update_line_on_interval(counter, params, n_clicks):
    dropdown_triggered = "sensor-drop" in str(dash.callback_context.triggered)
    if(n_clicks % 2 == 0):
        data_obj.increment_data()
        return figures.line_figure(data_obj, params=params)
    elif dropdown_triggered:
        return figures.line_figure(data_obj, params=params)
    else: 
        raise PreventUpdate       

banner.button_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)#, port=8051)
