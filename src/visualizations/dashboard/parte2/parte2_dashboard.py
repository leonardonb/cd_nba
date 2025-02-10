import dash
from dash import html

player_names = ["Cam Thomas", "Cameron Johnson", "D'Angelo Russell"]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Estatísticas dos Jogadores Selecionados", style={'textAlign': 'center'}),

    *[
        html.Div([
            html.H2(player),

            html.Img(src=f"/assets/{player}_distribuicao_pontos.jpg", style={'width': '400px'}),
            html.Img(src=f"/assets/{player}_distribuicao_rebotes.jpg", style={'width': '400px'}),
            html.Img(src=f"/assets/{player}_distribuicao_assistências.jpg", style={'width': '400px'}),
            html.Img(src=f"/assets/{player}_boxplot.jpg", style={'width': '400px'}),

            html.Hr()
        ])
        for player in player_names
    ]
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

# Rode o comando a seguir para gerar a pagina html referente ao dashboard da parte 2
# python src/visualizations/dashboard/parte2/parte2_dashboard.py