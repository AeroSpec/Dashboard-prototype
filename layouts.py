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
from datetime import date


def layout_all(app, data_obj):
    return html.Div(
        [
            dbc.Row(dbc.Col(banner.build_banner_v3(app), width=12), no_gutters=True),
            dbc.Row(dbc.Col(build_tabs(), width=10),),  # no_gutters=True),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id="app-content", className="main-layout",), width=8,
                    ),
                    dbc.Col(notifications.notifications(data_obj), width=2),
                ],
                no_gutters=True,
            ),
        ]
    )


def overview_layout(data_obj):
    return dbc.Container(
        className="main-layout",
        fluid=True,
        children=[
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(build_overview_tab(data_obj), width="auto",),
                            # dbc.Col(summary.pvi_component(data_obj), width="auto"),
                        ],
                        no_gutters=True,
                    ),
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
                                width=12,
                            ),
                        ],
                        no_gutters=True,
                    ),
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
                value="intro",
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
            html.P(),
            html.H6("Sensors"),
            dcc.Dropdown(
                id="sensor-drop",
                options=[
                    {"label": sensor, "value": sensor}
                    for sensor in data_obj.data.keys()
                ],
                value=["Sensor 1"],
                multi=True,
                clearable=False,
            ),
        ],
    )


def play_button():
    return html.Div(
        className="dashboard-component",
        children=[
            html.P(),
            html.H6("Streaming data"),
            html.Button("Pause", id="play-button", n_clicks=0),
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
            dbc.Row(dbc.Col(calendar_heatmap(data_obj))),
        ],
    )


def param_dropdown(data_obj):
    return html.Div(
        className="dashboard-component",
        children=dbc.Row(
            [
                dbc.Col(html.H4("Parameter"), width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id="param-drop",
                        options=[{"label": i, "value": i} for i in data_obj.params],
                        value="PM2.5_Std",
                        multi=False,
                        clearable=False,
                    ),
                    width=8,
                ),
            ]
        ),
    )


def list_view_dropdown(sensors_list):
    return html.Div(
        className="dashboard-component",
        children=[
            dcc.Dropdown(
                id="sensors-selection",
                options=[{"label": i, "value": i} for i in sensors_list],
                multi=True,
                clearable=False,
            ),
        ],
    )


def list_view_checklist():
    return html.Div(
        className="dashboard-component",
        children=[
            dcc.Checklist(
                id="all-sensors-checkbox",
                options=[{"label": " All sensors", "value": "All sensors"},],
                value=["All sensors"],
            )
        ],
    )


def datetime_dropdown(initial_date, initial_hour, initial_min, id_prefix):
    hour_range_values = [str(i) for i in range(24)]
    min_range_values = [str(i) for i in range(60)]
    return [
        dbc.Col(width=2,),
        dbc.Col(
            html.Div(
                dcc.DatePickerSingle(
                    id=id_prefix + "-date-dropdown",
                    min_date_allowed=date(2020, 6, 1),
                    max_date_allowed=date.today(),
                    placeholder=initial_date,
                ),
                className="dashboard-component",
            ),
            width=1.5,
        ),
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id=id_prefix + "-hour-dropdown",
                    options=[
                        {"label": str(i).zfill(2), "value": str(i).zfill(2)}
                        for i in hour_range_values
                    ],
                    multi=False,
                    placeholder=initial_hour,
                ),
                className="dashboard-component",
            ),
            width=1,
        ),
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id=id_prefix + "-min-dropdown",
                    options=[
                        {"label": str(i).zfill(2), "value": str(i).zfill(2)}
                        for i in min_range_values
                    ],
                    multi=False,
                    placeholder=initial_min,
                ),
                className="dashboard-component",
            ),
            width=1,
        ),
    ]


def list_view_submit_button(disable_update_button):

    return html.Div(
        children=[
            html.Button(
                "Update",
                id="submit-period",
                className="app_update_button",
                n_clicks=0,
                style={"color": "black"},
                disabled=disable_update_button,
            ),
        ],
        className="button-container",
    )


def map_figure():
    return dcc.Graph(id="map-figure", className="dashboard-component")


def table_colors(colors):

    return [
        {
            "if": {
                "column_id": "Average Air Quality",
                "filter_query": "{Average Air Quality} = Good",
            },
            "backgroundColor": colors[0],
            "color": "black",
        },
        {
            "if": {
                "column_id": "Average Air Quality",
                "filter_query": "{Average Air Quality} = Moderate",
            },
            "backgroundColor": colors[1],
            "color": "black",
        },
        {
            "if": {
                "column_id": "Average Air Quality",
                "filter_query": "{Average Air Quality} = Unhealthy",
            },
            "backgroundColor": colors[2],
            "color": "black",
        },
        {
            "if": {
                "column_id": "Average Air Quality",
                "filter_query": '{Average Air Quality} = "Very Unhealthy"',
            },
            "backgroundColor": colors[3],
            "color": "black",
        },
        {
            "if": {
                "column_id": "Average Air Quality",
                "filter_query": "{Average Air Quality} = Hazardous",
            },
            "backgroundColor": colors[4],
            "color": "white",
        },
    ]


def list_table(data_obj):

    colors = [row[2].format(0.5) for row in data_obj.settings["PM2.5_Std"]]

    return html.Div(
        className="dashboard-component",
        children=[
            dash_table.DataTable(
                id="list_table",
                # columns=list_view_columns,
                # data=list_view_data,
                sort_action="native",
                sort_mode="single",
                style_cell={"font-family": "sans-serif"},
                style_header={
                    "backgroundColor": "lightgray",
                    "color": "black",
                    "font_size": "20px",
                    "font-family": "sans-serif",
                    "border": "1px solid black",
                },
                style_data_conditional=table_colors(colors),
            ),
        ],
    )


def overview_hist(data_obj):
    return dcc.Graph(
        id="overview-hist",
        figure=figures.overview_histogram(data_obj, None),
        config={"displayModeBar": False},
    )


def overview_status(data_obj):
    return html.H4(
        id="overview-status", children=[figures.overview_status(data_obj, None)]
    )


def overview_donut(data_obj):
    return dcc.Graph(
        id="overview-donut",
        className="graph-medium",
        figure=figures.overview_donut(data_obj, None),
        config={"displayModeBar": False},
    )


def overview_donut_all(data_obj):
    return dcc.Graph(
        id="overview-donut-all",
        className="graph-medium",
        figure=figures.overview_donuts_all_param(data_obj),
        config={"displayModeBar": False},
    )


def overview_hist_component(data_obj):
    return html.Div(
        id="key-stats",
        className="dashboard-component",
        children=dbc.Row(
            [
                dbc.Col(overview_status(data_obj), width=4),
                dbc.Col(overview_hist(data_obj), width=8),
            ]
        ),
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
        children=[
            html.H6("Key Parameters Overview"),
            html.Hr(),
            overview_donut_all(data_obj),
        ],
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


def overview_map_and_dropdowns(data_obj):
    sensors = list(data_obj.data.keys())

    return html.Div(
        className="dashboard-component",
        children=[
            dbc.Row(
                [
                    dbc.Col(param_dropdown(data_obj), width=6),
                    dbc.Col(overview_hist_component(data_obj), width=6),
                ],
                no_gutters=True,
            ),
            dbc.Row(
                [
                    dbc.Col(html.H5("Select Sensors"), width=2),
                    dbc.Col(list_view_dropdown(sensors), width=8),
                    dbc.Col(list_view_checklist(), width=2),
                ],
                no_gutters=True,
            ),
            dbc.Row(dbc.Col(map_figure(), width=12), no_gutters=True,),
        ],
    )


def build_overview_tab(data_obj):
    return dbc.Container(
        id="overview_tab",
        className="tabs",
        fluid=True,
        children=[
            dbc.Row([dbc.Col(overview_map_and_dropdowns(data_obj))]),
            dbc.Row([dbc.Col(list_table_component(data_obj)),], no_gutters=True,),
        ],
    )


def list_table_component(data_obj,):

    return html.Div(
        id="list-table-container",
        className="dashboard-component",
        children=[
            dbc.Row(
                [
                    dbc.Col(html.H6("Select Period"), width=2),
                    dbc.Col(widgets.date_picker(), width="auto"),
                ],
                no_gutters=True,
            ),
            dbc.Row(dbc.Col(list_table(data_obj)), no_gutters=True),
        ],
    )
