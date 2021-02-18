import banner
import layouts

import figures
import data

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go





data_obj = data.DataObj(os.path.join(".", "data", "Clean UW"))
id1 = list(data_obj.data.keys())[0]
df = data_obj.data[id1]['data']

fig1 = figures.map_figure(df)
fig2 = figures.line_figure(data_obj, 1)







app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    id="outer layout",
    children=[
        banner.build_banner(app),
        html.Div(
            id="app-container",
            children=[
                layouts.build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        banner.generate_learn_button(),
        dcc.Interval(
            id="interval-component",
            interval=1000,  # 1 second
            n_intervals=0,
        ),
    ],
)

@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}


@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "sensors":
        return layouts.build_sensors_tab(data_obj, fig2)
    elif tab_switch == 'overview':
        return layouts.build_overview_tab(data_obj, fig1)
    else:
        return layouts.build_overview_tab(data_obj, fig1)





@app.callback(
    Output('map-figure', 'figure'),
    [Input('param-drop', 'value')])
def update_map(params):
    """
    """
    fig = figures.map_figure(data_obj, params = params)
    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    output=Output("line-graph", "figure"),
    inputs=[Input("interval-component", "n_intervals"),
            Input("sensor-drop", "value")],
)
def update_line_on_interval(counter, params):
    data_obj.increment_data()
    return figures.line_figure(data_obj, params = params)



if __name__ == '__main__':
    app.run_server(debug=True, port=8051)