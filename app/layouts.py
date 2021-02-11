

import dash_core_components as dcc
import dash_html_components as html


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Overview-tab",
                        label="Overview",
                        value="tab1",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Sensors",
                        value="tab2",
                    ),
                ],
            )
        ],
    )

def build_tab(fig):
    return html.Div(dcc.Graph(
                        id='Graph1',
                        figure=fig
                    ),
            )
