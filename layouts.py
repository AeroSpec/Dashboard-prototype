import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import figures
import dash_table
import banner
import summary
import widgets
import notifications


def layout_all(app):
    return html.Div(
        [
            dbc.Row(dbc.Col(banner.build_banner_v3(app), width=12), no_gutters=True),
            dbc.Row(dbc.Col(build_tabs(), width=12), no_gutters=True),
            dbc.Row(
                [dbc.Col(
                    html.Div(
                        id="app-content",
                        className="main-layout",
                        # children=overview_layout(),
                    ),
                    width=8,
                ),
                dbc.Col(notifications.notifications(), width=4)],
                no_gutters=True,
            ),
        ]
    )


def overview_layout(data_obj, data_table, sensors_list):
    return dbc.Container(
        className="main-layout",
        fluid=True,
        children=[
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                build_overview_tab(data_obj, data_table, sensors_list),
                                width="auto",
                            ),
                            dbc.Col(
                                summary.pvi_component(data_obj, "Hey"), width="auto"
                            ),
                            dbc.Col(
                                overview_donut_component(data_obj,), width="auto"
                            ),
                            dbc.Row(dbc.Col(widgets.get_daily_osha_noise_exposure_progress(data_obj), width="auto"),
                                    no_gutters=True),
                        ],
                        no_gutters=True,
                    ),
                    dbc.Row(dbc.Col(overview_donut_all_params_component(data_obj), width="auto"), no_gutters=True),
                ]
            ),
        ],
    )


def sensor_layout(data_obj):
    return dbc.Container(
        className="main-layout",
        fluid=True,
        children=[
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                build_sensors_tab(data_obj, figures.empty_fig()),
                                width=7,
                            ),
                            #dbc.Col(stats_panel(), width=5),
                        ],
                        no_gutters=True,
                    ),
                    # dbc.Row(dbc.Col(widgets.date_picker(data_obj), width=12), no_gutters=True),
                    # dbc.Row(dbc.Col(widgets.thermometer(df), width=12), no_gutters=True),
                ]
            ),
        ],
    )


def build_tabs():
    return html.Div(
        className="dashboard-tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="overview",#""intro",
                className="custom-tabs",
                children=[
                    dcc.Tab(id="Overview-tab", label="Overview", value="overview",),
                    dcc.Tab(id="Control-chart-tab", label="Sensors", value="sensors",),
                ],
            )
        ],
    )


def sensor_dropdown(data_obj):
    return html.Div(
        className="dashboard-component",
        children=[
            html.P(),  # this creates a new paragraph
            html.H6("Sensors"),
            dcc.Dropdown(
                id="sensor-drop",
                options=[
                    {"label": f"Sensor {i}", "value": i}
                    for i in range(1, data_obj.sensors_count + 1)
                ],
                value=[1],
                multi=True,
                clearable=False,
            )
        ],
    )

def play_button():
    return html.Div(
        className="dashboard-component",
        children=[
            html.P(),  # this creates a new paragraph
            html.H6("Streaming data"),
            html.Button("Pause", 
                id='play-button',
                n_clicks = 0
            )
        ],
    )

def line_graph(data_obj, fig):
    return dcc.Graph(id="line-graph", figure=fig)


def calendar_heatmap(data_obj):
    fig = figures.display_years(data_obj)
    return dcc.Graph(id="calendar-heatmap", figure=fig)


def build_sensors_tab(data_obj, fig):
    return html.Div(
        id="sensors_tab",
        className="dashboard-component",
        children=[
            dbc.Row(
                [
                    dbc.Col(sensor_dropdown(data_obj), width=6),
                    dbc.Col(play_button(), width=6),
                ],
                no_gutters=True,
            ),
            dbc.Row(dbc.Col(line_graph(data_obj, fig))),
            dbc.Row(dbc.Col(calendar_heatmap(data_obj)))
        ],
    )

def param_dropdown(data_obj):
    return html.Div(
        className="dashboard-component",
        children=[
            html.P(),  # this creates a new paragraph
            html.H6("Parameter"),
            dcc.Dropdown(
                id="param-drop",
                options=[{"label": i, "value": i} for i in data_obj.params],
                value="PM2.5_Std",
                multi=False,
                clearable=False,
            ),
        ],
    )


def list_view_dropdown(sensors_list, dropdown_name):
    return html.Div(
        className="dashboard-component",
        children=[
            html.P(),  # this creates a new paragraph
            html.H6(dropdown_name),
            dcc.Dropdown(
                id="list-view-senor-drop",
                options=[{"label": i, "value": i} for i in sensors_list],
                value=sensors_list,
                multi=True,
            ),
        ],
    )


def map_figure():
    return dcc.Graph(id="map-figure", className="dashboard-component")


def list_table(data_obj, list_view_table=pd.DataFrame()):
    list_view_columns = list()
    list_view_data = list()
    if len(list_view_table) != 0:
        list_view_table = list_view_table.reset_index()
        list_view_columns = [
            {"name": i.upper(), "id": i} for i in list_view_table.columns
        ]
        list_view_data = list_view_table.to_dict("records")

    return html.Div(
        className="dashboard-component",
        children=[
            dash_table.DataTable(
                id="list_table",
                columns=list_view_columns,
                data=list_view_data,
                sort_action="native",
                sort_mode="single",
                style_data_conditional=[
                    {
                        "if": {
                            "column_id": "air_quality",
                            "filter_query": "{air_quality} = Good",
                        },
                        "backgroundColor": "green",
                        "color": "white",
                    },
                    {
                        "if": {
                            "column_id": "air_quality",
                            "filter_query": "{air_quality} = Moderate",
                        },
                        "backgroundColor": "#3D9970",
                        "color": "white",
                    },
                    {
                        "if": {
                            "column_id": "air_quality",
                            "filter_query": "{air_quality} = Unhealthy",
                        },
                        "backgroundColor": "yellow",
                        "color": "white",
                    },
                    {
                        "if": {
                            "column_id": "air_quality",
                            "filter_query": '{air_quality} = "Very Unhealthy"',
                        },
                        "backgroundColor": "orange",
                        "color": "white",
                    },
                    {
                        "if": {
                            "column_id": "air_quality",
                            "filter_query": "{air_quality} = Hazardous",
                        },
                        "backgroundColor": "red",
                        "color": "white",
                    },
                ],
            ),
        ],
    )


def overview_hist(data_obj):
    return dcc.Graph(
        id="overview-hist", figure=figures.overview_histogram(data_obj, None)
    )

def overview_donut(data_obj):
    return dcc.Graph(
        id="overview-hist", className='graph-medium', figure=figures.overview_donut(data_obj, None)
    )

def overview_donut_all(data_obj):
    return dcc.Graph(
        id="overview-hist", className='graph-medium', figure=figures.overview_donuts_all_param(data_obj)
    )


def overview_hist_component(data_obj):
    return html.Div(
        id="key-stats",
        className="dashboard-component",
        children=[overview_hist(data_obj)],
    )


def overview_donut_component(data_obj):

    return html.Div(
        id="key-stats-donut",
        className="dashboard-component",
        children=[html.H6("Parameter Overview"), html.Hr(), overview_donut(data_obj)],
    )

def overview_donut_all_params_component(data_obj):
    return html.Div(
        id="key-stats-donut",
        className="dashboard-component",
        children=[html.H6("Key Parameters Overview"), html.Hr(), overview_donut_all(data_obj)],
    )


def key_stats():
    return html.Div(
        id="key-stats",
        className="dashboard-component",
        children=[
            html.P(),
            html.H6("Key Stats"),
            # get_key_stats()
        ],
    )

def stats_panel():
    return html.Div(
        id="quick-stats",
        className="dashboard-component",
        children=[
            html.Div(id="card-1", children=[key_stats(),],),
            html.Div(id="card-2", children=[html.P("More Data"),],),
            html.Div(id="notifications-card", children=notifications.notifications()),
        ],
    )


def build_overview_tab(data_obj, list_view_table=pd.DataFrame(), sensors_list=list()):
    return html.Div(
        id="overview_tab",
        className="tabs",
        children=[
            dbc.Row(
                [
                    dbc.Col(param_dropdown(data_obj), width=6),
                    dbc.Col(overview_hist_component(data_obj), width=6),
                ],
                no_gutters=True,
            ),
            dbc.Row(dbc.Col(map_figure(), width="auto"),),
            dbc.Row(
                [dbc.Col(list_view_dropdown(sensors_list, "Select sensors"), width=6),],
                no_gutters=True,
            ),
            dbc.Row(dbc.Col(list_table(data_obj, list_view_table),)),
        ],
    )
