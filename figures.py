import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np
import pandas as pd
import os


def empty_fig():
    return go.Figure()


def get_quality_color(settings, var, val, transparency):

    for (qual, threshold, color) in settings[var]:
        # qual being like "Good" or "Moderate"
        if val < threshold:
            return color.format(transparency)
    # if above largest threshold, return the color of the last
    return settings[var][-1][2].format(transparency)


def get_var_thresholds(settings, var, mean=False):
    dt = [0]
    for (qual, threshold, color) in settings[var]:
        dt.append(threshold)
    if mean:
        mean_list = []
        for x, y in zip(dt[0::], dt[1::]):
            mean_list.append((x + y) / 2)
        return mean_list
    else:
        return dt


def get_var_colors(settings, var, transparency):
    dt = []
    for (qual, threshold, color) in settings[var]:
        dt.append(color.format(transparency))
    return dt


def get_quality_status(settings, var, val):
    for (qual, threshold, color) in settings[var]:
        if val < threshold:
            return qual
    return settings[var][-1][0]


def overview_histogram(data_obj, param):

    if not param:
        param = "PM2.5_Std"

    data_zip = []
    for id in data_obj.data.keys():
        df = data_obj.data[id]["data"]
        val = df[param][0]
        data_zip.append([id, val])

    figure_data = []
    for (id, val) in sorted(data_zip, key=lambda x: x[1], reverse=True):
        transparency = 1.0
        color = get_quality_color(data_obj.settings, param, val, transparency)

        figure_data.append(
            go.Bar(
                name=id,
                y=["PM"],
                x=[1],
                hoverlabel={"bgcolor": "white", "bordercolor": "black"},
                hovertemplate="{}".format(val),
                orientation="h",
                marker=dict(
                    color=color, line=dict(color="rgba(58, 71, 80, 1.0)", width=1)
                ),
            )
        )

    fig = go.Figure(data=figure_data)
    fig.update_layout(
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

    # Change the bar mode
    margin = 0
    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=margin, r=margin, t=margin, b=margin),
        height=83,
    )
    return fig


def get_pie(data_obj, param, title=None):

    data_zip = []
    for id in data_obj.data.keys():
        df = data_obj.data[id]["data"]
        val = df[param][0]
        data_zip.append([id, val])

    labels, colors = [], []
    for (id, val) in sorted(data_zip, key=lambda x: x[1], reverse=True):
        labels.append(id)
        colors.append(get_quality_color(data_obj.settings, param, val, 1.0))

    return go.Pie(
        labels=labels, values=[1 for _ in labels], marker_colors=colors, title=title,
    )


def overview_status(data_obj, param):
    if not param:
        param = "PM2.5_Std"

    data_zip = []
    for id in data_obj.data.keys():
        df = data_obj.data[id]["data"]
        val = df[param][0]
        data_zip.append(val)

    mean_value = np.mean(data_zip)
    mean_status = get_quality_status(data_obj.settings, param, mean_value)
    if param == "Noise (dB)" or any(pmvar in param for pmvar in ["Dp", "PM"]):
        warnings = sum(i > data_obj.settings[param][1][1] for i in data_zip)
    elif (param == "P(hPa)") or (param == "RH(%)") or (param == "Temp(C)"):
        warnings = sum(i > data_obj.settings[param][1][1] for i in data_zip) + sum(
            i < data_obj.settings[param][0][1] for i in data_zip
        )
    return f"{mean_status}, {warnings} warning(s)"


def overview_donut(data_obj, param):

    if not param:
        param = "PM2.5_Std"

    fig = go.Figure(get_pie(data_obj, param, title=param))
    fig.update_traces(hole=0.4, textinfo="none", hoverinfo="label")
    fig.update(layout_showlegend=False)  # layout_title_text='{}'.format(param),
    fig.update_layout(margin={"l": 20, "r": 20, "t": 20, "b": 20})

    return fig


def overview_donuts_all_param(data_obj):

    params = ["PM2.5_Std", "P(hPa)", "RH(%)", "Temp(C)"]

    # use domains for pie charts
    specs = [
        [{"type": "domain"}, {"type": "domain"}],
        [{"type": "domain"}, {"type": "domain"}],
    ]
    fig = make_subplots(
        rows=2, cols=2, specs=specs, horizontal_spacing=0.05, vertical_spacing=0.05
    )

    for p, (i, j) in zip(params, [(1, 1), (1, 2), (2, 1), (2, 2)]):
        fig.add_trace(get_pie(data_obj, p, title=p), i, j)

    fig.update_traces(hole=0.4, textinfo="none", hoverinfo="label")
    fig.update(layout_showlegend=False)  # layout_title_text='Key Parameters',
    fig.update_layout(margin={"l": 20, "r": 20, "t": 20, "b": 20})

    return fig


def map_figure(data_obj, sensors_list, image, param):

    if image is None:
        image = os.path.join(".", "assets", "cool_floorplan.jpg")  # "floorplan.png")

    img_width = 890
    img_height = 890
    sensor_size = 30

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[0, img_width], y=[0, img_height], mode="markers", marker_opacity=0
        )
    )

    fig.add_layout_image(
        x=0,
        sizex=img_width,
        y=img_height,
        sizey=img_height,
        sizing="stretch",
        xref="x",
        yref="y",
        opacity=1.0,
        source=image,
    )

    fig.update_layout(
        width=img_width,
        height=img_height,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    for i, id in enumerate(sensors_list):
        df = data_obj.data[id]["data"]
        sensor_value = df[param][0]

        np.random.seed(1 + i)
        xrand = np.random.randint(0, img_width - sensor_size)
        yrand = np.random.randint(0, img_height - sensor_size)

        fig.add_shape(
            type="circle",
            fillcolor=get_quality_color(data_obj.settings, param, sensor_value, 1),
            line_color=get_quality_color(data_obj.settings, param, sensor_value, 1),
            x0=xrand,
            y0=yrand,
            x1=xrand + sensor_size,
            y1=yrand + sensor_size,
        )
        fig.add_trace(
            go.Scatter(
                x=[xrand + sensor_size],
                y=[yrand + sensor_size],
                text="{}<br>Current value: {}".format(id, round(sensor_value)),
                opacity=0,
                hoverinfo="text",
            )
        )

    fig.update_layout(showlegend=False, hoverlabel_bgcolor="white")
    return fig


def line_figure(data_obj, sensors, show_timeselector):

    fig = make_subplots(
        rows=4, cols=2, shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.1
    )

    for sensor in sensors:
        # TODO: update from placeholder data to noise data once available
        line_row = 1
        df = data_obj.data[sensor]["data"]
        for param in ["PM2.5_Std", "RH(%)", "RH(%)", "Temp(C)"]:
            fig.add_trace(
                go.Scattergl(
                    x=df.index, y=df[param], line=dict(color="black"), name=sensor,
                ),
                row=line_row,
                col=2,
            )
            line_row += 1

    hist_row = 1
    for var in ["PM2.5_Std", "Noise (dB)", "RH(%)", "Temp(C)"]:
        # TODO: update from placeholder data to noise data once available
        if var == "Noise (dB)":
            var = "RH(%)"

        data_list = []
        for sensor in sensors:
            vals = data_obj.data[sensor]["data"][var].values
            data_list.append(vals)

        counts, bins = np.histogram(
            np.concatenate(data_list), bins=get_var_thresholds(data_obj.settings, var)
        )
        fig.add_trace(
            go.Bar(
                x=counts,
                y=get_var_thresholds(data_obj.settings, var, True),
                width=np.diff(get_var_thresholds(data_obj.settings, var)),
                orientation="h",
                marker_color=get_var_colors(data_obj.settings, var, 1),
                hoverinfo="text",
            ),
            row=hist_row,
            col=1,
        )
        hist_row += 1

    fig["layout"].update(
        barmode="stack",
        hovermode="closest",
        plot_bgcolor="white",
        showlegend=False,
        height=1000,
        xaxis2=dict(
            domain=[0.3, 1.0],
            rangeslider=dict(visible=False),
            type="date",
            showticklabels=True,
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
        xaxis4=dict(domain=[0.3, 1.0], showticklabels=True),
        xaxis6=dict(domain=[0.3, 1.0], showticklabels=True),
        xaxis8=dict(domain=[0.3, 1.0], showticklabels=True),
        xaxis1=dict(autorange="reversed", domain=[0.0, 0.25], showticklabels=True),
        xaxis3=dict(autorange="reversed", domain=[0.0, 0.25], showticklabels=True),
        xaxis5=dict(autorange="reversed", domain=[0.0, 0.25], showticklabels=True),
        xaxis7=dict(autorange="reversed", domain=[0.0, 0.25], showticklabels=True),
        shapes=get_color_shape_list(data_obj, df.index),
        xaxis7_title="Number of observations",
    )

    if show_timeselector:
        fig["layout"].update(
            xaxis2=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1,
                                label="Month",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=14, label="Week", step="day", stepmode="backward"
                            ),
                            dict(count=1, label="Day", step="day", stepmode="backward"),
                            dict(
                                count=1, label="Hour", step="hour", stepmode="backward"
                            ),
                        ]
                    )
                ),
            )
        )

    return fig


def get_color_shape_list(data, x, transparency=0.2):
    shapes_list = []
    for param, (x_str, y_str) in zip(
        ["PM2.5_Std", "Noise (dB)", "RH(%)", "Temp(C)"],
        [("x2", "y2"), ("x4", "y4"), ("x6", "y6"), ("x8", "y8")],
    ):
        lower_threshold = 0
        for (_, upper_threshold, color) in data.settings[param]:

            shapes_list.append(
                dict(
                    fillcolor=color.format(transparency),
                    line={"width": 0},
                    type="rect",
                    xref=x_str,
                    yref=y_str,
                    y0=lower_threshold,
                    y1=upper_threshold,
                    x0=x.min(),
                    x1=x.max(),
                )
            )
            lower_threshold = upper_threshold
    return shapes_list


def display_year_heatmap(z, data_obj, year: int = None, fig=None, row: int = None):
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
    # [0,1,2,3,4,5,6,0,1,2,3,4,5,6,???] (ticktext in xaxis dict translates this to weekdays
    weekdays_in_year = [i.weekday() for i in dates_in_year]
    # [1,1,1,1,1,1,1,2,2,2,2,2,2,2,???] name is self-explanatory
    weeknumber_of_dates = [
        int(i.strftime("%W"))
        if not (int(i.strftime("%W")) == 1 and i.month == 12)
        else 0
        for i in dates_in_year
    ]

    # list of strings like ???2018-01-25??? for each date.
    # Used in data trace to make good hovertext.
    text = [str(i) for i in dates_in_year]

    color_scale = []
    lower = 0
    max_val = data_obj.settings["PM2.5_Std"][-1][1]
    for (_, val, color) in data_obj.settings["PM2.5_Std"]:
        color_scale.append([lower / max_val, color.format(1.0)])
        color_scale.append([val / max_val, color.format(1.0)])
        lower = val

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
            colorscale=color_scale,
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


def display_years(data_obj):
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
        display_year_heatmap(z, data_obj, year=year, fig=fig, row=i)
        fig.update_layout(height=250 * len(years))

    return fig
