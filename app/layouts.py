import dash_core_components as dcc
import dash_html_components as html
import dash_table


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
                    )
                ],
            )
        ],
    )

def build_tab(fig, table_data = list()):
    if (len(table_data) == 0):
        return html.Div(dcc.Graph(
                            id='Graph1',
                            figure=fig
                        ),
                )
    else:
        return html.Div(children=[
            html.Div([
                html.H1(children='Map view'),

                html.Div(children='''
                                    A map view of all sensor data.
                                '''),
                dcc.Graph(
                    id='Graph1',
                    figure=fig
                ),
            ]),
            html.Div([
                html.H1(children='List view'),

                html.Div(children='''
                                    A list view of all sensor data.
                                '''),
                dash_table.DataTable(
                    id='list_table',
                    columns=[{"name": i.upper(), "id": i} for i in table_data.columns],
                    data=table_data.to_dict('records'),
                ),
            ])
        ]
        )
