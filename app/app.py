import banner
import layouts
import load
import tables
import figures
import os

import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import load


data = list()
for dirpath, dirnames, files in os.walk('data/Clean UW'):
    # print(f'Found directory: {dirpath}')
    for file_name in files:
        data.append(pd.read_csv(dirpath+'/'+file_name))
        # print(file_name)

df = data[0]

fig1 = figures.map_figure(df)
fig2 = figures.line_figure(df)
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


@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        # lazy loading data here for now because get_data_table might slow main dashboard
        # print(table_data_view)
        # if table_data_view is None:
        table_list_view = tables.get_data_table(data)
        return layouts.build_tab(fig1, table_list_view)

    elif tab_switch == "tab2":
        return layouts.build_tab(fig2)

if __name__ == '__main__':
    app.run_server(debug=True, port=8053)