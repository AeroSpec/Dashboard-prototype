import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import datetime



def date_picker(data_obj):

    start = datetime.date(2020, 1, 1)
    today = datetime.date.today()

    # Date Picker
    return html.Div([
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=start,
            max_date_allowed=today,
            initial_visible_month=today,#.strftime("%B"),
            start_date=today - datetime.timedelta(6),
            end_date=today,
        ),
        html.Div(id='output-date-picker')
    ],
        style={'margin': 5}
    )

def callbacks(app):
    @app.callback(Output('output-date-picker', 'children'),
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date')])
    def update_output(start_date, end_date):
        return html.Div("{} {}".format(start_date, end_date))


def thermometer(df, name='Sensor ID'):

    color = 'red'

    return html.Div([
        daq.Thermometer(
            id='thermometer',
            label=name,
            labelPosition='bottom',
            value=35,
            color=color,
            min=0,
            max=40,
            showCurrentValue=True,
            units="C",
            height=100,
            width=20,
            style={
                'margin-bottom': '5%'
            }
        )
    ])