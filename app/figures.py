import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np


def map_figure(data, params =[]):

    print(params)
    # Create figure
    fig = go.Figure()

    # Constants
    img_width = 890
    img_height = 890

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width],
            y=[0, img_height],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
    )

    fig.update_yaxes(
        visible=False,
    )

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
        source="https://wcs.smartdraw.com/office-floor-plan/examples/office-floor-plan.png?bn=15100111771"
    )

    # Configure other layout
    fig.update_layout(
        width=img_width,
        height=img_height,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  fillcolor="#f70000",
                  line_color="#f70000",
                  x0=500, y0=490, x1=530, y1=520,
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  fillcolor="#fff980",
                  line_color="#fff980",
                  x0=130, y0=140, x1=160, y1=170,
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  fillcolor="#137506",
                  line_color="#137506",
                  x0=180, y0=620, x1=210, y1=650,
                  )

    return fig

def line_figure(df):
    x = df.index


    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1)
    # TODO: change to different variables by figure
    fig.add_trace(go.Scatter(x=x, y=df['PM2.5_Std'], line=dict(color="#000000"), name=''),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=x, y=df['PM2.5_Std'], line=dict(color="#000000"), name=''),
                  # Use atmospheric pressure as a substitute for noise data
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=x, y=df['PM2.5_Std'], line=dict(color="#000000"), name=''),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=x, y=df['PM2.5_Std'], line=dict(color="#000000"), name=''),
                  row=4, col=1)

    fig['layout'].update(
        hovermode="closest",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=1000,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="Month",
                         step="month",
                         stepmode="backward"),
                    dict(count=14,
                         label="Week",
                         step="day",
                         stepmode="backward"),
                    dict(count=1,
                         label="Day",
                         step="day",
                         stepmode="backward"),
                    dict(count=1,
                         label="Hour",
                         step="hour",
                         stepmode="backward"),
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date"
        ),
        yaxis=dict(
            fixedrange=True, title="PM2.5_Std", side="right"
        ),
        yaxis2=dict(
            fixedrange=True, title="Noise", side="right"
        ),
        yaxis3=dict(
            fixedrange=True, title="RH%", side="right"
        ),
        yaxis4=dict(
            fixedrange=True, title="Temp(C)", side="right"
        ),
        shapes=[
            dict(
                fillcolor="rgba(67, 176, 72, 0.2)",
                line={"width": 0},
                type="rect",
                y0=0,
                y1=50,
                x0=min(x),
                x1=max(x)
            ),
            dict(
                fillcolor="rgba(255, 250, 117, 0.2)",
                line={"width": 0},
                type="rect",
                y0=50,
                y1=100,
                x0=min(x),
                x1=max(x)
            ),
            dict(
                fillcolor="rgba(230, 32, 32, 0.2)",
                line={"width": 0},
                type="rect",
                y0=100,
                y1=200,
                x0=min(x),
                x1=max(x)
            ),
            dict(
                fillcolor="rgba(149, 69, 163, 0.2)",
                line={"width": 0},
                type="rect",
                y0=200,
                y1=max(200, max(df['PM2.5_Std'])),
                x0=min(x),
                x1=max(x)
            )
        ]
    )
    return fig


def display_year_heatmap(z,
                         year: int = None,
                         fig=None,
                         row: int = None):
    if year is None:
        year = datetime.datetime.now().year

    data = np.ones(365) * np.nan
    data[:len(z)] = z

    d1 = datetime.date(year, 1, 1)
    d2 = datetime.date(year, 12, 31)

    delta = d2 - d1

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_positions = (np.cumsum(month_days) - 15) / 7

    # list with datetimes for each day a year
    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days + 1)]
    # [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
    weekdays_in_year = [i.weekday() for i in dates_in_year]
    # [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
    weeknumber_of_dates = [int(i.strftime("%W")) if not (int(i.strftime("%W")) == 1 and i.month == 12) else 0
                           for i in dates_in_year]

    # list of strings like ‘2018-01-25’ for each date.
    # Used in data trace to make good hovertext.
    text = [str(i) for i in dates_in_year]

    data = [
        go.Heatmap(
            x=weeknumber_of_dates,
            y=weekdays_in_year,
            z=data,
            text=text,
            hoverinfo='text',
            xgap=3,  # this
            ygap=3,  # and this is used to make the grid-like apperance
            showscale=False,
            colorscale=[[0, "green"],
                        [0.60, "green"],
                        [0.60, "yellow"],
                        [0.80, "yellow"],
                        [0.80, "orange"],
                        [0.90, "orange"],
                        [0.90, "red"],
                        [0.95, "red"],
                        [0.95, "magenta"],
                        [1.0, "magenta"]]
        )
    ]

    # month_lines
    kwargs = dict(
        mode='lines',
        line=dict(
            color='#9e9e9e',
            width=1
        ),
        hoverinfo='skip'

    )
    for date, dow, wkn in zip(dates_in_year,
                              weekdays_in_year,
                              weeknumber_of_dates):
        if date.day == 1:
            data += [
                go.Scatter(
                    x=[wkn - .5, wkn - .5],
                    y=[dow - .5, 6.5],
                    **kwargs
                )
            ]
            if dow:
                data += [
                    go.Scatter(
                        x=[wkn - .5, wkn + .5],
                        y=[dow - .5, dow - .5],
                        **kwargs
                    ),
                    go.Scatter(
                        x=[wkn + .5, wkn + .5],
                        y=[dow - .5, -.5],
                        **kwargs
                    )
                ]

    layout = go.Layout(
        title=None,
        height=250,
        yaxis=dict(
            showline=False, showgrid=False, zeroline=False,
            tickmode='array',
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            autorange="reversed"
        ),
        xaxis=dict(
            showline=False, showgrid=False, zeroline=False,
            tickmode='array',
            ticktext=month_names,
            tickvals=month_positions
        ),
        font={'size': 10, 'color': 'black'},
        plot_bgcolor=('#fff'),
        margin=dict(t=40),
        showlegend=False
    )

    if fig is None:
        fig = go.Figure(data=data, layout=layout)
    else:
        fig.add_traces(data, rows=[(row + 1)] * len(data), cols=[1] * len(data))
        fig.update_layout(layout)
        fig.update_xaxes(layout['xaxis'])
        fig.update_yaxes(layout['yaxis'])

    return fig


def display_years():
    years = (2020, 2021)

    z_2020 = np.random.random(365)

    # generate random data for days up until today, then nan
    z_2021 = np.zeros(365) * np.nan  # list of nan
    now = datetime.datetime.now()
    d1 = datetime.date(now.year, 1, 1)
    delta = now.date() - d1
    z_2021[:delta.days] = np.random.random(delta.days)

    fig = make_subplots(rows=len(years), cols=1, subplot_titles=years)
    for i, (year, z) in enumerate(zip(years, [z_2020, z_2021])):
        display_year_heatmap(z, year=year, fig=fig, row=i)
        fig.update_layout(height=250 * len(years))

    return fig
