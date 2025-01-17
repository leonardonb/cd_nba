import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report


def regressao_linear(data):
    """
    Executa regressão linear para prever pontos por jogo e retorna resultados como string.

    Args:
        data (pd.DataFrame): Dados tratados contendo as colunas 'PTS', 'REB', 'AST', 'PLUS_MINUS'.

    Returns:
        str: Resultados da regressão linear.
    """
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    import pandas as pd

    # Selecionar variáveis independentes (features) e dependente (target)
    X = data[['REB', 'AST', 'PLUS_MINUS']]
    y = data['PTS']

    # Dividir os dados em conjunto de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo de regressão linear
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    y_pred = modelo.predict(X_test)

    # Avaliar o modelo
    mse = mean_squared_error(y_test, y_pred)
    coeficientes = modelo.coef_
    intercepto = modelo.intercept_

    # Exibir uma previsão exemplo
    exemplo = pd.DataFrame([[5, 7, 10]], columns=['REB', 'AST', 'PLUS_MINUS'])
    previsao = modelo.predict(exemplo)

    # Retornar resultados como string
    return (
        f"[Regressão Linear] Prevendo Pontos por Jogo:\n"
        f"Erro Quadrático Médio (MSE): {mse:.2f}\n"
        f"Coeficientes (Impacto das variáveis): {coeficientes}\n"
        f"Intercepto: {intercepto:.2f}\n"
        f"Previsão de pontos para o exemplo {exemplo.values}: {previsao[0]:.2f}\n"
    )

def regressao_logistica(data):
    """
    Executa regressão logística para prever vitória ou derrota e retorna resultados como string.

    Args:
        data (pd.DataFrame): Dados tratados contendo as colunas 'PTS', 'REB', 'AST' e 'WL'.

    Returns:
        str: Resultados da regressão logística.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    import pandas as pd

    # Garantir que não existam valores NaN na coluna 'WL'
    if data['WL'].isna().sum() > 0:
        data = data.dropna(subset=['WL'])

    # Mapear valores categóricos de 'WL' (Win/Loss) para 1 (Win) e 0 (Loss)
    data['WL'] = data['WL'].astype(int)

    # Selecionar variáveis independentes (features) e dependente (target)
    X = data[['PTS', 'REB', 'AST']]
    y = data['WL']

    # Dividir os dados em conjunto de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo de regressão logística
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    y_pred = modelo.predict(X_test)

    # Avaliar o modelo
    acc = accuracy_score(y_test, y_pred)
    relatorio_classificacao = classification_report(y_test, y_pred)

    # Exibir uma previsão exemplo
    exemplo = pd.DataFrame([[120, 50, 25]], columns=['PTS', 'REB', 'AST'])
    previsao = modelo.predict(exemplo)
    probabilidade = modelo.predict_proba(exemplo)

    # Retornar resultados como string
    return (
        f"[Regressão Logística] Prevendo Vitória ou Derrota:\n"
        f"Acurácia do Modelo: {acc:.2f}\n"
        f"Relatório de Classificação:\n{relatorio_classificacao}\n"
        f"Previsão de vitória para o exemplo {exemplo.values}: "
        f"{'Vitória' if previsao[0] == 1 else 'Derrota'}\n"
        f"Probabilidades (Derrota/Vitória): {probabilidade}\n"
    )
