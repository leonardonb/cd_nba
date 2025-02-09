# src/rf/parte3/parte3_rf4.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from nba_api.stats.endpoints import leaguedashplayerstats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split, LeaveOneOut

# Função sigmoide para transformar a diferença (valor predito - threshold) em "probabilidade"
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def graficos_regressao_linear():
    """
    Gera gráficos que facilitam a interpretação das previsões obtidas com regressão linear para os jogadores
    do Brooklyn Nets (Cam Thomas, Cameron Johnson e D'Angelo Russell) nas temporadas 2023-24 e 2024-25.

    Para cada variável dependente (PTS, AST, REB), a função:
      - Obtém os dados via nba_api filtrando para o time e jogadores desejados;
      - Treina um modelo de regressão linear (usando LOOCV se necessário);
      - Define uma classificação binária com base na média do target (acima/abaixo da média);
      - Calcula uma "probabilidade predita" aplicando a função sigmoide à diferença (valor predito – média);
      - Salva uma tabela (CSV e HTML) com os dados de avaliação;
      - Gera e salva os seguintes gráficos (JPG):
            1. Matriz de Confusão;
            2. Curva ROC (com AUC);
            3. Gráfico de Coeficientes do Modelo;
            4. Gráfico de Previsões Individuais (com anotação do nome do jogador).
      - Gera também um arquivo HTML que incorpora a tabela e todos os gráficos (por meio de tags <img>).

    Os arquivos de saída usarão o prefixo "rf4_" e serão salvos nas pastas:
         - CSV: reports/arquivos_csv/parte3
         - HTML: reports/html/parte3
         - JPG: reports/imagens/parte3
    """
    # Diretórios de saída
    output_dir = "reports/arquivos_csv/parte3"   # CSV
    html_dir   = "reports/html/parte3"             # HTML
    img_dir    = "reports/imagens/parte3"          # JPG

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # Parâmetros fixos
    team_id = 1610612751  # Brooklyn Nets
    seasons = ["2023-24", "2024-25"]
    desired_player_ids = [1630560, 1629661, 1626156]
    features = ['MIN', 'FGA', 'TOV']
    targets  = ['PTS', 'AST', 'REB']

    # Mapeamento dos targets para nomes em português
    target_mapping = {'PTS': 'Pontos', 'AST': 'Assistências', 'REB': 'Rebotes'}
    # Mapeamento dos features para nomes em português
    features_mapping = {'MIN': 'Minutos', 'FGA': 'Arremessos Tentados', 'TOV': 'Turnovers'}

    for season in seasons:
        print(f"\nProcessando dados para a temporada {season} dos Brooklyn Nets...")

        # Obtém os dados para a temporada
        try:
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                season_type_all_star='Regular Season',
                team_id_nullable=team_id
            )
            df = stats.get_data_frames()[0]
        except Exception as e:
            print(f"Erro ao obter os dados da API para a temporada {season}: {e}")
            continue

        # Filtra para os jogadores desejados
        df = df[df['PLAYER_ID'].isin(desired_player_ids)]
        if df.empty:
            print(f"Nenhum dado encontrado para os jogadores desejados na temporada {season}.")
            continue

        # Converte colunas relevantes para numérico
        for col in ['MIN', 'FGA', 'TOV', 'PTS', 'AST', 'REB']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        for target in targets:
            print(f"\nGerando gráficos para o target: {target} na temporada {season}")
            # Seleciona as colunas necessárias
            data = df[['PLAYER_ID', 'PLAYER_NAME'] + features + [target]].dropna()
            if data.empty:
                print(f"Sem dados para o target {target} na temporada {season}.")
                continue

            # Define o threshold como a média do target
            threshold = data[target].mean()

            # Se houver amostras suficientes, usa train_test_split; senão, LOOCV
            if len(data) >= 4:
                train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)
                X_train = train_data[features]
                y_train = train_data[target]
                X_test  = test_data[features]
                y_test  = test_data[target]
                lr = LinearRegression()
                lr.fit(X_train, y_train)
                y_pred = lr.predict(X_test)
                eval_df = test_data.copy()
                eval_df['Predito'] = y_pred
            else:
                loo = LeaveOneOut()
                predictions = []
                y_true_list = []
                y_pred_list = []
                for train_idx, test_idx in loo.split(data):
                    train_data = data.iloc[train_idx]
                    test_data = data.iloc[test_idx]
                    X_train = train_data[features]
                    y_train = train_data[target]
                    X_test  = test_data[features]
                    y_test  = test_data[target]
                    lr = LinearRegression()
                    lr.fit(X_train, y_train)
                    pred = lr.predict(X_test)[0]
                    y_true_list.append(y_test.values[0])
                    y_pred_list.append(pred)
                    temp_df = test_data.copy()
                    temp_df['Predito'] = pred
                    predictions.append(temp_df)
                eval_df = pd.concat(predictions, ignore_index=True)
                y_pred = np.array(y_pred_list)

            # Define classificação binária: 1 se valor > threshold, 0 caso contrário
            eval_df['Real Acima'] = (eval_df[target] > threshold).astype(int)
            eval_df['Predito Acima'] = (eval_df['Predito'] > threshold).astype(int)
            # Calcula "probabilidade predita" via sigmoide
            eval_df['Probabilidade Predita'] = sigmoid(eval_df['Predito'] - threshold)

            # Salva a tabela de avaliação (CSV e HTML)
            table_cols = ['PLAYER_ID', 'PLAYER_NAME'] + features + [target, 'Predito', 'Probabilidade Predita', 'Real Acima', 'Predito Acima']
            table_df = eval_df[table_cols].copy()
            rename_map = {
                'PLAYER_ID': 'ID Jogador',
                'PLAYER_NAME': 'Nome do Jogador',
                'MIN': 'Minutos',
                'FGA': 'Arremessos Tentados',
                'TOV': 'Turnovers',
                target: target_mapping[target],
                'Predito': 'Predito',
                'Probabilidade Predita': 'Probabilidade Predita',
                'Real Acima': 'Real Acima da Média',
                'Predito Acima': 'Predito Acima da Média'
            }
            table_df.rename(columns=rename_map, inplace=True)
            season_tag = season.replace("-", "_")
            csv_filename  = os.path.join(output_dir, f"rf4_regressao_{target}_{season_tag}.csv")
            html_filename = os.path.join(html_dir, f"rf4_regressao_{target}_{season_tag}.html")
            table_df.to_csv(csv_filename, index=False)
            table_df.to_html(html_filename, index=False)
            print(f"Tabela de avaliação salva para {target_mapping[target]} na temporada {season}.")

            # --- Geração dos Gráficos ---
            # 1. Matriz de Confusão
            cm = confusion_matrix(eval_df['Real Acima'], eval_df['Predito Acima'])
            plt.figure(figsize=(6,5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=["Predito: Não", "Predito: Sim"],
                        yticklabels=["Real: Não", "Real: Sim"])
            plt.title(f"Matriz de Confusão - {target_mapping[target]} ({season})")
            plt.xlabel("Previsão")
            plt.ylabel("Real")
            cm_filename = os.path.join(img_dir, f"rf4_confusao_{target}_{season_tag}.jpg")
            plt.tight_layout()
            plt.savefig(cm_filename)
            plt.close()
            print(f"Gráfico da Matriz de Confusão salvo: {cm_filename}")

            # 2. Curva ROC
            fpr, tpr, _ = roc_curve(eval_df['Real Acima'], eval_df['Probabilidade Predita'])
            roc_auc = auc(fpr, tpr)
            plt.figure(figsize=(6,5))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f"ROC (AUC = {roc_auc:.2f})")
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0, 1])
            plt.ylim([0, 1.05])
            plt.xlabel("Taxa de Falso Positivo")
            plt.ylabel("Taxa de Verdadeiro Positivo")
            plt.title(f"Curva ROC - {target_mapping[target]} ({season})")
            plt.legend(loc="lower right")
            roc_filename = os.path.join(img_dir, f"rf4_roc_{target}_{season_tag}.jpg")
            plt.tight_layout()
            plt.savefig(roc_filename)
            plt.close()
            print(f"Gráfico da Curva ROC salvo: {roc_filename}")

            # 3. Gráfico de Coeficientes do Modelo
            X_full = data[features]
            y_full = data[target]
            lr_full = LinearRegression()
            lr_full.fit(X_full, y_full)
            coef_df = pd.DataFrame({
                'Variável': features,
                'Coeficiente': lr_full.coef_
            })
            coef_df['Variável'] = coef_df['Variável'].map(features_mapping)
            plt.figure(figsize=(6,5))
            ax = sns.barplot(x="Coeficiente", y="Variável", data=coef_df,
                             hue="Variável",
                             palette=sns.color_palette("viridis", n_colors=len(coef_df)),
                             dodge=False)
            leg = ax.get_legend()
            if leg is not None:
                leg.remove()
            plt.title(f"Coeficientes do Modelo - {target_mapping[target]} ({season})")
            coef_filename = os.path.join(img_dir, f"rf4_coef_{target}_{season_tag}.jpg")
            plt.tight_layout()
            plt.savefig(coef_filename)
            plt.close()
            print(f"Gráfico de Coeficientes salvo: {coef_filename}")

            # 4. Gráfico de Previsões Individuais (com anotação do jogador)
            plt.figure(figsize=(6,5))
            sns.scatterplot(x=eval_df[target], y=eval_df['Predito'], hue=eval_df['PLAYER_NAME'], s=100, legend=False)
            # Anota cada ponto com o nome do jogador
            for _, row in eval_df.iterrows():
                plt.text(row[target], row['Predito'], row['PLAYER_NAME'], fontsize=9, ha='right')
            plt.xlabel(f"Valor Real de {target_mapping[target]}")
            plt.ylabel(f"Valor Predito de {target_mapping[target]}")
            plt.title(f"Previsões Individuais - {target_mapping[target]} ({season})")
            individual_filename = os.path.join(img_dir, f"rf4_individual_{target}_{season_tag}.jpg")
            plt.tight_layout()
            plt.savefig(individual_filename)
            plt.close()
            print(f"Gráfico de Previsões Individuais salvo: {individual_filename}")

            # --- Geração do HTML Completo (com a tabela e todos os gráficos) ---
            rel_img_path = "../../imagens/parte3"
            html_complete = f"""
            <html>
              <head>
                <meta charset="utf-8">
                <title>Resultados de Regressão - {target_mapping[target]} ({season})</title>
              </head>
              <body>
                <h1>Resultados de Regressão - {target_mapping[target]} - Temporada {season}</h1>
                <h2>Tabela de Avaliação</h2>
                {table_df.to_html(index=False)}
                <h2>Matriz de Confusão</h2>
                <img src="{rel_img_path}/rf4_confusao_{target}_{season_tag}.jpg" alt="Matriz de Confusão">
                <h2>Curva ROC</h2>
                <img src="{rel_img_path}/rf4_roc_{target}_{season_tag}.jpg" alt="Curva ROC">
                <h2>Coeficientes do Modelo</h2>
                <img src="{rel_img_path}/rf4_coef_{target}_{season_tag}.jpg" alt="Coeficientes do Modelo">
                <h2>Previsões Individuais</h2>
                <img src="{rel_img_path}/rf4_individual_{target}_{season_tag}.jpg" alt="Previsões Individuais">
              </body>
            </html>
            """
            html_complete_filename = os.path.join(html_dir, f"rf4_regressao_{target}_{season_tag}_completo.html")
            with open(html_complete_filename, "w", encoding="utf-8") as f:
                f.write(html_complete)
            print(f"HTML completo com gráficos salvo: {html_complete_filename}")

    print("\nGeração dos gráficos de regressão linear finalizada para todas as temporadas desejadas!")
    print("Processamento concluído.")
