from nba_api.stats.endpoints import playergamelog, teamgamelog, leaguegamefinder
import pandas as pd

def coletar_dados_jogadores(player_ids, season):
    """
    Coleta dados de jogo para múltiplos jogadores.

    Args:
        player_ids (list): Lista de IDs de jogadores.
        season (str): Temporada no formato 'YYYY-YY'.

    Returns:
        pd.DataFrame: Dados consolidados de todos os jogadores.
    """
    todos_os_dados = []
    for player_id in player_ids:
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        data = gamelog.get_data_frames()[0]
        data['Player_ID'] = player_id  # Adicionar ID do jogador para diferenciar
        print(f"Dados coletados para o jogador {player_id}:\n{data.head()}")
        if not data.empty:  # Verificar se o DataFrame não está vazio
            todos_os_dados.append(data)

    if todos_os_dados:
        return pd.concat(todos_os_dados, ignore_index=True)
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio se nenhum dado foi coletado

def coletar_dados_time(team_id, season):
    """
    Coleta dados do time em uma temporada específica.

    Args:
        team_id (int): ID do time.
        season (str): Temporada no formato 'YYYY-YY'.

    Returns:
        pd.DataFrame: Dados do time.
    """
    gamelog = teamgamelog.TeamGameLog(team_id=team_id, season=season)
    return gamelog.get_data_frames()[0]

def coletar_dados_todos_os_times(season):
    """
    Coleta dados de todos os times na temporada especificada.

    Args:
        season (str): Temporada no formato 'YYYY-YY'.

    Returns:
        pd.DataFrame: Dados de todos os times.
    """
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season)
    return gamefinder.get_data_frames()[0]

    print("Colunas disponíveis nos dados de todos os times:")
    print(dados_todos_os_times.columns)
