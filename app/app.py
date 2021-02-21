import banner
import layouts
import figures
import data
import os
import pandas as pd

from tables import ListViewTablesObj

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output








data_obj = data.DataObj(os.path.join(".", "data", "Clean UW"))
id1 = list(data_obj.data.keys())[0]
df = data_obj.data[id1]['data']

fig1 = figures.map_figure(df)
fig2 = figures.line_figure(df)
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True







app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])
app.config.suppress_callback_exceptions = True

'''
Construct table data for list view
'''
## Table object -> stores selected table data
table_object = ListViewTablesObj()
table_object.set_data(data_obj.loaded_data)

## Default selected attribute
table_object.set_attr_selected('PM10_Std')

## TODO - Remove and add values selected by user in list view
table_object.add_sensor_to_selected_list('Sensor 11')
table_object.add_sensor_to_selected_list('Sensor 12')
table_object.add_sensor_to_selected_list('Sensor 13')
table_object.add_sensor_to_selected_list('Sensor 14')
table_object.add_sensor_to_selected_list('Sensor 15')

data_table = pd.DataFrame.transpose(pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data()))

app.layout = html.Div(
    id="outer layout",
    children=[
        banner.build_banner(app),
        html.Div(
            id="app-container",
            children=[
                layouts.build_tabs(),
                # Main app
                html.Div(id="app-content"),

            ],

        ),
        # The following are helper components
        banner.generate_learn_button(),
        banner.generate_settings_button(),
        dcc.Interval(
            id="interval-component",
            interval=5*1000,  # 5 seconds
            n_intervals=0,
        ),

    ],
)






@app.callback(
    Output("learn", "style"),
    [Input("learn-more-button", "n_clicks"),
     Input("markdown_close", "n_clicks"),
     ],
)
def trigger_learn_more(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if prop_id == "learn-more-button":
            return {"display": "block"}
    return {"display": "none"}

@app.callback(
    Output("settings", "style"),
    [Input("settings-button", "n_clicks"),
     Input("settings-close", "n_clicks"),
     ],
)
def trigger_settings(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if prop_id == "settings-button":
            return {"display": "block"}
    return {"display": "none"}


layout1 = dbc.Container(html.Div(
    [
        dbc.Row(
            [
                dbc.Col(layouts.build_overview_tab(data_obj, data_table), width="auto"),
                #dbc.Col(stats_panel(), width=2),
            ],
            no_gutters=True,
        ),
    ]
),fluid=True)

layout2 = dbc.Container(html.Div(
    [
        dbc.Row(
            [
                dbc.Col(layouts.build_sensors_tab(data_obj, fig2), width=7),
                dbc.Col(layouts.stats_panel(), width=2),
            ],
            no_gutters=True,
        ),
    ]
),fluid=True)


@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "sensors":
        return layout2
    elif tab_switch == 'overview':
        return layout1
    else:
        return layout1



'''
Call back function to update map and list view table data upon change in drop down value
'''
@app.callback(
    [Output('map-figure', 'figure'), Output('list_table', 'data'), Output('list_table', 'columns')],
    [Input('param-drop', 'value')])
def update_map(params):
    """
    """
    fig = figures.map_figure(data_obj, params = params)
    fig.update_layout(transition_duration=500)

    table_object.set_attr_selected(params)
    data_table = pd.DataFrame.transpose(pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data()))
    data_table = data_table.reset_index()
    list_view_columns = [{"name": i.upper(), "id": i} for i in data_table.columns]
    list_view_table_data = data_table.to_dict('records')

    return fig, list_view_table_data, list_view_columns


@app.callback(
    output=Output("line-graph", "figure"),
    inputs=[Input("interval-component", "n_intervals")],
)
def update_line_on_interval(counter):
    data_obj.increment_data()

    id1 = list(data_obj.data.keys())[0]
    df = data_obj.data[id1]['data']
    return figures.line_figure(df)

banner.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
