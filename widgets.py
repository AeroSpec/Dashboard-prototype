import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import figures
import datetime
import numpy as np

def get_daily_osha_noise_exposure_progress(data_obj):
    return html.Div(
        id="osha_progress",
        className="dashboard-component",
        children=progress_bars(data_obj))

def progress_bars(data_obj):

    i = 10
    accumulated_values = []
    for id in data_obj.data.keys():
        df = data_obj.data[id]["data"]
        val = df["PM2.5_Std"][0]  # current value

    r = np.random.lognormal(size=len(data_obj.data.keys()))
    j = 100*r/max(r)
    accumulated_values = j

    bars_list = [progress_bar_title()]
    for v in accumulated_values:
        color = figures.get_quality_color(data_obj, "PM2.5_Std", v*4, 1.0)
        bars_list.append(dbc.Row(dbc.Col(
            dbc.Progress(value=v, color=color,#"info",
                         style={"height": "10px", "width": "500px"}, className="mb-4"), width=12), no_gutters=True))

    return bars_list

def progress_bar_title():
    return dbc.Row(dbc.Col([html.H6("Daily OSHA Noise Exposure [%]"), html.Hr()], width=12), no_gutters=True)


def date_picker(data_obj):

    start = datetime.date(2020, 1, 1)
    today = datetime.date.today()

    # Date Picker
    return html.Div(
        [
            dcc.DatePickerRange(
                id="date-picker",
                min_date_allowed=start,
                max_date_allowed=today,
                initial_visible_month=today,  # .strftime("%B"),
                start_date=today - datetime.timedelta(6),
                end_date=today,
            ),
            html.Div(id="output-date-picker"),
        ],
        style={"margin": 5},
    )


def callbacks(app):
    @app.callback(
        Output("output-date-picker", "children"),
        [Input("date-picker", "start_date"), Input("date-picker", "end_date")],
    )
    def update_output(start_date, end_date):
        return html.Div("{} {}".format(start_date, end_date))


def thermometer(df, name="Sensor ID"):

    color = "red"

    return html.Div(
        [
            daq.Thermometer(
                id="thermometer",
                label=name,
                labelPosition="bottom",
                value=35,
                color=color,
                min=0,
                max=40,
                showCurrentValue=True,
                units="C",
                height=100,
                width=20,
                style={"margin-bottom": "5%"},
            )
        ]
    )
