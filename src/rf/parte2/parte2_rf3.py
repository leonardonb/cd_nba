from nba_api.stats.endpoints import playergamelog
import pandas as pd
import os
import matplotlib.pyplot as plt

def fetch_player_game_data_against_team(player_id, opponent_abbr):
    """
    Busca os dados de jogos de um jogador contra um time específico na temporada atual, 
    garantindo que ele jogue pelo Brooklyn Nets (BKN).

    Args:
        player_id (int): ID do jogador na NBA API.
        opponent_abbr (str): Abreviação do time adversário (ex.: "LAL" para Los Angeles Lakers).

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos jogos contra o adversário.
    """
    try:
        player_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season="2024-25",
            timeout=30
        ).get_data_frames()[0]

        player_log = player_log[player_log['MATCHUP'].str.contains("BKN")]
        player_log = player_log[player_log['MATCHUP'].str.contains(opponent_abbr)]

        player_log = player_log.rename(columns={
            'GAME_DATE': 'Data do Jogo',
            'MATCHUP': 'Adversário',
            'WL': 'V ou D',
            'PTS': 'PTS',
            'REB': 'REB',
            'AST': 'AST',
            'FG3A': 'Tentativas de Cestas de 3 PTS',
            'FG3M': 'Cestas de 3 PTS Marcados',
            'MIN': 'Tempo de Permanência do Jogador em Quadra'
        })

        player_log['Casa/Fora'] = player_log['Adversário'].apply(lambda x: 'Casa' if 'vs.' in x else 'Fora')
        player_log['Adversário'] = opponent_abbr
        player_log['V ou D'] = player_log['V ou D'].map({'W': 'V', 'L': 'D'})

        columns = [
            'Data do Jogo', 'Adversário', 'V ou D', 'Casa/Fora', 'PTS', 'REB', 'AST',
            'Tentativas de Cestas de 3 PTS', 'Cestas de 3 PTS Marcados',
            'Tempo de Permanência do Jogador em Quadra'
        ]
        player_log = player_log[columns]

        return player_log

    except Exception as e:
        print(f"Erro ao buscar dados do jogador {player_id}: {e}")
        return pd.DataFrame()


def apresentar_dados_partidas_contra_time(opponent_abbr, output_dir, html_dir, img_dir):
    """
    Apresenta os dados das partidas dos três jogadores do Brooklyn Nets contra um time adversário.

    Args:
        opponent_abbr (str): Abreviação do time adversário (ex.: "LAL" para Los Angeles Lakers).
        output_dir (str): Diretório para salvar arquivos CSV.
        html_dir (str): Diretório para salvar arquivos HTML.
        img_dir (str): Diretório para salvar imagens.
    """
    # IDs dos jogadores determinados
    players = [
        {'PLAYER': 'Cam Thomas', 'PLAYER_ID': 1630560},
        {'PLAYER': 'Cameron Johnson', 'PLAYER_ID': 1629661},
        {'PLAYER': 'D\'Angelo Russell', 'PLAYER_ID': 1626156}
    ]

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for player in players:
        player_name = player['PLAYER']
        player_id = player['PLAYER_ID']

        try:
            print(f"Buscando dados do jogador: {player_name}, ID: {player_id}")
            player_game_data = fetch_player_game_data_against_team(player_id, opponent_abbr)

            if player_game_data.empty:
                print(f"Nenhuma partida encontrada para {player_name} contra {opponent_abbr}.")
                continue

            # Salvar como CSV
            csv_path = os.path.join(output_dir, f"{player_name}_vs_{opponent_abbr}.csv")
            player_game_data.to_csv(csv_path, index=False)
            print(f"Tabela CSV salva em: {csv_path}")

            # Salvar como HTML
            html_path = os.path.join(html_dir, f"{player_name}_vs_{opponent_abbr}.html")
            player_game_data.to_html(html_path, index=False)
            print(f"Tabela HTML salva em: {html_path}")

            # Salvar como imagem
            img_path = os.path.join(img_dir, f"{player_name}_vs_{opponent_abbr}.jpg")
            salvar_tabela_como_imagem(player_game_data, img_path, f"Partidas contra {opponent_abbr} - {player_name}")

        except Exception as e:
            print(f"Erro ao processar dados do jogador {player_name}: {e}")

    print('Processamento da Parte2-RF3 concluído.')


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

    fig, ax = plt.subplots(figsize=(12, len(df) * 0.6))
    ax.axis("off")
    ax.axis("tight")
    ax.set_title(title, fontsize=16, weight="bold")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(img_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Tabela salva como imagem em: {img_path}")
