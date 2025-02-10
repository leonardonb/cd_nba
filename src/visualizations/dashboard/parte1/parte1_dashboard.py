import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Estatísticas do time Brooklyn Nets referentes da temporada 2023-24 e 2024-25", style={'textAlign': 'center'}),

    # Gráficos de Barras
    html.Div([
        html.H2("Gráficos de Barras"),
        html.Img(src="/assets/rf8_bar_stats_especificas RF06.jpg", style={'width': '400px'}),
        html.Img(src="/assets/rf8_barras_empilhado_vitorias_derrotas.jpg", style={'width': '400px'}),
        html.Hr()
    ]),

    # Gráficos de Linha
    html.Div([
        html.H2("Gráficos de Linha"),
        html.Img(src="/assets/rf8_linha_seq_2023-24.jpg", style={'width': '400px'}),
        html.Img(src="/assets/rf8_linha_seq_2024-25.jpg", style={'width': '400px'}),
        html.Hr()
    ]),

    # Gráficos de Pizza
    html.Div([
        html.H2("Gráficos de Pizza"),
        html.Img(src="/assets/rf8_pizza_vitorias_derrotas_2023-24.jpg", style={'width': '400px'}),
        html.Img(src="/assets/rf8_pizza_vitorias_derrotas_2024-25.jpg", style={'width': '400px'}),
        html.Hr()
    ]),

    # Gráficos de Radar
    html.Div([
        html.H2("Gráficos de Radar"),
        html.Img(src="/assets/rf8_radar_casa_media.jpg", style={'width': '400px'}),
        html.Img(src="/assets/rf8_radar_fora_media.jpg", style={'width': '400px'}),
        html.Hr()
    ]),

    # Gráficos de Dispersão (Scatter)
    html.Div([
        html.H2("Gráficos de Dispersão"),
        html.Img(src="/assets/rf8_scatter_detalhes_jogos RF07.jpg", style={'width': '400px'}),
        html.Img(src="/assets/rf8_scatter_media_pontos.jpg", style={'width': '400px'}),
        html.Hr()
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

# Rode o comando a seguir para gerar a pagina html referente ao dashboard da parte 1
# python src/visualizations/dashboard/parte1/parte1_dashboard.py