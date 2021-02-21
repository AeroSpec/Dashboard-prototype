
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import figures
import dash_table


def build_tabs():
    return html.Div(
        className="tabs-header",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Overview-tab",
                        label="Overview",
                        value="overview",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Sensors",
                        value="sensors",
                    ),
                ],
            )
        ],
    )


def sensor_dropdown(data_obj):
    return dcc.Dropdown(id='sensor-drop'
                                 , options=[
                                    {'label': f'Sensor {i}', 'value': i} for i in range(1, data_obj.sensors_count + 1)],
                                 value=[1],
                                 multi=True, clearable=False
                 )

def line_graph(data_obj, fig):
    return dcc.Graph(
                     id='line-graph',
                     figure=fig
                 )

def calendar_heatmap():
    fig = figures.display_years()
    return dcc.Graph(
                     id='calendar-heatmap',
                     figure=fig
                 )

def build_sensors_tab(data_obj, fig):
    return html.Div(
        id="sensors_tab",
        className="tabs",
        children=[
                sensor_dropdown(data_obj),
                line_graph(data_obj, fig),
                calendar_heatmap(),
                ]
            )


def param_dropdown(data_obj):
    return html.Div(
        className="dashboard-component",
        children=[
                        html.P(),  # this creates a new paragraph
                        html.H6('Parameter'),
                        dcc.Dropdown(id='param-drop'
                                     , options=[
                                {'label': i, 'value': i} for i in data_obj.params],
                                     value='PM2.5_Std',
                                     multi=False, clearable=False
                                     ),
                    ])

def map_figure():
    return dcc.Graph(id='map-figure')

def list_table(data_obj, list_view_table = pd.DataFrame()):
    list_view_columns = list()
    list_view_data = list()
    if len(list_view_table) != 0:
        list_view_table = list_view_table.reset_index()
        print(list_view_table)
        list_view_columns = [{"name": i.upper(), "id": i} for i in list_view_table.columns]
        list_view_data = list_view_table.to_dict('records')

    return html.Div([
                    dash_table.DataTable(
                        id='list_table',
                        columns=list_view_columns,
                        data=list_view_data,
                    ),
                ])

def key_stats():
    return html.Div(
        id="key-stats",
        className="dashboard-component",
        children = [
                        html.P(),
                        html.H6('Key Stats'),
                        # get_key_stats()
                    ])

def notifications():
    return html.Div(
        [
            dbc.Button(
                "Notification",
                id="auto-toast-toggle",
                color="primary",
                className="notification",
            ),
            # dbc.Toast(
            #     [html.P("The sensors have gone haywire!", className="mb-0")],
            #     id="auto-toast",
            #     header="Alert",
            #     icon="primary",
            #     duration=4000,
            #     dismissable=True,
            # ),
        ]
    )

# @app.callback(
#     Output("auto-toast", "is_open"), [Input("auto-toast-toggle", "n_clicks")]
# )
# def open_toast(n):
#     return True


def stats_panel():
    return html.Div(
        id="quick-stats",
        className="quick-stats",
        children=[
            html.Div(
                id="card-1",
                children=[
                    key_stats(),
                ],
            ),
            html.Div(
                id="card-2",
                children=[
                    html.P("More Data"),
                ],
            ),
            html.Div(
                id="notifications-card",
                children=notifications()
            ),
        ],
    )

def build_overview_tab(data_obj, list_view_table = pd.DataFrame()):
    return html.Div(
    id="overview_tab",
    className="tabs",
    children=[
        dbc.Row([
            dbc.Col(param_dropdown(data_obj), width=6),
            dbc.Col(key_stats(), width=6)
        ],no_gutters=True,),
        dbc.Row(
            dbc.Col(map_figure(), width="auto"),
        ),
        dbc.Row(
            dbc.Col(
                list_table(data_obj, list_view_table),
            )
        ),
    ]
)


