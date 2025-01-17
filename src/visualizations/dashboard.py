import dash
from dash import dcc, html

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure={"data": [{"x": [1, 2, 3], "y": [4, 1, 2]}]})
])

app.run_server(debug=True)
