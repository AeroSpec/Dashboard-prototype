
import dash_core_components as dcc
import dash_html_components as html


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
                        className="app_button"
                    ),
                    html.Img(id="logo",
                             src=app.get_asset_url('aerospec.png'),
                             width="40",
                             className="app__menu__img"),
                ],
                className="app__header__logo",
            ),
        ],
    )


def generate_learn_button():
    return html.Div(
        id="markdown",
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
