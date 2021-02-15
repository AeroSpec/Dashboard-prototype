
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

def build_overview_tab(data_obj, fig):
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            html.P(),  # this creates a new paragraph
            html.H5('Parameter'),
            dcc.Dropdown(id='param-drop'
                         , options=[
                            {'label': i, 'value': i} for i in data_obj.params],
                         value=['US'],
                         multi=True
                         ),
            dcc.Graph(
                        id='Graph1',
                        figure=fig
                    ),

                ]
            )

#
# @app.callback(Output('province-drop', 'options'),
#               [Input('country-drop', 'value')])
# def set_province_options(country):
#     if len(country) > 0:
#         countries = country
#         return [{'label': i, 'value': i} for i in sorted(set(df['province'].loc[df['country'].isin(countries)]))]
#
#     else:
#         countries = []
#         return [{'label': i, 'value': i} for i in sorted(set(df['province'].loc[df['country'].isin(countries)]))]


def build_tab(fig):
    return html.Div(dcc.Graph(
                         id='Graph1',
                         figure=fig
                     ),
             )
