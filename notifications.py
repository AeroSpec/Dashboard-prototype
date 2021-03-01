
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import figures


def notifications(data_obj):
    return html.Div(id="notifications",
                    className="dashboard-component",
                    children=[notifications_title(),
                              html.Div(generate_notifications(data_obj))])


def notifications_title():
    return dbc.Row(dbc.Col([html.H6("Notifications"), html.Hr()], width=12), no_gutters=True)


def generate_notifications(data_obj, param=None):
    if not param:
        param = "PM2.5_Std"

    threshold_category = data_obj.settings[param][1]  # category

    notify_list = []
    for id in data_obj.data.keys():
        df = data_obj.data[id]["data"]
        val = df[param][0] # current value

        if val > threshold_category[1]:
            #color = figures.get_quality_color(data_obj, param, val, 1.0)
            cat = figures.get_quality_status(data_obj, param, val)
            notify_list.append((id, param, cat))

    toast_list = []
    for id, param, cat in notify_list:
        toast_list.append(get_toast_notification(id, param, cat))

    return toast_list

def get_toast_notification(id, param, category):

    # icon options :  "primary", "secondary", "success", "warning", "danger", "info", "light", "dark"
    if category == "Very Unhealthy":
        icon = "warning"
    elif category == "Hazardous":
        icon = "danger"
    else:
        icon = "info"

    return dbc.Toast(
        [html.P("{}: {} reading is currently  '{}'.".format(id, param, category))],
        id="auto-toast-{}".format(id),
        header=icon.capitalize(),
        icon=icon,
        #duration=4000,
        dismissable=True,
        )