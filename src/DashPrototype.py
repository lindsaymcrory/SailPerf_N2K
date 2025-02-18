import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container(
    style={"marginTop": "50px", "width": "80%"},  # Centered container
    children=[
        html.H5("S A I L P E R F  -  N2K", style={"backgroundColor": "gray", "color": "white", "padding": "10px", "textAlign": "center"}),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Data Source Status", className="text-center fw-bold bg-light text-dark"),
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Actisense", className="text-center bg-secondary text-white"),
                                        dbc.CardBody(
                                            [
                                                html.P("High-performance marine electronics for NMEA2000.", className="text-white"),
                                                dbc.Button("Configure", id="btn-actisense", color="secondary", className="mt-2 text-white"),
                                            ],
                                            className="text-center"
                                        ),
                                    ],
                                    className="shadow p-3 mb-4 bg-light text-dark rounded"
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("PI-CAN", className="text-center bg-secondary text-white"),
                                        dbc.CardBody(
                                            [
                                                html.P("Raspberry Pi CAN interface for marine applications.", className="text-white"),
                                                dbc.Button("Configure", id="btn-pi-can", color="secondary", className="mt-2 text-white"),
                                            ],
                                            className="text-center"
                                        ),
                                    ],
                                    className="shadow p-3 mb-4 bg-light text-dark rounded"
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Simulator", className="text-center bg-secondary text-white"),
                                        dbc.CardBody(
                                            [
                                                html.P("Software-based simulation for NMEA2000 networks.", className="text-white"),
                                                dbc.Button("Configure", id="btn-simulator", color="secondary", className="mt-2 text-white"),
                                            ],
                                            className="text-center"
                                        ),
                                    ],
                                    className="shadow p-3 mb-4 bg-light text-dark rounded"
                                ),
                                width=4,
                            ),
                        ],
                        className="justify-content-center"
                    ),
                    className="p-4",
                ),
            ],
            className="shadow-lg p-4 bg-light text-dark rounded"
        ),
    ]
)

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)