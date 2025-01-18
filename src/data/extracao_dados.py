from nba_api.stats.endpoints import playercareerstats, teamgamelog, scoreboardv2
from nba_api.stats.static import players, teams
import pandas as pd
import datetime


def extrair_dados_time(time_nome, temporada):
    """
    Extrai dados dos jogos de um time específico na NBA para uma temporada.

    Args:
        time_nome (str): Nome do time.
        temporada (str): Temporada no formato '2023-24'.

    Returns:
        pd.DataFrame: Dados dos jogos do time.
    """
    time = [t for t in teams.get_teams() if t['full_name'] == time_nome][0]
    team_id = time['id']

    gamelog = teamgamelog.TeamGameLog(team_id=team_id, season=temporada)
    return gamelog.get_data_frames()[0]


def extrair_dados_jogadores(jogadores_ids):
    """
    Extrai dados de carreira de jogadores específicos com base nos IDs.

    Args:
        jogadores_ids (list): Lista com os IDs dos jogadores.

    Returns:
        pd.DataFrame: Dados de carreira dos jogadores.
    """
    jogadores_dados = []
    for player_id in jogadores_ids:
        stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        jogadores_dados.append(stats.get_data_frames()[0])

    return pd.concat(jogadores_dados, ignore_index=True)


def preencher_placares_faltantes(data_inicio, data_fim):
    """
    Preenche placares de jogos entre duas datas.

    Args:
        data_inicio (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Dados de placares dos jogos.
    """
    placares = scoreboardv2.ScoreboardV2(game_date=data_inicio, day_offset=0)
    df_placares = placares.get_data_frames()[0]
    return df_placares
