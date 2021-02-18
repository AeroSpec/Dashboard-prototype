import plotly.graph_objects as go
from plotly.subplots import make_subplots


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

def line_figure(data, params):
    id2 = list(data.data.keys())[int(params)-1]
    df = data.data[id2]['data']
    x = df.index

    fig = make_subplots(rows=4, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1)
    
    fig.add_trace(go.Scatter(x=x, y=df['PM2.5_Std'], line=dict(color="#000000"), name=''),
                  row=1, col=1)
# TODO: update from placeholder data to noise data once available
    fig.add_trace(go.Scatter(x=x, y=df['P(hPa)']/10000, line=dict(color="#000000"), name=''),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=x, y=df['RH(%)'], line=dict(color="#000000"), name=''),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=x, y=df['Temp(C)'], line=dict(color="#000000"), name=''),
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
            fixedrange=True, title = "Air quality (PM2.5)", side = "right"
        ),
        yaxis2=dict(
            fixedrange=True, title = "Noise (dB)", side = "right"
        ),
        yaxis3=dict(
            fixedrange=True, title = "Relative Humidity (%)", side = "right"
        ),
        yaxis4=dict(
            fixedrange=True, title = "Temperature (C)", side = "right"
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
                y1=max(200,max(df['PM2.5_Std'])),
                x0=min(x),
                x1=max(x)
            )
        ]
    )
    return fig