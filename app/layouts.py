
import pandas as pd
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

def build_sensors_tab(fig):
    return html.Div(dcc.Graph(
                         id='Graph1',
                         figure=fig
                     ),
             )

def build_overview_tab(data_obj, fig, list_view_table = pd.DataFrame()):
    list_view_columns = list()
    list_view_data = list()
    if len(list_view_table) != 0:
        list_view_table = list_view_table.reset_index()
        print(list_view_table)
        list_view_columns = [{"name": i.upper(), "id": i} for i in list_view_table.columns]
        list_view_data = list_view_table.to_dict('records')

    return html.Div(children=[
                html.Div(
                    id="tabs",
                    className="tabs",
                    children=[
                        html.P(),  # this creates a new paragraph
                        html.H3('Parameter'),
                        dcc.Dropdown(id='param-drop'
                                     , options=[
                                {'label': i, 'value': i} for i in data_obj.params],
                                     value=[],
                                     multi=True
                                     ),
                        dcc.Graph(
                            id='map-figure',
                        ),
                    ]),
                html.Div([
                    html.H1(children='List view'),

                    html.Div(children='''
                                        A list view of all sensor data.
                                    '''),
                    dash_table.DataTable(
                        id='list_table',
                        columns=list_view_columns,
                        data=list_view_data,
                    ),
                ])
            ])



