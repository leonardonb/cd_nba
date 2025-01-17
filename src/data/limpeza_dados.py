def tratar_dados_jogadores(data):
    """
    Trata os dados coletados de múltiplos jogadores.

    Args:
        data (pd.DataFrame): Dados brutos.

    Returns:
        pd.DataFrame: Dados tratados.
    """
    # Selecionar colunas relevantes
    colunas_relevantes = ['Player_ID', 'Game_ID', 'PTS', 'REB', 'AST', 'PLUS_MINUS']
    data = data.loc[:, colunas_relevantes]  # Garante que é uma cópia explícita

    # Preencher valores ausentes
    data = data.fillna(0)  # Substituir inplace por uma atribuição explícita

    return data


