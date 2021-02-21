import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq


def build_banner(app):
    return html.Div(
        id="banner",
        className="app__header",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H4("AeroSpec Dashboard", className="app__header__title"),
                    html.H5("Data Display"),
                ],
                className="app__header__desc",
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0,
                        className="app_button",
                        style={'margin-right': '5px'}
                    ),
                    html.Button(
                        id="settings-button", children="SETTINGS", n_clicks=0,
                        className="app_button",
                        style={'margin-right': '5px'}
                    ),
                    html.Img(id="logo",
                             src=app.get_asset_url('aerospec.png'),
                             width="40",
                             className="app__menu__img"),
                ],
                className="app__header__logo",
                style={'margin-right': '20px'}
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
"""###### What does this app do?
This is a dashboard for monitoring real-time data from AeroSpec sensors.
###### Notes
* This is a bullet
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
                        children=[dcc.Markdown(
                            children=("### Settings"),
                            ),
                              html.Br(),
                              html.Div(id="value-setter-panel", children=build_setters_panel(data_obj)),
                              html.Br(),
                              html.Button("Update",
                                          id="update-settings",
                                          className="app_button",
                                          n_clicks=0,
                                          style={'color': 'white'})
                        ],
                              ),
                            ],
                            ),
                        ),
                    )

def button_callbacks(app):
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


# input_1 = daq.NumericInput(
#     id="input-1", className="setting-input", size=200, max=9999999
# )
# input_2 = daq.NumericInput(
#     id="input-2", className="setting-input", size=200, max=9999999
# )

# def register_callbacks(app):
#     @app.callback(
#         output=[
#             Output("value-setter-panel", "children"),
#             Output("input-1", "value"),
#             Output("input-2", "value"),
#         ],
#         inputs=[Input("metric-select-dropdown", "value")],
#         state=[State("value-setter-store", "data")],
#     )




def build_setters_panel(data_obj):
    panel = [build_value_setter_line(
                "settings-panel-header",
                "Setting",
                "Current Value",
                #"Set New Value",
            )]
    print(data_obj.settings)
    for setting in data_obj.settings.keys():
        for var in data_obj.settings[setting].keys():
            name = '{} : {}'.format(setting, var)
            val = data_obj.settings[setting][var]
            panel.append(build_value_setter_line(
                "setting-{}".format(name),
                name,
                val,
            ))
    return panel


def build_value_setter_line(line_num, label, current_value):#, new_val_input):
    return html.Div(
        #id=line_num,
        children=[
            html.Label(label, className="four columns"),
            html.Label(current_value, className="four columns"),
            #html.Div(new_val_input, className="four columns"),
        ],
        className="settings-row",
    )
