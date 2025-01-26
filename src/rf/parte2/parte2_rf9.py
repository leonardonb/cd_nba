from matplotlib import pyplot as plt
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import os

def fetch_career_stats(player_id):
    """
    Busca os dados de carreira de um jogador e retorna os totais de pontos, rebotes e assistências.

    Args:
        player_id (int): ID do jogador na NBA API.

    Returns:
        pd.DataFrame: DataFrame com os totais de carreira do jogador.
    """
    try:
        career_stats = playercareerstats.PlayerCareerStats(
            player_id=player_id, timeout=30
        ).get_data_frames()[0]

        career_totals = career_stats[career_stats['LEAGUE_ID'] == '00']
        career_totals = career_totals.rename(columns={
            'PTS': 'Pontos',
            'REB': 'Rebotes',
            'AST': 'Assistências'
        })

        totals = career_totals[['Pontos', 'Rebotes', 'Assistências']].sum()
        return totals

    except Exception as e:
        print(f"Erro ao buscar dados de carreira do jogador {player_id}: {e}")
        return pd.Series({'Pontos': 0, 'Rebotes': 0, 'Assistências': 0})

def apresentar_totais_carreira(players, output_dir, html_dir, img_dir):
    """
    Calcula e apresenta os totais de pontos, rebotes e assistências da carreira dos jogadores.

    Args:
        players (list): Lista de dicionários com nomes e IDs dos jogadores.
        output_dir (str): Diretório para salvar os resultados em CSV.
        html_dir (str): Diretório para salvar os resultados em HTML.
        img_dir (str): Diretório para salvar os resultados como imagens.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for player in players:
        player_name = player['PLAYER']
        player_id = player['PLAYER_ID']

        try:
            print(f"Buscando dados de carreira do jogador: {player_name}, ID: {player_id}")
            totals = fetch_career_stats(player_id)

            # Criar DataFrame final
            final = pd.DataFrame({
                'Estatística': ['Pontos', 'Rebotes', 'Assistências'],
                'Total na Carreira': totals.values
            })

            # Salvar como CSV
            csv_path = os.path.join(output_dir, f"{player_name}_carreira_totais.csv")
            final.to_csv(csv_path, index=False)
            print(f"Tabela CSV salva em: {csv_path}")

            # Salvar como HTML
            html_path = os.path.join(html_dir, f"{player_name}_carreira_totais.html")
            final.to_html(html_path, index=False)
            print(f"Tabela HTML salva em: {html_path}")

            # Salvar como imagem
            img_path = os.path.join(img_dir, f"{player_name}_carreira_totais.jpg")
            salvar_tabela_como_imagem(final, img_path, f"Totais de Carreira - {player_name}")

        except Exception as e:
            print(f"Erro ao processar dados do jogador {player_name}: {e}")

    print('Processamento do RF9 concluído.')

def salvar_tabela_como_imagem(df, img_path, title):
    """
    Salva uma tabela como imagem.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem salvos.
        img_path (str): Caminho para salvar a imagem.
        title (str): Título da tabela.
    """
    if df.empty:
        print("DataFrame vazio. Não é possível salvar como imagem.")
        return

    fig, ax = plt.subplots(figsize=(8, len(df) * 0.6))
    ax.axis("off")
    ax.axis("tight")
    ax.set_title(title, fontsize=14, weight="bold")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(img_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Tabela salva como imagem em: {img_path}")
