from nba_api.stats.endpoints import TeamGameLog
import pandas as pd

def coletar_dados_time(team_id, season):
    """
    Coleta os dados do time para uma temporada específica.
    Args:
        team_id (int): ID do time.
        season (str): Temporada no formato 'YYYY-YY'.
    Returns:
        pd.DataFrame: Dados do time na temporada.
    """
    print(f"Enviando solicitação para a temporada {season}...")
    try:
        gamelog = TeamGameLog(team_id=team_id, season=season)
        data = gamelog.get_data_frames()[0]
    except Exception as e:
        print(f"Erro ao coletar dados: {e}")
        raise

    return data
