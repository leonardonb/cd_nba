import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from nba_api.stats.endpoints import leaguedashplayerstats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, confusion_matrix, roc_curve
from sklearn.model_selection import train_test_split

def analisar_regressao_logistica_graficos():
    players = [
        {"PLAYER": "Cam Thomas", "PLAYER_ID": 1630560},
        {"PLAYER": "Cameron Johnson", "PLAYER_ID": 1629661},
        {"PLAYER": "D'Angelo Russell", "PLAYER_ID": 1626156},
    ]

    output_dir = "reports/arquivos_csv/parte3/parte3-rf5-rf6"
    html_dir = "reports/html/parte3/parte3-rf5-rf6"
    img_dir = "reports/imagens/parte3/parte3-rf5-rf6"

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # Parâmetros fixos
    team_id = 1610612751  # Brooklyn Nets
    seasons = ["2023-24", "2024-25"]
    features = ["MIN", "FGA", "TOV"]
    targets = ["PTS", "AST", "REB"]

    target_mapping = {"PTS": "Pontos", "AST": "Assistências", "REB": "Rebotes"}

    for season in seasons:
        print(f"\nProcessando dados para a temporada {season} dos Brooklyn Nets...")

        try:
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season, season_type_all_star="Regular Season", team_id_nullable=team_id
            )
            df = stats.get_data_frames()[0]
        except Exception as e:
            print(f"Erro ao obter os dados da API para a temporada {season}: {e}")
            continue

        if df.empty:
            print(f"Nenhum dado encontrado para o Brooklyn Nets na temporada {season}.")
            continue

        # Converter para numérico
        for col in features + targets:
            df[col] = pd.to_numeric(df[col], errors="coerce")


        for target in targets:
            print(f"\nProcessando o target: {target} para a temporada {season}")
            data = df[["PLAYER_ID", "PLAYER_NAME"] + features + [target]].dropna()

            if data.empty:
                print(f"Atenção: Nenhum dado válido para {target} na temporada {season}. Pulando esta análise.")
                continue

            median_val = data[target].median()
            data["target_class"] = (data[target] > median_val).astype(int)

            if len(data["target_class"].unique()) < 2 or data["target_class"].value_counts().min() < 2:
                print(f"Atenção: O target {target} para a temporada {season} não possui exemplos suficientes em ambas as classes. Pulando esta análise.")
                continue

            X_train, X_test, y_train, y_test = train_test_split(
                data[features], data["target_class"], test_size=0.3, random_state=42, stratify=data["target_class"]
            )

            model = LogisticRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            conf_matrix = confusion_matrix(y_test, y_pred)

            test_data = X_test.copy()
            test_data["Real"] = y_test.values
            test_data["Predito"] = y_pred

            for player in players:
                if player["PLAYER_ID"] not in data["PLAYER_ID"].values:
                    print(f"Jogador {player['PLAYER']} não encontrado na base, adicionando com valores NaN.")
                    new_row = pd.Series(
                        {**{col: np.nan for col in features}, "Real": np.nan, "Predito": np.nan}
                    )
                    test_data = pd.concat([test_data, pd.DataFrame([new_row])], ignore_index=True)

            rename_map = {
                "PLAYER_ID": "ID Jogador",
                "PLAYER_NAME": "Nome do Jogador",
                "MIN": "Minutos",
                "FGA": "Arremessos Tentados",
                "TOV": "Turnovers",
                target: target_mapping[target],
                "Predito": "Predito",
                "Real": "Real",
            }
            test_data.rename(columns=rename_map, inplace=True)

            season_tag = season.replace("-", "_")
            csv_filename = os.path.join(output_dir, f"rf5_logistic_regression_{target}_{season_tag}.csv")
            html_filename = os.path.join(html_dir, f"rf5_logistic_regression_{target}_{season_tag}.html")
            img_filename = os.path.join(img_dir, f"rf5_logistic_regression_{target}_{season_tag}.jpg")

            test_data.to_csv(csv_filename, index=False)
            print(f"Arquivo CSV salvo em: {csv_filename}")
            test_data.to_html(html_filename, index=False)
            print(f"Arquivo HTML salvo em: {html_filename}")

            # Gráfico da Matriz de Confusão
            plt.figure(figsize=(8, 6))
            sns.heatmap(
                conf_matrix,
                annot=True,
                fmt="d",
                cmap="Blues",
                xticklabels=["Abaixo Mediana", "Acima Mediana"],
                yticklabels=["Abaixo Mediana", "Acima Mediana"],
            )
            plt.xlabel("Predito")
            plt.ylabel("Real")
            plt.title(f"Matriz de Confusão para {target_mapping[target]} - Temporada {season}")
            plt.savefig(img_filename)
            plt.close()
            print(f"Gráfico da Matriz de Confusão salvo em: {img_filename}")

            y_prob = model.predict_proba(X_test)[:, 1]  # Probabilidade da classe positiva (Acima Mediana)

            # Calcular a curva ROC
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)

            # Gerar a curva ROC
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, color='blue', lw=2, label=f'Curva ROC (AUC = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('Taxa de Falsos Positivos (FPR)')
            plt.ylabel('Taxa de Verdadeiros Positivos (TPR)')
            plt.title(f'Curva ROC para {target_mapping[target]} - Temporada {season}')
            plt.legend(loc='lower right')
            
            # Salvar o gráfico como imagem
            img_filename_roc = os.path.join(img_dir, f"rf5_logistic_regression_{target}_{season_tag}_roc.jpg")
            plt.savefig(img_filename_roc)
            plt.close()
            print(f"Gráfico de Curva ROC salvo em: {img_filename_roc}")


        print(f"\nProcessamento finalizado para a temporada {season}.")

    print("Processamento concluído.")