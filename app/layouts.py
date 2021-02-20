
import dash_core_components as dcc
import dash_html_components as html

import figures

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

def build_sensors_tab(data_obj, fig):
    return html.Div(
        id="sensors_tab",
        className="tabs",
        children=[
                dcc.Dropdown(id='sensor-drop'
                                 , options=[
                                    {'label': f'Sensor {i}', 'value': i} for i in range(1, data_obj.sensors_count + 1)],
                                 value=[],
                                 multi=True
                 ),
                dcc.Graph(
                     id='line-graph',
                     figure=fig
                 ),
                ]
            )

def build_overview_tab(data_obj, fig):
    return html.Div(
        id="overview_tab",
        className="tabs",
        children=[

            html.P(),  # this creates a new paragraph
            html.H5('Parameter'),
            dcc.Dropdown(id='param-drop'
                         , options=[
                            {'label': i, 'value': i} for i in data_obj.params],
                         value=[],
                         multi=True
                         ),
            dcc.Graph(
                        id='map-figure',
                    ),

                ]
            )



