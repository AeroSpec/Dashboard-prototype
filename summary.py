import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

import figures


def pvi_component(data_obj, param):
    return html.Div(
        className="dashboard-component",
        children=[
            dcc.Markdown(children=("##### Status"),),
            html.Div(id="pvi-panel", children=param_val_indicator(data_obj, param),),
        ],
    )


def param_val_indicator(data_obj, param):
    panel = [html.Div(html.H5(param), className="pvi-row")]

    param = "PM2.5_Std"

    data_zip = []
    for id in data_obj.data.keys():
        df = data_obj.data[id]["data"]
        val = df[param][0]
        data_zip.append([id, val])

    for (id, val) in sorted(data_zip, key=lambda x: x[1], reverse=True):
        transparency = 1.0

        color = figures.get_quality_color(data_obj, param, val, transparency)
        panel.append(param_val_indicator_line(id, color, val))

    return panel


def param_val_indicator_line(label, color, current_value):
    return html.Div(
        children=[
            html.Label(label, className="columns1"),
            indicator(color),
            html.Label(current_value, className="columns"),
        ],
        className="pvi-row",
    )


def indicator(color):
    return daq.Indicator(
        className="columns",
        value=True,
        color=color,
        size=12,
        width=12,
        # height=12, # uncomment for square
    )
