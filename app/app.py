import banner
import layouts
import figures

import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import load



class DataObj:
    def __init__(self, input_data_path):

        self.data = load.load_folder(input_data_path)
        self.params = self.get_params()

    def get_params(self):
        """
        Return a list of parameters

        Notes
        -----
        Uses the first data frame columns to determine parameters.
        """
        params = []
        df = self.data[0]
        for i in df.columns:
            if i in [
                'Dp > 0.3',
                'Dp > 0.5',
                'Dp > 1.0',
                'Dp > 2.5',
                'Dp > 5.0',
                'Dp > 10.0',
                'PM1_Std',
                'PM2.5_Std',
                'PM10_Std',
                'PM1_Env',
                'PM2.5_Env',
                'PM10_Env',
                'Temp(C)',
                'RH( %)',
                'P(hPa)',
                'Alti(m)',
                'Noise (dB)'
            ]:
                params.append(i)
        return params

data_obj = DataObj('.\data\Clean UW')
df = data_obj.data[0]

fig1 = figures.map_figure(df)
fig2 = figures.line_figure(df)
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
        return layouts.build_sensors_tab(fig2)
    elif tab_switch == 'overview':
        # lazy loading data here for now because get_data_table might slow main dashboard
        # print(table_data_view)
        # if table_data_view is None:
        list_view_table = tables.get_data_table(data)
        return layouts.build_overview_tab(data_obj, fig1, list_view_table)
    else:
        return layouts.build_overview_tab(data_obj, fig1)


@app.callback(
    Output('map-figure', 'figure'),
    [Input('param-drop', 'value')])
def update_figure(params):
    """
    """
    fig = figures.map_figure(data_obj, params = params)
    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)