#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementação para geração de gráficos de interpretação das previsões (RF8)
usando modelos GAMLSS (PoissonGAM e LinearGAM) para jogadores dos Brooklyn Nets:
Cam Thomas, Cameron Johnson e D'Angelo Russell.

Os dados são obtidos para as temporadas 2023-24 e 2024-25 via nba_api.
As saídas serão geradas em:
    - CSV: reports/arquivos_csv/parte3 (dados dos gráficos)
    - HTML: reports/html/parte3 (dados e gráficos interativos)
    - JPG: reports/imagens/parte3 (imagens dos gráficos)

O prefixo dos arquivos gerados é rf8_.

A função principal deste módulo é:
    graficos_gamglss_nets
"""

# --- Monkey patch para corrigir a ausência da propriedade "A" em matrizes esparsas ---
import scipy.sparse
if not hasattr(scipy.sparse.csr_matrix, 'A'):
    scipy.sparse.csr_matrix.A = property(lambda self: self.toarray())

# Patch para evitar o erro de deprecated do np.int (se necessário)
import numpy as np
np.int = int

import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3  # para gerar gráficos interativos em HTML

from pygam import PoissonGAM, LinearGAM, s
from scipy.stats import poisson, norm, mode
from nba_api.stats.endpoints import playergamelog

# Para avaliação de classificação:
from sklearn.metrics import confusion_matrix, roc_curve, auc

def graficos_gamglss_nets():
    """
    Função principal que:
      1. Obtém os dados reais (via nba_api) para os jogadores dos Brooklyn Nets (Cam Thomas,
         Cameron Johnson e D'Angelo Russell) nas temporadas 2023-24 e 2024-25.
      2. Ajusta os modelos PoissonGAM e LinearGAM para as estatísticas (points, rebounds, assists),
         gerando previsões para o próximo jogo.
      3. Gera os seguintes gráficos para cada jogador e estatística:
           - Matriz de Confusão (classificação "acima/abaixo da mediana" usando o modelo Poisson)
           - Gráfico da Distribuição de Probabilidade Predita (PMF da distribuição de Poisson para o próximo jogo)
           - Curva ROC (para a classificação "acima/abaixo da mediana")
           - Gráficos de Efeito Parcial (Partial Dependence) para os modelos PoissonGAM e LinearGAM
      4. Para cada gráfico, os dados subjacentes são salvos em CSV e os gráficos são salvos em JPG
         e também gerados em HTML (usando mpld3) para visualização interativa.
    """
    print("Executando RF8: Gerando gráficos através de GAMLSS...")

    # Configurar diretórios de saída
    csv_dir = 'reports/arquivos_csv/parte3'
    html_dir = 'reports/html/parte3'
    img_dir = 'reports/imagens/parte3'
    for d in [csv_dir, html_dir, img_dir]:
        os.makedirs(d, exist_ok=True)

    # Definir jogadores (IDs da nba_api) e nomes – Brooklyn Nets
    players = {
        1630560: 'Cam Thomas',
        1629661: 'Cameron Johnson',
        1626156: "D'Angelo Russell"
    }
    seasons = ["2023-24", "2024-25"]
    data_list = []
    # Obter dados via nba_api para cada temporada e jogador
    for season in seasons:
        for pid, player_name in players.items():
            print(f"Buscando dados para {player_name} na temporada {season}...")
            try:
                time.sleep(1)  # Delay para evitar rate limiting
                gamelog = playergamelog.PlayerGameLog(
                    player_id=pid,
                    season=season,
                    season_type_all_star='Regular Season'
                )
                df = gamelog.get_data_frames()[0]
                # Filtrar apenas jogos dos Nets (usando "MATCHUP" que contenha "BKN")
                df = df[df["MATCHUP"].str.contains("BKN")]
                if df.empty:
                    print(f"Não há dados para {player_name} na temporada {season}.")
                    continue
                df = df.sort_values("GAME_DATE")
                df["game"] = range(1, len(df) + 1)
                df["player_id"] = pid
                df["team"] = "BKN"
                df = df.rename(columns={"PTS": "points", "REB": "rebounds", "AST": "assists"})
                df = df[["team", "player_id", "game", "points", "rebounds", "assists"]]
                data_list.append(df)
            except Exception as e:
                print(f"Erro ao buscar dados para {player_name} na temporada {season}: {e}")
    if not data_list:
        print("Nenhum dado foi recuperado da API nba_api.")
        return
    data = pd.concat(data_list, ignore_index=True)

    # Armazenar modelos e dados para os gráficos
    modelos = {}  # modelos[player][stat] = { 'poisson': ..., 'linear': ..., 'X': ..., 'y': ..., 'median': ..., 'predicted_poisson': ... }
    stats = ['points', 'rebounds', 'assists']
    for pid, player_name in players.items():
        modelos[player_name] = {}
        player_data = data[data['player_id'] == pid]
        if player_data.empty:
            print(f"Sem dados para {player_name}.")
            continue
        for stat in stats:
            X = player_data['game'].values.reshape(-1, 1)
            y = player_data[stat].values
            # Ajuste dos modelos
            poisson_model = PoissonGAM(s(0))
            poisson_model.gridsearch(X, y)
            linear_model = LinearGAM(s(0))
            linear_model.gridsearch(X, y)
            next_game = player_data['game'].max() + 1
            pred_poisson = poisson_model.predict(np.array([[next_game]]))[0]
            pred_linear = linear_model.predict(np.array([[next_game]]))[0]
            median_val = np.median(y)
            modelos[player_name][stat] = {
                'X': X,
                'y': y,
                'median': median_val,
                'poisson': poisson_model,
                'linear': linear_model,
                'predicted_poisson': pred_poisson,
                'predicted_linear': pred_linear
            }

    # --- Geração dos gráficos para cada jogador e estatística ---
    for player_name in modelos:
        for stat in modelos[player_name]:
            dados = modelos[player_name][stat]
            X = dados['X']
            y = dados['y']
            median_val = dados['median']
            poisson_model = dados['poisson']
            linear_model = dados['linear']

            #### 1. Matriz de Confusão (modelo Poisson)
            actual = (y > median_val).astype(int)
            y_pred = poisson_model.predict(X)
            predicted = (y_pred > median_val).astype(int)
            cm = confusion_matrix(actual, predicted)
            # Gerar figura
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
            ax.set_title(f"Matriz de Confusão - {player_name} - {stat}")
            ax.set_xlabel("Predito")
            ax.set_ylabel("Real")
            # Salvar como JPG
            cm_jpg_path = os.path.join(img_dir, f"rf8_confusion_{player_name.replace(' ', '_')}_{stat}.jpg")
            fig.savefig(cm_jpg_path, dpi=300, bbox_inches='tight')
            # Gerar HTML interativo com mpld3
            cm_html_graph_path = os.path.join(html_dir, f"rf8_confusion_{player_name.replace(' ', '_')}_{stat}_graph.html")
            html_str = mpld3.fig_to_html(fig)
            with open(cm_html_graph_path, "w") as f:
                f.write(html_str)
            plt.close(fig)
            print(f"Matriz de Confusão (JPG) salva em: {cm_jpg_path}")
            print(f"Matriz de Confusão (HTML) salva em: {cm_html_graph_path}")
            # Salvar dados da matriz em CSV e HTML (dados)
            df_cm = pd.DataFrame(cm)
            cm_csv_path = os.path.join(csv_dir, f"rf8_confusion_{player_name.replace(' ', '_')}_{stat}.csv")
            df_cm.to_csv(cm_csv_path, index=False)
            cm_data_html_path = os.path.join(html_dir, f"rf8_confusion_{player_name.replace(' ', '_')}_{stat}_data.html")
            df_cm.to_html(cm_data_html_path, index=False)

            #### 2. Gráfico de Probabilidade Predita (Distribuição de Poisson)
            pred_lambda = dados['predicted_poisson']
            max_range = int(max(1.5 * np.max(y), 30))
            x_vals = np.arange(0, max_range)
            pmf_vals = poisson.pmf(x_vals, pred_lambda)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(x_vals, pmf_vals, color="skyblue", edgecolor="black", label=f"λ = {pred_lambda:.1f}")
            refs = {"média": np.mean(y), "mediana": median_val, "moda": np.atleast_1d(mode(y).mode)[0],
                    "mínimo": np.min(y), "máximo": np.max(y)}
            for ref, valor in refs.items():
                ax.axvline(valor, color="red", linestyle="--", label=f"{ref}: {valor:.1f}")
            ax.set_title(f"Distribuição Poisson Predita - {player_name} - {stat}")
            ax.set_xlabel(stat.capitalize())
            ax.set_ylabel("Probabilidade")
            ax.legend()
            # Salvar como JPG
            prob_jpg_path = os.path.join(img_dir, f"rf8_prob_{player_name.replace(' ', '_')}_{stat}.jpg")
            fig.savefig(prob_jpg_path, dpi=300, bbox_inches='tight')
            # Gerar HTML interativo
            prob_html_graph_path = os.path.join(html_dir, f"rf8_prob_{player_name.replace(' ', '_')}_{stat}_graph.html")
            html_str = mpld3.fig_to_html(fig)
            with open(prob_html_graph_path, "w") as f:
                f.write(html_str)
            plt.close(fig)
            print(f"Gráfico de Probabilidade Predita (JPG) salvo em: {prob_jpg_path}")
            print(f"Gráfico de Probabilidade Predita (HTML) salvo em: {prob_html_graph_path}")
            # Salvar dados do gráfico de probabilidade
            df_prob = pd.DataFrame({'x': x_vals, 'pmf': pmf_vals})
            prob_csv_path = os.path.join(csv_dir, f"rf8_prob_{player_name.replace(' ', '_')}_{stat}.csv")
            df_prob.to_csv(prob_csv_path, index=False)
            prob_data_html_path = os.path.join(html_dir, f"rf8_prob_{player_name.replace(' ', '_')}_{stat}_data.html")
            df_prob.to_html(prob_data_html_path, index=False)

            #### 3. Curva ROC (modelo Poisson)
            prob_preds = 1 - poisson.cdf(median_val, poisson_model.predict(X))
            fpr, tpr, _ = roc_curve(actual, prob_preds)
            roc_auc = auc(fpr, tpr)
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.plot(fpr, tpr, color="darkorange", lw=2, label=f"AUC = {roc_auc:.2f}")
            ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel("Taxa de Falso Positivo")
            ax.set_ylabel("Taxa de Verdadeiro Positivo")
            ax.set_title(f"Curva ROC - {player_name} - {stat}")
            ax.legend(loc="lower right")
            roc_jpg_path = os.path.join(img_dir, f"rf8_roc_{player_name.replace(' ', '_')}_{stat}.jpg")
            fig.savefig(roc_jpg_path, dpi=300, bbox_inches='tight')
            # Gerar HTML interativo
            roc_html_graph_path = os.path.join(html_dir, f"rf8_roc_{player_name.replace(' ', '_')}_{stat}_graph.html")
            html_str = mpld3.fig_to_html(fig)
            with open(roc_html_graph_path, "w") as f:
                f.write(html_str)
            plt.close(fig)
            print(f"Curva ROC (JPG) salva em: {roc_jpg_path}")
            print(f"Curva ROC (HTML) salva em: {roc_html_graph_path}")
            # Salvar dados da curva ROC
            df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
            roc_csv_path = os.path.join(csv_dir, f"rf8_roc_{player_name.replace(' ', '_')}_{stat}.csv")
            df_roc.to_csv(roc_csv_path, index=False)
            roc_data_html_path = os.path.join(html_dir, f"rf8_roc_{player_name.replace(' ', '_')}_{stat}_data.html")
            df_roc.to_html(roc_data_html_path, index=False)

            #### 4. Efeito Parcial (Partial Dependence)
            grid = np.linspace(np.min(X), np.max(X), 100).reshape(-1, 1)
            # Para o modelo Poisson
            pd_poisson = poisson_model.partial_dependence(term=0, X=grid)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(grid, pd_poisson, color="green", lw=2)
            ax.set_xlabel("Jogo")
            ax.set_ylabel("Efeito Parcial (Poisson)")
            ax.set_title(f"Efeito Parcial - PoissonGAM - {player_name} - {stat}")
            coef_poisson_jpg = os.path.join(img_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_poisson.jpg")
            fig.savefig(coef_poisson_jpg, dpi=300, bbox_inches='tight')
            # Gerar HTML interativo
            coef_poisson_html_graph = os.path.join(html_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_poisson_graph.html")
            html_str = mpld3.fig_to_html(fig)
            with open(coef_poisson_html_graph, "w") as f:
                f.write(html_str)
            plt.close(fig)
            print(f"Efeito Parcial (Poisson) (JPG) salvo em: {coef_poisson_jpg}")
            print(f"Efeito Parcial (Poisson) (HTML) salvo em: {coef_poisson_html_graph}")
            # Salvar dados do efeito parcial (Poisson)
            df_pd_poisson = pd.DataFrame({'jogo': grid.flatten(), 'efeito_poisson': pd_poisson.flatten()})
            coef_poisson_csv = os.path.join(csv_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_poisson.csv")
            df_pd_poisson.to_csv(coef_poisson_csv, index=False)
            coef_poisson_data_html = os.path.join(html_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_poisson_data.html")
            df_pd_poisson.to_html(coef_poisson_data_html, index=False)

            # Para o modelo Linear
            pd_linear = linear_model.partial_dependence(term=0, X=grid)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(grid, pd_linear, color="purple", lw=2)
            ax.set_xlabel("Jogo")
            ax.set_ylabel("Efeito Parcial (Linear)")
            ax.set_title(f"Efeito Parcial - LinearGAM - {player_name} - {stat}")
            coef_linear_jpg = os.path.join(img_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_linear.jpg")
            fig.savefig(coef_linear_jpg, dpi=300, bbox_inches='tight')
            # Gerar HTML interativo
            coef_linear_html_graph = os.path.join(html_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_linear_graph.html")
            html_str = mpld3.fig_to_html(fig)
            with open(coef_linear_html_graph, "w") as f:
                f.write(html_str)
            plt.close(fig)
            print(f"Efeito Parcial (Linear) (JPG) salvo em: {coef_linear_jpg}")
            print(f"Efeito Parcial (Linear) (HTML) salvo em: {coef_linear_html_graph}")
            # Salvar dados do efeito parcial (Linear)
            df_pd_linear = pd.DataFrame({'jogo': grid.flatten(), 'efeito_linear': pd_linear.flatten()})
            coef_linear_csv = os.path.join(csv_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_linear.csv")
            df_pd_linear.to_csv(coef_linear_csv, index=False)
            coef_linear_data_html = os.path.join(html_dir, f"rf8_coef_{player_name.replace(' ', '_')}_{stat}_linear_data.html")
            df_pd_linear.to_html(coef_linear_data_html, index=False)

    print("Processamento concluído. Todos os gráficos foram gerados em CSV, HTML e JPG com sucesso!")
