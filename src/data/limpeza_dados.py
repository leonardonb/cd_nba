import pandas as pd

def adicionar_informacoes_placar(data):
    """
    Adiciona colunas ao dataset relacionadas ao placar dos jogos.

    Args:
        data (pd.DataFrame): Dados do time contendo as colunas 'PTS' e 'PTS_Opp'.

    Returns:
        pd.DataFrame: Dataset atualizado com novas colunas.
    """
    if 'PTS' not in data.columns or 'PTS_Opp' not in data.columns:
        raise KeyError("As colunas 'PTS' (pontos do time) e 'PTS_Opp' (pontos do adversário) são necessárias no dataset.")

    # Preencher valores nulos com 0
    data['PTS'].fillna(0, inplace=True)
    data['PTS_Opp'].fillna(0, inplace=True)

    # Adicionar coluna Resultado
    data['Resultado'] = data.apply(
        lambda row: 'Vitória' if row['PTS'] > row['PTS_Opp'] else 'Derrota', axis=1
    )

    # Adicionar coluna Diferença de Pontos
    data['Diferenca_Pontos'] = data['PTS'] - data['PTS_Opp']

    # Adicionar coluna Total de Pontos
    data['Total_Pontos'] = data['PTS'] + data['PTS_Opp']

    return data


def tratar_dados_jogadores():
    return None