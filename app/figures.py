import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np
import pandas as pd

def get_quality_color(data, var, val, transparency):
    settings_var = data.settings[var]
    if var == "Noise (dB)" or any(pmvar in var for pmvar in ["Dp", "PM"]):
        if val >= 0 & val <= settings_var['Good']:
            return f"rgba(67, 176, 72, {transparency})"
        elif val > settings_var['Good'] & val <= settings_var['Moderate']:
            return f"rgba(255, 250, 117, {transparency})"
        elif val > settings_var['Moderate'] & val <= settings_var['Unhealthy']:
            return f"rgba(230, 32, 32, {transparency})"
        elif val > settings_var['Unhealthy'] & val <= settings_var['Very Unhealthy']:
           return f"rgba(149, 69, 163, {transparency})"
        elif val >= settings_var['Very Unhealthy']:
           return f"rgba(107, 30, 30, {transparency})"
    if var == "P(hPa)" or var == "RH(%)" or var == "Temp(C)":
        if val <= settings_var['Low']:
            return f"rgba(230, 32, 32, {transparency})"
        elif (val > settings_var['Low']) & (val <= settings_var['Normal']):
            return f"rgba(67, 176, 72, {transparency})"
        elif val >= settings_var['Normal']:
            return f"rgba(230, 32, 32, {transparency})"

def map_figure(data, params):
    # get all values for that param across all sensors
    # df = data.append_sensor_data(subset_vars = params)
    df = pd.DataFrame()
    for sensor in range(1, data.sensors_count + 1):
        id2 = list(data.data.keys())[int(sensor)-1]
        sensor_dt = data.data[id2]['data'][params].to_frame()
        sensor_dt['Sensor'] = sensor
        df = df.append(sensor_dt)

    # Create figure
    fig = go.Figure()

    # Constants
    img_width = 890
    img_height = 890
    sensor_size = 30

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width], y=[0, img_height], mode="markers", marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(visible=False,)

    fig.update_yaxes(visible=False,)

    # Add image
    fig.add_layout_image(
        x=0,
        sizex=img_width,
        y=img_height,
        sizey=img_height,
        xref="x",
        yref="y",
        opacity=1.0,
        # TODO: change to use png file in repo
        source="https://wcs.smartdraw.com/office-floor-plan/examples/office-floor-plan.png?bn=15100111771",
    )

    # Configure other layout
    fig.update_layout(
        width=img_width,
        height=img_height,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        plot_bgcolor="rgba(0,0,0,0)",
    )

    for i in range(1, data.sensors_count + 1):
        np.random.seed(1+i)
        xrand = np.random.randint(0, img_width - sensor_size)
        yrand = np.random.randint(0, img_height - sensor_size)
        sensor_value = df[(df['Sensor'] == i) & (df.index == max(df.index))][params].item()
        fig.add_shape(type="circle",
                  fillcolor=get_quality_color(data, params, sensor_value, 1),
                  line_color=get_quality_color(data, params, sensor_value, 1),
                  x0=xrand, y0=yrand, x1=xrand+sensor_size, y1=yrand+sensor_size,
                  )
        fig.add_trace(
          go.Scatter(
              x=[xrand+sensor_size], y=[yrand+sensor_size],
              text=f'Sensor {i}<br>Current value: {sensor_value}',
              opacity=0,
              hoverinfo="text"
          )
        )

    fig.update_layout(
        showlegend=False,
        hoverlabel_bgcolor='#ffffff'
    )
    return fig


def line_figure(data, params=[]):
    df = data.append_sensor_data(sensors=params)
    x = df.index

    fig = make_subplots(
        rows=4,
        cols=2,
        shared_xaxes=True,
        shared_yaxes=True,
        vertical_spacing=0.1,
        horizontal_spacing=0.02,
    )

    for param in params:
        # Time series line graphs
        fig.add_trace(
            go.Scatter(
                x=x,
                y=df[df["Sensor"] == int(param)]["PM2.5_Std"],
                line=dict(color="#000000"),
                name=f"Sensor {param}",
            ),
            row=1,
            col=2,
        )
        # TODO: update from placeholder data to noise data once available
        fig.add_trace(
            go.Scatter(
                x=x,
                y=df[df["Sensor"] == int(param)]["P(hPa)"] / 10000,
                line=dict(color="#000000"),
                name=f"Sensor {param}",
            ),
            row=2,
            col=2,
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df[df["Sensor"] == int(param)]["RH(%)"],
                line=dict(color="#000000"),
                name=f"Sensor {param}",
            ),
            row=3,
            col=2,
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df[df["Sensor"] == int(param)]["Temp(C)"],
                line=dict(color="#000000"),
                name=f"Sensor {param}",
            ),
            row=4,
            col=2,
        )

        # Histograms
        fig.add_trace(
            go.Histogram(
                y=df[df["Sensor"] == int(param)]["PM2.5_Std"],
                name=f"Sensor {param}",
                marker_color="#000000",
            ),
            row=1,
            col=1,
        )
        # TODO: update from placeholder data to noise data once available
        fig.add_trace(
            go.Histogram(
                y=df[df["Sensor"] == int(param)]["P(hPa)"] / 10000,
                name=f"Sensor {param}",
                marker_color="#000000",
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Histogram(
                y=df[df["Sensor"] == int(param)]["RH(%)"],
                name=f"Sensor {param}",
                marker_color="#000000",
            ),
            row=3,
            col=1,
        )

        fig.add_trace(
            go.Histogram(
                y=df[df["Sensor"] == int(param)]["Temp(C)"],
                name=f"Sensor {param}",
                marker_color="#000000",
            ),
            row=4,
            col=1,
        )
    
    fig["layout"].update(
        barmode="stack",
        hovermode="closest",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=1000,
        xaxis2=dict(
            domain=[0.3, 1.0],
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="Month", step="month", stepmode="backward"),
                        dict(count=14, label="Week", step="day", stepmode="backward"),
                        dict(count=1, label="Day", step="day", stepmode="backward"),
                        dict(count=1, label="Hour", step="hour", stepmode="backward"),
                    ]
                )
            ),
            rangeslider=dict(visible=False),
            type="date",
        ),
        yaxis2=dict(fixedrange=True, title="", side="right", showticklabels=True),
        yaxis4=dict(fixedrange=True, title="", side="right", showticklabels=True),
        yaxis6=dict(fixedrange=True, title="", side="right", showticklabels=True),
        yaxis8=dict(fixedrange=True, title="", side="right", showticklabels=True),
        yaxis1=dict(
            fixedrange=True,
            title="Air quality (PM2.5)",
            side="left",
            showticklabels=False,
        ),
        yaxis3=dict(
            fixedrange=True, title="Noise (dB)", side="left", showticklabels=False
        ),
        yaxis5=dict(
            fixedrange=True,
            title="Relative Humidity (%)",
            side="left",
            showticklabels=False,
        ),
        yaxis7=dict(
            fixedrange=True, title="Temperature (C)", side="left", showticklabels=False
        ),
        xaxis4=dict(domain=[0.3, 1.0]),
        xaxis6=dict(domain=[0.3, 1.0]),
        xaxis8=dict(domain=[0.3, 1.0]),
        xaxis1=dict(autorange="reversed", domain=[0.0, 0.25]),
        xaxis3=dict(autorange="reversed", domain=[0.0, 0.25]),
        xaxis5=dict(autorange="reversed", domain=[0.0, 0.25]),
        xaxis7=dict(autorange="reversed", domain=[0.0, 0.25]),
        shapes=[
            dict(
                fillcolor='rgba(67, 176, 72, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x2", yref="y2",
                y0=0,
                y1=data.settings['PM2.5_Std']['Good'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(255, 250, 117, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x2", yref="y2",
                y0=data.settings['PM2.5_Std']['Good'],
                y1=data.settings['PM2.5_Std']['Moderate'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(230, 32, 32, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x2", yref="y2",
                y0=data.settings['PM2.5_Std']['Moderate'],
                y1=data.settings['PM2.5_Std']['Unhealthy'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(149, 69, 163, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x2", yref="y2",
                y0=data.settings['PM2.5_Std']['Unhealthy'],
                y1=data.settings['PM2.5_Std']['Very Unhealthy'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(107, 30, 30, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x2", yref="y2",
                y0=data.settings['PM2.5_Std']['Very Unhealthy'],
                y1=data.settings['PM2.5_Std']['Hazardous'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(67, 176, 72, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x4", yref="y4",
                y0=0,
                y1=data.settings["Noise (dB)"]['Good'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(255, 250, 117, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x4", yref="y4",
                y0=data.settings['Noise (dB)']['Good'],
                y1=data.settings['Noise (dB)']['Moderate'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(230, 32, 32, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x4", yref="y4",
                y0=data.settings['Noise (dB)']['Moderate'],
                y1=data.settings['Noise (dB)']['Unhealthy'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(149, 69, 163, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x4", yref="y4",
                y0=data.settings['Noise (dB)']['Unhealthy'],
                y1=data.settings['Noise (dB)']['Very Unhealthy'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor='rgba(107, 30, 30, 0.2)',
                line={"width": 0},
                type="rect",
                xref="x4", yref="y4",
                y0=data.settings['Noise (dB)']['Very Unhealthy'],
                y1=data.settings['Noise (dB)']['Hazardous'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor="rgba(230, 32, 32, 0.2)",
                line={"width": 0},
                type="rect",
                xref="x6", yref="y6",
                y0=0,
                y1=data.settings['RH(%)']['Low'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor="rgba(67, 176, 72, 0.2)",
                line={"width": 0},
                type="rect",
                xref="x6", yref="y6",
                y0=data.settings['RH(%)']['Low'],
                y1=data.settings['RH(%)']['Normal'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor="rgba(230, 32, 32, 0.2)",
                line={"width": 0},
                type="rect",
                xref="x6", yref="y6",
                y0=data.settings['RH(%)']['Normal'],
                y1=data.settings['RH(%)']['High'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor="rgba(230, 32, 32, 0.2)",
                line={"width": 0},
                type="rect",
                xref="x8", yref="y8",
                y0=0,
                y1=data.settings['Temp(C)']['Low'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor="rgba(67, 176, 72, 0.2)",
                line={"width": 0},
                type="rect",
                xref="x8", yref="y8",
                y0=data.settings['Temp(C)']['Low'],
                y1=data.settings['Temp(C)']['Normal'],
                x0=x.min(),
                x1=x.max()
            ),
            dict(
                fillcolor="rgba(230, 32, 32, 0.2)",
                line={"width": 0},
                type="rect",
                xref="x8", yref="y8",
                y0=data.settings['Temp(C)']['Normal'],
                y1=data.settings['Temp(C)']['High'],
                x0=x.min(),
                x1=x.max()
            )
        ]
    )

    return fig


def display_year_heatmap(z, year: int = None, fig=None, row: int = None):
    if year is None:
        year = datetime.datetime.now().year

    data = np.ones(365) * np.nan
    data[: len(z)] = z

    d1 = datetime.date(year, 1, 1)
    d2 = datetime.date(year, 12, 31)

    delta = d2 - d1

    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_positions = (np.cumsum(month_days) - 15) / 7

    # list with datetimes for each day a year
    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days + 1)]
    # [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
    weekdays_in_year = [i.weekday() for i in dates_in_year]
    # [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
    weeknumber_of_dates = [
        int(i.strftime("%W"))
        if not (int(i.strftime("%W")) == 1 and i.month == 12)
        else 0
        for i in dates_in_year
    ]

    # list of strings like ‘2018-01-25’ for each date.
    # Used in data trace to make good hovertext.
    text = [str(i) for i in dates_in_year]

    data = [
        go.Heatmap(
            x=weeknumber_of_dates,
            y=weekdays_in_year,
            z=data,
            text=text,
            hoverinfo="text",
            xgap=3,  # this
            ygap=3,  # and this is used to make the grid-like apperance
            showscale=False,
            colorscale=[
                [0, "green"],
                [0.60, "green"],
                [0.60, "yellow"],
                [0.80, "yellow"],
                [0.80, "orange"],
                [0.90, "orange"],
                [0.90, "red"],
                [0.95, "red"],
                [0.95, "magenta"],
                [1.0, "magenta"],
            ],
        )
    ]

    # month_lines
    kwargs = dict(mode="lines", line=dict(color="#9e9e9e", width=1), hoverinfo="skip")
    for date, dow, wkn in zip(dates_in_year, weekdays_in_year, weeknumber_of_dates):
        if date.day == 1:
            data += [go.Scatter(x=[wkn - 0.5, wkn - 0.5], y=[dow - 0.5, 6.5], **kwargs)]
            if dow:
                data += [
                    go.Scatter(
                        x=[wkn - 0.5, wkn + 0.5], y=[dow - 0.5, dow - 0.5], **kwargs
                    ),
                    go.Scatter(x=[wkn + 0.5, wkn + 0.5], y=[dow - 0.5, -0.5], **kwargs),
                ]

    layout = go.Layout(
        title=None,
        height=250,
        yaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            tickmode="array",
            ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            autorange="reversed",
        ),
        xaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            tickmode="array",
            ticktext=month_names,
            tickvals=month_positions,
        ),
        font={"size": 10, "color": "black"},
        plot_bgcolor=("#fff"),
        margin=dict(t=40),
        showlegend=False,
    )

    if fig is None:
        fig = go.Figure(data=data, layout=layout)
    else:
        fig.add_traces(data, rows=[(row + 1)] * len(data), cols=[1] * len(data))
        fig.update_layout(layout)
        fig.update_xaxes(layout["xaxis"])
        fig.update_yaxes(layout["yaxis"])

    return fig


def display_years():
    years = (2020, 2021)

    z_2020 = np.random.random(365)

    # generate random data for days up until today, then nan
    z_2021 = np.zeros(365) * np.nan  # list of nan
    now = datetime.datetime.now()
    d1 = datetime.date(now.year, 1, 1)
    delta = now.date() - d1
    z_2021[: delta.days] = np.random.random(delta.days)

    fig = make_subplots(rows=len(years), cols=1, subplot_titles=years)
    for i, (year, z) in enumerate(zip(years, [z_2020, z_2021])):
        display_year_heatmap(z, year=year, fig=fig, row=i)
        fig.update_layout(height=250 * len(years))

    return fig
