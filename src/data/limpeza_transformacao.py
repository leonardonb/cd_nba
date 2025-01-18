import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def verificar_dados_ausentes(df):
    """
    Verifica e preenche valores ausentes no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame a ser verificado.

    Returns:
        pd.DataFrame: DataFrame com valores ausentes preenchidos.
    """
    return df.ffill().bfill()

def remover_colunas_irrelevantes(df, colunas_irrelevantes):
    """
    Remove colunas irrelevantes do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame original.
        colunas_irrelevantes (list): Lista de colunas a serem removidas.

    Returns:
        pd.DataFrame: DataFrame atualizado.
    """
    return df.drop(columns=colunas_irrelevantes, errors='ignore')

def normalizar_valores(df, colunas):
    """
    Normaliza valores numéricos em colunas especificadas.

    Args:
        df (pd.DataFrame): DataFrame original.
        colunas (list): Colunas a serem normalizadas.

    Returns:
        pd.DataFrame: DataFrame com valores normalizados.
    """
    for coluna in colunas:
        df[coluna] = (df[coluna] - df[coluna].mean()) / df[coluna].std()
    return df

def tratar_outliers(df, colunas):
    """
    Remove outliers das colunas especificadas usando o método IQR.

    Args:
        df (pd.DataFrame): DataFrame original.
        colunas (list): Colunas para verificar e tratar outliers.

    Returns:
        pd.DataFrame: DataFrame sem outliers.
    """
    for coluna in colunas:
        Q1 = df[coluna].quantile(0.25)
        Q3 = df[coluna].quantile(0.75)
        IQR = Q3 - Q1
        lim_inferior = Q1 - 1.5 * IQR
        lim_superior = Q3 + 1.5 * IQR
        df = df[(df[coluna] >= lim_inferior) & (df[coluna] <= lim_superior)]
    return df

def remover_duplicatas(df):
    """
    Remove duplicatas do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: DataFrame sem duplicatas.
    """
    return df.drop_duplicates()

def separar_treino_teste(df, target_column, test_size=0.2, random_state=42):
    """
    Separa os dados em conjuntos de treinamento e teste.

    Args:
        df (pd.DataFrame): DataFrame com os dados processados.
        target_column (str): Nome da coluna alvo (variável dependente).
        test_size (float): Proporção de dados para o conjunto de teste (default: 0.2).
        random_state (int): Semente para reprodutibilidade (default: 42).

    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
