from nba_api.stats.endpoints import playergamelog
import pandas as pd
import os
import matplotlib.pyplot as plt


def fetch_player_game_data_home_away(player_id):
    """
    Busca os dados de jogos de um jogador na temporada atual para o Brooklyn Nets.

    Args:
        player_id (int): ID do jogador na NBA API.

    """
    try:
        player_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season="2024-25",
            timeout=30
        ).get_data_frames()[0]

        player_log = player_log[player_log['MATCHUP'].str.contains("BKN")]
        player_log['Casa/Fora'] = player_log['MATCHUP'].apply(lambda x: 'Casa' if 'vs.' in x else 'Fora')
        player_log['Adversário'] = player_log['MATCHUP'].str.split().str[-1]

        return player_log[['Adversário', 'Casa/Fora']]

    except Exception as e:
        print(f"Erro ao buscar dados do jogador {player_id}: {e}")
        return pd.DataFrame()


def apresentar_dados_jogos_casa_fora(opponent_abbr, output_dir, html_dir, img_dir):
    """
    Apresenta os dados das partidas dos jogadores do Brooklyn Nets dentro e fora de casa,
    tanto no geral quanto contra um time específico.

    Args:
        opponent_abbr (str): Abreviação do time adversário (ex.: "LAL" para Los Angeles Lakers).
        output_dir (str): Diretório para salvar arquivos CSV.
        html_dir (str): Diretório para salvar arquivos HTML.
        img_dir (str): Diretório para salvar imagens.
    """
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
            player_game_data = fetch_player_game_data_home_away(player_id)

            if player_game_data.empty:
                print(f"Nenhuma partida encontrada para {player_name}.")
                continue

            # Primeira parte: Total de partidas em casa e fora
            total_home_away = player_game_data.groupby('Casa/Fora').size().reset_index(name='Quantidade')

            # Segunda parte: Partidas contra o time específico
            games_against_opponent = player_game_data[player_game_data['Adversário'] == opponent_abbr]
            opponent_home_away = games_against_opponent.groupby('Casa/Fora').size().reset_index(name='Quantidade')

            # Salvar como CSV
            csv_total_path = os.path.join(output_dir, f"{player_name}_casa_fora_total.csv")
            total_home_away.to_csv(csv_total_path, index=False)
            print(f"Tabela total salva como CSV em: {csv_total_path}")

            csv_opponent_path = os.path.join(output_dir, f"{player_name}_vs_{opponent_abbr}_casa_fora.csv")
            opponent_home_away.to_csv(csv_opponent_path, index=False)
            print(f"Tabela contra {opponent_abbr} salva como CSV em: {csv_opponent_path}")

            # Salvar como HTML
            html_total_path = os.path.join(html_dir, f"{player_name}_casa_fora_total.html")
            total_home_away.to_html(html_total_path, index=False)
            print(f"Tabela total salva como HTML em: {html_total_path}")

            html_opponent_path = os.path.join(html_dir, f"{player_name}_vs_{opponent_abbr}_casa_fora.html")
            opponent_home_away.to_html(html_opponent_path, index=False)
            print(f"Tabela contra {opponent_abbr} salva como HTML em: {html_opponent_path}")

            # Salvar como imagem
            img_total_path = os.path.join(img_dir, f"{player_name}_casa_fora_total.jpg")
            salvar_tabela_como_imagem(total_home_away, img_total_path, f"Total Jogos em Casa/Fora - {player_name}")

            img_opponent_path = os.path.join(img_dir, f"{player_name}_vs_{opponent_abbr}_casa_fora.jpg")
            salvar_tabela_como_imagem(opponent_home_away, img_opponent_path, f"Jogos contra {opponent_abbr} - {player_name}")

        except Exception as e:
            print(f"Erro ao processar dados do jogador {player_name}: {e}")

    print('Processamento do RF4 concluído.')


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
