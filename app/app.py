import banner
import layouts
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__)



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


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)