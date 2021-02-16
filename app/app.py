import banner
import layouts
import figures
from tables import ListViewTablesObj

import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import load
import os
import pandas as pd


class DataObj:
    def __init__(self, input_data_path):

        self.data = list()
        for dirpath, dirnames, files in os.walk('data/Clean UW'):
            for file_name in files:
                self.data.append(pd.read_csv(dirpath + '/' + file_name))

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

## Table object -> stores selected table data
table_object = ListViewTablesObj()
table_object.set_data(data_obj.data)

## Adding sensor for just 2 object values
## TODO - Remove and add values selected by user in list view
table_object.add_sensor_to_selected_list('Sensor 11')
table_object.add_sensor_to_selected_list('Sensor 12')
table_object.add_sensor_to_selected_list('Sensor 13')
table_object.add_sensor_to_selected_list('Sensor 14')
table_object.add_sensor_to_selected_list('Sensor 15')

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
        return layouts.build_overview_tab(data_obj, fig1, pd.DataFrame.transpose(pd.DataFrame.from_dict(table_object.get_selected_sensors_grouped_data())))
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