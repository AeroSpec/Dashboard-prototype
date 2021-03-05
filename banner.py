import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_daq as daq
import plotly.graph_objects as go

import numpy as np
import json
import figures


def build_banner(app):
    return html.Div(
        id="banner",
        className="app__header",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H4(
                        "AeroSpec Environmental Quality Monitoring Dashboard",
                        className="app__header__title",
                    ),
                    html.H5("Data Display"),
                ],
                className="app__header__desc",
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button",
                        children="LEARN MORE",
                        n_clicks=0,
                        className="app_button",
                        style={"margin-right": "5px"},
                    ),
                    html.Button(
                        id="settings-button",
                        children="SETTINGS",
                        n_clicks=0,
                        className="app_button",
                        style={"margin-right": "5px"},
                    ),
                    html.Img(
                        id="logo",
                        src=app.get_asset_url("aerospec.png"),
                        className="app__menu__img",
                    ),
                ],
                className="app__header__logo",
                style={"margin-right": "20px"},
            ),
        ],
    )


def build_banner_v2(app):
    return html.Div(
        id="banner",
        className="app__header",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            id="logo",
                            src=app.get_asset_url("aerospec.png"),
                            className="app__menu__img",
                        ),
                        align="start",
                    ),
                    dbc.Col(
                        html.H6("AeroSpec Environmental Quality Monitoring Dashboard"),
                        className="app__header__title",
                    ),
                    dbc.Col(
                        html.Button(
                            id="learn-more-button",
                            children="LEARN MORE",
                            n_clicks=0,
                            className="banner_button",
                        ),
                        align="end",
                    ),
                    dbc.Col(
                        html.Button(
                            id="settings-button",
                            children="SETTINGS",
                            n_clicks=0,
                            className="banner_button",
                        ),
                        align="end",
                    ),
                ],
                no_gutters=True,
            )
        ],
    )


def build_banner_v3(app):
    return html.Div(
        id="banner",
        className="banner-sam",
        children=[
            html.Img(
                id="logo",
                src=app.get_asset_url("aerospec.png"),
                className="app__menu__img",
            ),
            html.H5(
                "AeroSpec Environmental Quality Monitoring Dashboard",
                className="app__header__title",
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button",
                        children="LEARN MORE",
                        n_clicks=0,
                        className="banner_button",
                    ),
                    html.Button(
                        id="settings-button",
                        children="SETTINGS",
                        n_clicks=0,
                        className="banner_button",
                    ),
                ],
            ),
        ],
    )


def generate_learn_button():
    return html.Div(
        id="learn",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
## Welcome!
###### What does this app do?
This is a dashboard for monitoring real-time environmental quality data from AeroSpec sensors. 

Parameters measured include:
* Particulate matter (PM)
* Temperature
* Relative humidity
* Noise

###### How to use this app
On the Overview tab, choose a parameter to view current values and summary statistics observed by all sensors.

On the Sensors tab, choose a sensor to view the time trends and distributions of observed data across different parameters.

Different colors represent the environmental quality; these can be modified by clicking the Settings button.
"""
                            )
                        ),
                    ),
                ],
            )
        ),
    )


def generate_settings_button(data_obj):
    return html.Div(
        id="settings",
        className="modal",
        children=(
            html.Div(
                id="settings-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="settings-close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=[
                            dcc.Markdown(children=("### Settings"),),
                            html.Div(
                                style={"height": "2px", "background-color": "lightgray"}
                            ),
                            html.Div(
                                id="value-setter-panel",
                                children=build_setters_panel(data_obj),
                            ),
                            html.Br(),
                            html.Button(
                                "Update",
                                id="update-settings",
                                className="app_button",
                                n_clicks=0,
                                style={"color": "white"},
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )


def button_callbacks(app):
    @app.callback(
        Output("learn", "style"),
        [
            Input("learn-more-button", "n_clicks"),
            Input("markdown_close", "n_clicks"),
            Input("app-tabs", "value"),
        ],
    )
    def trigger_learn_more(button_click, close_click, tab_switch):
        ctx = dash.callback_context

        if ctx.triggered:
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if prop_id == "learn-more-button":
                return {"display": "block"}
        elif tab_switch == "intro":
            return {"display": "block"}
        else:
            return {"display": "none"}

    @app.callback(
        Output("settings", "style"),
        [Input("settings-button", "n_clicks"), Input("settings-close", "n_clicks"),],
    )
    def trigger_settings(button_click, close_click):
        ctx = dash.callback_context

        if ctx.triggered:
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if prop_id == "settings-button":
                return {"display": "block"}
        return {"display": "none"}



def build_setters_panel(data_obj):

    return dbc.Row(
        [
            dbc.Col(settings_dropdown(data_obj.settings), width=3),
            dbc.Col(build_settings_panel("PM2.5_Std", data_obj.settings), width=9),
        ],
        no_gutters=True,
    )


def build_settings_panel(param, settings):

    panel = [setting_graph(settings), build_setting_header()]

    for i, (var, val, color) in enumerate(settings[param]):
        name = "{} : {}".format(param, var)
        panel.append(build_setting_line(i, var, val, color))
        # panel.append(build_value_setter_line("setting-{}".format(name), name, val,))

    return panel

def get_rgb_ints(color_str):
    return [int(i) for i in color_str.replace('rgba(', '').replace(', {})', '').split(',')]

def build_setting_line(id, param, value, color):

    r,g,b = get_rgb_ints(color)

    return dbc.Row(
        [
            dbc.Col(html.Div(param), width=2),
            dbc.Col(
                daq.NumericInput(
                    id="input-{}".format(id),
                    className="setting-input",
                    value=value,
                    size=50,
                    max=99999,
                ),
                width=2,
            ),
            dbc.Col(html.Div('RGB'), width=2),
            dbc.Col(
                daq.NumericInput(
                    id="input-{}-r".format(id),
                    className="setting-input",
                    value=r,
                    size=50,
                    min=0,
                    max=255,
                ),
                width=2,
            ),
            dbc.Col(
                daq.NumericInput(
                    id="input-{}-g".format(id),
                    className="setting-input",
                    value=g,
                    size=50,
                    min=0,
                    max=255,
                ),
                width=2,
            ),
            dbc.Col(
                daq.NumericInput(
                    id="input-{}-b".format(id),
                    className="setting-input",
                    value=b,
                    size=50,
                    min=0,
                    max=255,
                ),
                width=2,
            ),
        ],
        no_gutters=True,
    )


def build_setting_header():

    return dbc.Row(
        [
            dbc.Col(html.Div("Category"), width=2),
            dbc.Col(html.Div("Threshold"), width=2),
            dbc.Col(html.Div("Color"), width=2),
        ],
        no_gutters=True,
    )


def settings_callbacks(app, settings):
    @app.callback([
        Output("input-0", "value"),
        Output("input-0-r", "value"),
        Output("input-0-g", "value"),
        Output("input-0-b", "value"),
        Output("input-1", "value"),
        Output("input-1-r", "value"),
        Output("input-1-g", "value"),
        Output("input-1-b", "value"),
        Output("input-2", "value"),
        Output("input-2-r", "value"),
        Output("input-2-g", "value"),
        Output("input-2-b", "value"),
        Output("input-3", "value"),
        Output("input-3-r", "value"),
        Output("input-3-g", "value"),
        Output("input-3-b", "value"),
        Output("input-4", "value"),
        Output("input-4-r", "value"),
        Output("input-4-g", "value"),
        Output("input-4-b", "value"),
        Output("settings-bar-chart", "figure"),
        ],
        Input("settings-drop", "value"),

    )
    def trigger_settings_dropdown(param):

        print(param)
        output = []
        i = 0
        for i, (var, val, color) in enumerate(settings[param]):
            r, g, b = get_rgb_ints(color)
            output.append(val)
            output.append(r)
            output.append(g)
            output.append(b)
        while i < 4:
            output.append(" ")
            output.append(" ")
            output.append(" ")
            output.append(" ")
            i += 1

        fig = get_settings_fig(settings, param)
        output.append(fig)

        return output

    # @app.callback(
    #     Output('setting-cache', 'children'),
    #     Input("update-settings", "n_clicks"),
    #     # State("input-0", "value"),
    #     # State("input-0-r", "value"),
    #     # State("input-0-g", "value"),
    #     # State("input-0-b", "value"),
    #     # State("input-1", "value"),
    #     # State("input-1-r", "value"),
    #     # State("input-1-g", "value"),
    #     # State("input-1-b", "value"),
    #     # State("input-2", "value"),
    #     # State("input-2-r", "value"),
    #     # State("input-2-g", "value"),
    #     # State("input-2-b", "value"),
    #     # State("input-3", "value"),
    #     # State("input-3-r", "value"),
    #     # State("input-3-g", "value"),
    #     # State("input-3-b", "value"),
    #     # State("input-4", "value"),
    #     # State("input-4-r", "value"),
    #     # State("input-4-g", "value"),
    #     # State("input-4-b", "value")
    # )
    # def trigger_settings_update(button_click
    #                             # i_0, r_0, g_0, b_0,
    #                             # i_1, r_1, g_1, b_1,
    #                             # i_2, r_2, g_2, b_2,
    #                             # i_3, r_3, g_3, b_3,
    #                             # i_4, r_4, g_4, b_4,
    #                             ):
    #
    #     return json.dumps(settings)






def settings_dropdown(settings):
    return html.Div(
        children=[
            html.P(),  # this creates a new paragraph
            html.H6("Parameter"),
            dcc.Dropdown(
                id="settings-drop",
                options=[{"label": param, "value": param} for param in settings.keys()],
                value="PM2.5_Std",
                multi=False,
            ),
        ],
    )

def get_settings_fig(settings, param):
    mean_thresholds = figures.get_var_thresholds(settings, param, True)
    real_thresholds = [cat[1] for cat in settings[param]]
    colors = figures.get_var_colors(settings, param, 1)
    bar_widths = np.diff(mean_thresholds)
    bar_widths = np.append(bar_widths, list(np.diff(mean_thresholds))[-1])
    categories = [cat[0] for cat in settings[param]]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=mean_thresholds,
            y=[1 for _ in settings[param]],
            width=bar_widths,
            # orientation='h',
            marker_color=colors,
            hoverinfo="skip",
        )
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

    fig.update_xaxes(
        tickvals=np.cumsum(bar_widths) - bar_widths / 2,
        ticktext=["%s<br>%d" % (l, w) for l, w in zip(categories, real_thresholds)],
        tickfont_color="white",
    )

    # Change the bar mode
    margin = 30
    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=margin, r=margin, t=margin, b=80),
        height=130,
    )
    return fig

def setting_graph(settings, param="PM2.5_Std"):

    fig = get_settings_fig(settings, param="PM2.5_Std")
    return dbc.Row(
        dbc.Col(
            dcc.Graph(
                id="settings-bar-chart", figure=fig, config={"displayModeBar": False}
            )
        ),
        no_gutters=True,
    )
