
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



def notifications():
    return html.Div(id="notifications",
                    className="dashboard-component",
                    children=[notifications_title()])


def notifications_title():
    return dbc.Row(dbc.Col([html.H6("Notifications"), html.Hr()], width=12), no_gutters=True)


def generate_notifications(data_obj, app):
    # dbc.Toast(
    #     [html.P("The sensors have gone haywire!", className="mb-0")],
    #     id="auto-toast",
    #     header="Alert",
    #     icon="primary",
    #     duration=4000,
    #     dismissable=True,
    #     )


    def callbacks(app):
        @app.callback(
            Output("auto-toast", "is_open"), [Input("auto-toast-toggle", "n_clicks")]
        )
        def open_toast(n):
            return True