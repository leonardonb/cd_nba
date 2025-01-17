def analisar_pontuacao_media(data):
    """
    Calcula a pontuação média por jogador.

    Args:
        data (pd.DataFrame): Dados tratados.

    Returns:
        pd.Series: Pontuação média por jogador.
    """
    return data.groupby('Player_ID')['PTS'].mean()

def analisar_pontos_time(data):
    """
    Calcula a média de pontos por jogo para o time.

    Args:
        data (pd.DataFrame): Dados do time.

    Returns:
        float: Média de pontos do time.
    """
    return data['PTS'].mean()

