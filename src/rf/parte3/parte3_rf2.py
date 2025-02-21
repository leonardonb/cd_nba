import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def visualizando_metodo_gumbel(resultado_df, nome_jogador, output_dir):
    """
    Gera e salva seis gráficos baseados nos dados de eventos extremos do método de Gumbel.
    
    Args:
        resultado_df (pd.DataFrame): DataFrame contendo os resultados das análises.
        nome_jogador (str): Título a ser exibido nos gráficos.
        output_dir (str): Diretório onde os gráficos serão salvos.
    
    Returns:
        None: Os gráficos são gerados e salvos no diretório especificado.
    """
    os.makedirs(output_dir, exist_ok=True)

    metricas = resultado_df['Métrica'][:-2]
    categorias = ['PTS', 'REB', 'AST']

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()

    df_plot = resultado_df.melt(id_vars=["Métrica"], value_vars=["PTS", "REB", "AST"],
                                var_name="Categoria", value_name="Valor")

    # Garantir que a coluna 'Métrica' seja string válida
    df_plot["Métrica"] = df_plot["Métrica"].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, (list, tuple, set)) else str(x))

    # Garantir que a coluna 'Valor' contenha apenas valores numéricos
    df_plot["Valor"] = df_plot["Valor"].apply(lambda x: float(x) if isinstance(x, (int, float, str)) and str(x).replace('.', '', 1).isdigit() else float(sum(x) / len(x)) if isinstance(x, list) else None)

    print("Verificando df_plot antes da plotagem:")
    print(df_plot.dtypes)
    print(df_plot.head())

    for i, metrica in enumerate(metricas):
        valores = resultado_df.loc[i, categorias].astype(float)

        sns.barplot(data=df_plot, x="Categoria", y="Valor", ax=axes[i], palette='viridis', hue="Métrica", legend=False)

        axes[i].set_title(metrica)
        axes[i].set_ylabel('%')
        axes[i].set_ylim(0, 110)

        for j, v in enumerate(valores):
            offset = 5 if v > 90 else 2
            axes[i].text(j, v + offset, f"{v:.2f}%", ha='center', fontsize=10)

    valores_menores = {cat: resultado_df.loc[4, cat] for cat in categorias}
    df_menores = pd.DataFrame({k: pd.Series(v) for k, v in valores_menores.items()})

    for i, cat in enumerate(categorias):
        axes[4].scatter([cat] * len(df_menores[cat]), df_menores[cat], label=cat, s=80)

    axes[4].set_title("Valores Menores que X (Dispersão)")
    axes[4].set_ylabel("Valor")
    axes[4].grid(True, linestyle='--', alpha=0.6)

    valores_proporcao = resultado_df.loc[5, categorias].astype(float)
    sns.barplot(data=pd.DataFrame({'Categoria': categorias, 'Valor': valores_proporcao}),
                x="Categoria", y="Valor", ax=axes[5], hue="Categoria", palette='magma', legend=False)
    axes[5].set_title("Proporção de Valores Menores que X (%)")
    axes[5].set_ylabel('%')
    axes[5].set_ylim(0, 110)

    for j, v in enumerate(valores_proporcao):
        offset = 5 if v > 90 else 2
        axes[5].text(j, v + offset, f"{v:.2f}%", ha='center', fontsize=10)

    plt.suptitle(nome_jogador, fontsize=16)
    plt.tight_layout()

    # Salvar gráfico
    output_path = os.path.join(output_dir, f"{nome_jogador.replace(' ', '_')}_gumbel.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Gráficos salvos em: {output_path}")
    print('Processamento da Parte3-RF2 concluído.')
