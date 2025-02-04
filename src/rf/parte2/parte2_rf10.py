import matplotlib
from matplotlib import pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
from nba_api.stats.endpoints import playercareerstats, playergamelog
import pandas as pd
import os
import statistics

def fetch_career_stats(player_id):
    """
    Busca os dados de carreira de um jogador e retorna os totais de pontos, rebotes e assistências.

    Args:
        player_id (int): ID do jogador na NBA API.

    Returns:
        pd.Series: Totais de carreira do jogador.
    """
    try:
        career_stats = playercareerstats.PlayerCareerStats(
            player_id=player_id, timeout=30
        ).get_data_frames()[0]

        career_totals = career_stats[career_stats['LEAGUE_ID'] == '00']
        career_totals = career_totals.rename(columns={
            'PTS': 'Pontos',
            'REB': 'Rebotes',
            'AST': 'Assistências',
            'MIN': 'Minutos'
        })

        totals = career_totals[['Pontos', 'Rebotes', 'Assistências', 'Minutos', 'GP']].sum()
        totals['Média de Pontos'] = round(totals['Pontos'] / totals['GP'], 2)
        totals['Média de Rebotes'] = round(totals['Rebotes'] / totals['GP'], 2)
        totals['Média de Assistências'] = round(totals['Assistências'] / totals['GP'], 2)
        return totals

    except Exception as e:
        print(f"Erro ao buscar dados de carreira do jogador {player_id}: {e}")
        return pd.Series({'Pontos': 0, 'Rebotes': 0, 'Assistências': 0, 'Minutos': 0, 'GP': 0,
                          'Média de Pontos': 0, 'Média de Rebotes': 0, 'Média de Assistências': 0})

def fetch_season_stats(player_id):
    """
    Busca os dados da temporada atual de um jogador.

    Args:
        player_id (int): ID do jogador na NBA API.

    Returns:
        pd.Series: Totais da temporada do jogador.
    """
    try:
        season_stats = playergamelog.PlayerGameLog(
            player_id=player_id, season="2024-25", timeout=30
        ).get_data_frames()[0]

        season_stats = season_stats.rename(columns={
            'PTS': 'Pontos',
            'REB': 'Rebotes',
            'AST': 'Assistências',
            'MIN': 'Minutos'
        })

        season_totals = season_stats[['Pontos', 'Rebotes', 'Assistências', 'Minutos']].sum()
        season_totals['GP'] = len(season_stats)
        season_totals['Média de Pontos'] = round(season_totals['Pontos'] / season_totals['GP'], 2)
        season_totals['Média de Rebotes'] = round(season_totals['Rebotes'] / season_totals['GP'], 2)
        season_totals['Média de Assistências'] = round(season_totals['Assistências'] / season_totals['GP'], 2)
        return season_totals

    except Exception as e:
        print(f"Erro ao buscar dados da temporada do jogador {player_id}: {e}")
        return pd.Series({'Pontos': 0, 'Rebotes': 0, 'Assistências': 0, 'Minutos': 0, 'GP': 0,
                          'Média de Pontos': 0, 'Média de Rebotes': 0, 'Média de Assistências': 0})
    
def fetch_player_game_data(player_id):
    """
    Busca dados de todos os jogos de um jogador na temporada atual.

    Args:
        player_id (int): ID do jogador na NBA API.

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos jogos.
    """
    try:
        player_log = playergamelog.PlayerGameLog(player_id=player_id, season="2024-25").get_data_frames()[0]

        player_log = player_log[player_log['MATCHUP'].str.contains("BKN")]

        player_log = player_log.rename(columns={
            'PTS': 'Pontos',
            'REB': 'Rebotes',
            'AST': 'Assistências'
        })

        columns = [
            'Pontos', 'Rebotes', 'Assistências'
        ]
        player_log = player_log[columns]

        return player_log
    except Exception as e:
        print(f"Erro ao buscar dados do jogador: {e}")
        return pd.DataFrame()

def comparar_estatisticas(players, output_dir, html_dir, img_dir):
    """
    Compara as estatísticas da carreira e da temporada atual dos jogadores.

    Args:
        players (list): Lista de dicionários com nomes e IDs dos jogadores.
        output_dir (str): Diretório para salvar os resultados em CSV.
        html_dir (str): Diretório para salvar os resultados em HTML.
        img_dir (str): Diretório para salvar os gráficos.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for player in players:
        player_name = player['PLAYER']
        player_id = player['PLAYER_ID']

        try:
            print(f"Buscando dados do jogador: {player_name}, ID: {player_id}")
            career_stats = fetch_career_stats(player_id)
            season_stats = fetch_season_stats(player_id)

            comparison = pd.DataFrame({
                'Estatística': ['Total de Jogos', 'Média de Pontos', 'Média de Rebotes', 'Média de Assistências', 'Minutos em Quadra'],
                'Temporada Atual': [season_stats['GP'], season_stats['Média de Pontos'], season_stats['Média de Rebotes'], season_stats['Média de Assistências'], season_stats['Minutos']],
                'Carreira': [career_stats['GP'], career_stats['Média de Pontos'], career_stats['Média de Rebotes'], career_stats['Média de Assistências'], career_stats['Minutos']]
            })

            # Salvar como CSV
            csv_path = os.path.join(output_dir, f"{player_name}_comparacao.csv")
            comparison.to_csv(csv_path, index=False)
            print(f"Tabela CSV salva em: {csv_path}")

            # Salvar como HTML
            html_path = os.path.join(html_dir, f"{player_name}_comparacao.html")
            comparison.to_html(html_path, index=False)
            print(f"Tabela HTML salva em: {html_path}")

            # Salvar gráficos
            dados = fetch_player_game_data(player_id)
            salvar_graficos_distribuicao(player_name, dados, img_dir, html_dir)
            salvar_graficos_boxplot(player_name, dados, img_dir)

        except Exception as e:
            print(f"Erro ao processar dados do jogador {player_name}: {e}")

    print('Processamento do RF10 concluído.')


def salvar_graficos_distribuicao(player_name, dados, img_dir, html_dir):
    """
    Salva gráficos de distribuição para os dados de um jogador.

    Args:
        player_name (str): Nome do jogador.
        dados (pd.DataFrame): DataFrame com os dados dos jogos do jogador.
        img_dir (str): Diretório para salvar os gráficos como imagens.
        html_dir (str): Diretório para salvar os gráficos como HTML.
    """
    def plot_distribuicao_plotly(dados, nome, xlabel):
        """
        Cria e salva um gráfico de distribuição usando Plotly.
        """
        media = statistics.mean(dados)
        mediana = statistics.median(dados)
        moda = max(set(dados), key=dados.count) if dados else None

        fig = ff.create_distplot([dados], [xlabel], show_hist=False, show_rug=False)

        fig.add_vline(x=media, line=dict(color="blue", dash="dash"))
        fig.add_vline(x=mediana, line=dict(color="green", dash="dash"))
        if moda is not None:
            fig.add_vline(x=moda, line=dict(color="orange", dash="dash"))

        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(color='blue', size=8),
            name=f"Média: {media:.2f}"
        ))

        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(color='green', size=8),
            name=f"Mediana: {mediana:.2f}"
        ))

        if moda is not None:
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(color='orange', size=8),
                name=f"Moda: {moda:.2f}"
            ))

        fig.update_layout(
            title=f"Distribuição de {nome} - {player_name}",
            xaxis_title=xlabel,
            yaxis_title="Densidade",
            legend_title="Estatísticas",
        )

        # Salvar gráfico como .jpg
        img_path = os.path.join(img_dir, f"{player_name}_distribuicao_{nome.lower()}.jpg")
        img_path = os.path.normpath(img_path)  # Normaliza para o formato correto do sistema operacional
        fig.write_image(img_path, format='jpg', engine='orca')
        print(f"Gráfico de distribuição salvo em: {img_path}")

        # Salvar gráfico como HTML
        html_path = os.path.join(html_dir, f"{player_name}_distribuicao_{nome.lower()}.html")
        fig.write_html(html_path)
        print(f"Gráfico de distribuição salvo em: {html_path}")

    for coluna, nome, xlabel in zip(
        ['Pontos', 'Rebotes', 'Assistências'],
        ['Pontos', 'Rebotes', 'Assistências'],
        ['Pontos por Jogo', 'Rebotes por Jogo', 'Assistências por Jogo']
    ):
        if coluna in dados:
            dados_filtrados = dados[coluna].dropna().tolist()
            if dados_filtrados:
                plot_distribuicao_plotly(dados_filtrados, nome, xlabel)


def salvar_graficos_boxplot(player_name, dados, img_dir):
    """
    Salva gráficos de box plot comparando temporada e carreira de um jogador.

    Args:
        player_name (str): Nome do jogador.
        dados (pd.DataFrame): DataFrame com os dados dos jogos do jogador.
        img_dir (str): Diretório para salvar os gráficos.
    """
    def plot_boxplot(dados):
        """
        Gráfico de box plot comparando temporada atual e carreira.
        """
        plt.figure(figsize=(10, 6))
        
        pontos = dados['Pontos'].dropna().tolist()
        rebotes = dados['Rebotes'].dropna().tolist()
        assistencias = dados['Assistências'].dropna().tolist()

        box = plt.boxplot([pontos, rebotes, assistencias], patch_artist=True, medianprops=dict(color="red"), widths=0.7)

        colors = ['lightblue', 'lightgreen', 'lightcoral']
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)

        legend_texts = [
            f"Pontos: Min: {min(pontos):.1f}, Q1: {statistics.quantiles(pontos, n=4)[0]:.1f}, Mediana: {statistics.median(pontos):.1f}, Q3: {statistics.quantiles(pontos, n=4)[2]:.1f}, Max: {max(pontos):.1f}",
            f"Rebotes: Min: {min(rebotes):.1f}, Q1: {statistics.quantiles(rebotes, n=4)[0]:.1f}, Mediana: {statistics.median(rebotes):.1f}, Q3: {statistics.quantiles(rebotes, n=4)[2]:.1f}, Max: {max(rebotes):.1f}",
            f"Assistências: Min: {min(assistencias):.1f}, Q1: {statistics.quantiles(assistencias, n=4)[0]:.1f}, Mediana: {statistics.median(assistencias):.1f}, Q3: {statistics.quantiles(assistencias, n=4)[2]:.1f}, Max: {max(assistencias):.1f}"
        ]

        plt.legend(legend_texts, loc='upper right', fontsize=10, frameon=True, title="Estatísticas Detalhadas")
        plt.title(f"Box Plot de Pontos, Rebotes e Assistências - {player_name}")
        plt.ylabel("Valores")
        plt.xticks([1, 2, 3], ["Pontos", "Rebotes", "Assistências"])
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.savefig(os.path.join(img_dir, f"{player_name}_boxplot.jpg"))
        plt.close()

    plot_boxplot(dados)
