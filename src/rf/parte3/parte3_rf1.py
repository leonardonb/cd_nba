import numpy as np
import pandas as pd
import scipy.stats as stats

def aplicar_metodo_gumbel(dados, valores_x):
    """
    Aplica o método de Gumbel para modelar eventos extremos e calcula as probabilidades solicitadas.
    
    Args:
        dados (pd.DataFrame): DataFrame contendo as colunas 'PTS', 'REB' e 'AST'.
        valores_x (dict): Valores de X para calcular as probabilidades para cada métrica.

    Returns:
        pd.DataFrame: DataFrame contendo as probabilidades calculadas para cada métrica.
    """
    resultados = {
        "Métrica": ["Probabilidade de marcar acima de X (%)", 
                    "Probabilidade de atingir ou exceder X (%)", 
                    "Probabilidade de atingir ou ficar abaixo de X (%)", 
                    "Proporção de valores menores ou iguais a X (%)", 
                    "Valores menores que X", 
                    "Proporção de valores menores que X (%)"]
    }

    for coluna in ['PTS', 'REB', 'AST']:
        if coluna in dados:
            valores = dados[coluna].dropna().values
            
            loc, scale = stats.gumbel_r.fit(valores)
            
            x = valores_x.get(coluna, np.median(valores))
            
            # Cálculos
            prob_acima_x = round((1 - stats.gumbel_r.cdf(x, loc, scale)) * 100, 2)  # Probabilidade de marcar acima de X (%)
            prob_excede_x = round(stats.gumbel_r.sf(x, loc, scale) * 100, 2)  # Probabilidade de atingir ou exceder X (%)
            prob_abaixo_x = round(stats.gumbel_r.cdf(x, loc, scale) * 100, 2)  # Probabilidade de atingir ou ficar abaixo de X (%)
            prop_menor_igual_x = round(np.mean(valores <= x) * 100, 2)  # Proporção de valores menores ou iguais a X (%)
            valores_menores_x = valores[valores < x]  # Valores menores que X
            prop_menor_x = round(np.mean(valores < x) * 100, 2)  # Proporção de valores menores que X (%)
            
            resultados[coluna] = [
                prob_acima_x,
                prob_excede_x,
                prob_abaixo_x,
                prop_menor_igual_x,
                valores_menores_x.tolist(),
                prop_menor_x
            ]
    
    print('Processamento da Parte3-RF1 concluído.')
    return pd.DataFrame(resultados)
