import plotly.graph_objects as go
from plotly.subplots import make_subplots


def map_figure(data, params =[]):

    print(params)
    # Create figure
    fig = go.Figure()

    # Constants
    img_width = 1200
    img_height = 1200
    scale_factor = 0.5

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source="https://wcs.smartdraw.com/office-floor-plan/examples/office-floor-plan.png?bn=15100111771")
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  fillcolor="#f70000",
                  line_color="#f70000",
                  x0=300, y0=300, x1=320, y1=320,
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  fillcolor="#fff980",
                  line_color="#fff980",
                  x0=100, y0=100, x1=120, y1=120,
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  fillcolor="#137506",
                  line_color="#137506",
                  x0=120, y0=440, x1=140, y1=460,
                  )

    return fig

def line_figure(df):
    x = df.index
    # TODO: add secondary_y axis
    fig = make_subplots(rows=4, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1)
    # TODO: change to different variables by figure
    fig.add_trace(go.Scatter(x=x, y=df['PM2.5_Std'], line=dict(color="#000000"), name=''),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=x, y=df['PM2.5_Std'], line=dict(color="#000000"), name=''), # Use atmospheric pressure as a substitute for noise data
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
            fixedrange=True, title = "PM2.5_Std"
        ),
        yaxis2=dict(
            fixedrange=True, title = "Noise"
        ),
        yaxis3=dict(
            fixedrange=True, title = "RH%"
        ),
        yaxis4=dict(
            fixedrange=True, title = "Temp(C)"
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