import plotly.graph_objects as go
from plotly.subplots import make_subplots


def map_figure(df):


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
    y = df['PM2.5_Std']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x, y=y,
                             mode='lines',
                             name='lines'),
                             secondary_y=True,
             )
    return fig