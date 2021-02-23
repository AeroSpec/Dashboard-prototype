import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html



def pvi_component(data_obj, param):
    return html.Div(
        className="dashboard-component",
        children=[
            dcc.Markdown(children=("##### Status"), ),
            html.Div(
                id="pvi-panel",
                children=param_val_indicator(data_obj, param),
            )])

def param_val_indicator(data_obj, param):
    panel = [
        html.Div(html.H5(param), className="pvi-row")
    ]

    for id in data_obj.data.keys():
        df = data_obj.data[id]["data"]
        color = "#f70000" # red
        val = 777
        panel.append(param_val_indicator_line(id, color, val))

    return panel

def param_val_indicator_line(label, color, current_value):
    return html.Div(
        children=[
            html.Label(label, className="columns"),
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
