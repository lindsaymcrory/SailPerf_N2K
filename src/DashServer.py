import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from SensorPipeline import sensorpipeline
import time


# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Button labels
buttons = ["ACTISENSE", "CAN HAT", "SIMULATOR", "FILE UPLOAD"]

def create_button(label):
    default_color = "red" if label == "SIMULATOR" else "gray"
    return dbc.Button(
        label,
        id=f"btn-{label.replace(' ', '_')}",
        style={"backgroundColor": default_color, "color": "white", "width": "100%"},
        className="text-center"
    )

def changed_source(msg):
    """ """
    print("self.changed_source: ",msg)
    return

# Define the layout
app.layout = dbc.Container(
    
    style={"marginTop": "20px", "width": "50%", "fontSize": "60%"},
   
    children=[
        html.H5("S A I L P E R F  -  N2K", style={"backgroundColor": "gray", "color": "white", "padding": "10px", "textAlign": "center"}),
        html.Br(),
        dbc.Row(
            className="mb-3",
            children=[
                dbc.Col(create_button("ACTISENSE"), width=3),
                dbc.Col(create_button("CAN HAT"), width=3),
                dbc.Col(create_button("SIMULATOR"), width=3),
                dbc.Col(create_button("FILE UPLOAD"), width=3),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.H3("SOURCES", className="text-center mt-3")
            )
        ),   dcc.Interval(
        id="interval-component",
        interval=1000,  # 1000ms = 1 second
        n_intervals=0  # Starts at 0 and increments every second
    ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Label("BoatSpeed:"),
                        html.Span("0", id="boat-speed", style={"fontWeight": "bold", "marginLeft": "10px"})
                    ],
                    className="text-center mt-3"
                )
            )
        ),
               dbc.Row(
                   
            dbc.Col(
                html.Div(
                    [
                        html.Label("BoatSpeed2:"),
                        html.Span("0", id="live-label", style={"fontWeight": "bold", "marginLeft": "10px"}),
                        html.Br(),
                        html.Label("Something Else:"),
                        html.Span("0", id="live-label2", style={"fontWeight": "bold", "marginLeft": "10px"}),
                        html.Div(id='live-update-text')
                    ],
                    className="text-center mt-3"
                )
                
            )
        )
    ]
)


@app.callback(
    [Output(f"btn-{label.replace(' ', '_')}", "style") for label in buttons],
    [Input(f"btn-{label.replace(' ', '_')}", "n_clicks") for label in buttons],
    prevent_initial_call=True
)
def update_button_color(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [{"backgroundColor": "gray", "color": "white", "width": "100%"}] * len(buttons)

    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # ✅ This is the new line: Calls the Python function when a button is pressed
    changed_source(clicked_id)

    return [
        {"backgroundColor": "red", "color": "white", "width": "100%"} if f"btn-{label.replace(' ', '_')}" == clicked_id 
        else {"backgroundColor": "gray", "color": "white", "width": "100%"} 
        for label in buttons
    ]


@app.callback(
    Output("boat-speed", "children"),
    Input("boat-speed", "id"),
    prevent_initial_call=False
)
def update_boat_speed(_):
    time.sleep(1)  # Simulate real-time update delay
    sensorpipeline.sensors['boat_speed_nm'] = .5
    print("update_boat_speed(_)")
    return f"{sensorpipeline.sensors['boat_speed_nm']:.2f} knots"

counter = 0 


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    #lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    # sensorpipeline.sensors['']
    # html.Span('Longitude: {0:.2f}'.format(num), style=style),
    num = 66.6
    style = {'padding': '5px', 'fontSize': '16px'}
    retval = []
    for sensor_label in sensorpipeline.sensors:
        val = sensorpipeline.sensors[sensor_label]
        val = str(val)
        #txt =  html.Span( + "'"+ sensor_label + ": " + str(val) + "'",style=style)
        txt = html.Span(f"{sensor_label}: {val}", style=style)
        retval.append(txt)
        retval.append(html.Br())

    return retval




# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
