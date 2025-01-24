from nba_api.stats.endpoints import commonteamroster, playergamelog
import pandas as pd
import os
import matplotlib.pyplot as plt


def fetch_team_players_by_id(team_id):
    """
    Busca todos os jogadores de um time específico usando o team_id.

    Args:
        team_id (int): ID do time na NBA API.

    Returns:
        list: Lista de dicionários contendo os dados dos jogadores.
    """
    try:
        roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]
        players = roster[['PLAYER', 'PLAYER_ID']].to_dict('records')
        return players
    except Exception as e:
        print(f"Erro ao buscar jogadores do time (ID: {team_id}): {e}")
        return []


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

        player_log['V ou D'] = player_log['V ou D'].map({'W': 'V', 'L': 'D'})
        player_log['Casa/Fora'] = player_log['Adversário'].apply(lambda x: 'Casa' if 'vs.' in x else 'Fora')
        player_log['Adversário'] = player_log['Adversário'].apply(lambda x: x.split(' ')[-1])

        columns = [
            'Data do Jogo', 'Adversário', 'V ou D', 'Casa/Fora', 'PTS', 'REB', 'AST',
            'Tentativas de Cestas de 3 PTS', 'Cestas de 3 PTS Marcados',
            'Tempo de Permanência do Jogador em Quadra'
        ]
        player_log = player_log[columns]

        return player_log
    except Exception as e:
        print(f"Erro ao buscar dados do jogador: {e}")
        return pd.DataFrame()


def apresentar_dados_partidas_time_por_id(team_id, output_dir, html_dir, img_dir):
    players = fetch_team_players_by_id(team_id)

    if not players:
        print("Nenhum jogador encontrado para o time especificado.")
        return

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for player in players:
        player_name = player['PLAYER']
        player_id = player['PLAYER_ID']

        try:
            print(f"Buscando dados do jogador: {player_name}, ID: {player_id}")
            player_game_data = fetch_player_game_data(player_id)

            player_log = playergamelog.PlayerGameLog(
                player_id=player_id,
                season="2024-25",
                timeout=30
            ).get_data_frames()[0]

            if player_log.empty:
                raise ValueError(f"Nenhuma partida encontrada para o jogador ID: {player_id}")

            if not player_game_data.empty:
                csv_path = os.path.join(output_dir, f"{player_name}_dados_partidas.csv")
                player_game_data.to_csv(csv_path, index=False)
                print(f"Tabela CSV salva em: {csv_path}")

                html_path = os.path.join(html_dir, f"{player_name}_dados_partidas.html")
                player_game_data.to_html(html_path, index=False)
                print(f"Tabela HTML salva em: {html_path}")

                img_path = os.path.join(img_dir, f"{player_name}_dados_partidas.jpg")
                salvar_tabela_como_imagem(player_game_data, img_path, f"Dados das Partidas - {player_name}")


        except Exception as e:
            print(f"Erro ao processar dados do jogador {player_name}: {e}")
    
    print('Processamento da Parte2-RF2 concluído.')


def salvar_tabela_como_imagem(df, img_path, title):
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
