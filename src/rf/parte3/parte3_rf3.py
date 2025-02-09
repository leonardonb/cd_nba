# src/rf/parte3/parte3_rf3.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from nba_api.stats.endpoints import leaguedashplayerstats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def analisar_regressao_linear():

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
    target_mapping = {'PTS': 'Pontos', 'AST': 'Assistencias', 'REB': 'Rebotes'}

    for season in seasons:
        print(f"\nProcessando dados para a temporada {season} dos Brooklyn Nets...")

        # Obtém os dados para a temporada atual
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

        # Filtra os dados apenas para os jogadores desejados
        df = df[df['PLAYER_ID'].isin(desired_player_ids)]
        if df.empty:
            print(f"Nenhum dado encontrado para os jogadores desejados na temporada {season}.")
            continue

        # Converte as colunas relevantes para o formato numérico
        for col in ['MIN', 'FGA', 'TOV', 'PTS', 'AST', 'REB']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        print("Dados filtrados (exibindo as 5 primeiras linhas):")
        print(df[['PLAYER_ID', 'PLAYER_NAME', 'MIN', 'FGA', 'TOV', 'PTS', 'AST', 'REB']].head())

        # Processa cada variável dependente (target)
        for target in targets:
            print(f"\nProcessando o target: {target} para a temporada {season}")
            data = df[['PLAYER_ID', 'PLAYER_NAME'] + features + [target]].dropna()

            # Se a amostra for muito pequena (menos de 4), utiliza LOOCV para evitar warnings do R²
            if len(data) < 4:
                from sklearn.model_selection import LeaveOneOut
                loo = LeaveOneOut()
                y_true_list = []
                y_pred_list = []
                predicted_dfs = []

                for train_index, test_index in loo.split(data):
                    train_data = data.iloc[train_index]
                    test_data = data.iloc[test_index]
                    X_train = train_data[features]
                    y_train = train_data[target]
                    X_test  = test_data[features]
                    y_test  = test_data[target]

                    # Calcula os thresholds a partir do conjunto de treinamento
                    mean_val   = y_train.mean()
                    median_val = y_train.median()
                    mode_series = y_train.mode()
                    mode_val   = mode_series.iloc[0] if not mode_series.empty else np.nan
                    max_val    = y_train.max()
                    min_val    = y_train.min()

                    lr = LinearRegression()
                    lr.fit(X_train, y_train)
                    y_pred_val = lr.predict(X_test)[0]

                    y_true_list.append(y_test.values[0])
                    y_pred_list.append(y_pred_val)

                    temp_df = test_data.copy()
                    temp_df['Predicted'] = y_pred_val
                    temp_df['above_mean'] = int(y_pred_val > mean_val)
                    temp_df['above_median'] = int(y_pred_val > median_val)
                    temp_df['above_mode'] = int(y_pred_val > mode_val)
                    temp_df['above_max'] = int(y_pred_val > max_val)
                    temp_df['above_min'] = int(y_pred_val > min_val)
                    predicted_dfs.append(temp_df)

                result_df = pd.concat(predicted_dfs, ignore_index=True)
                # Seleciona explicitamente as colunas desejadas (incluindo os features)
                result_df = result_df[['PLAYER_ID', 'PLAYER_NAME'] + features + [target, 'Predicted',
                                                                                 'above_mean', 'above_median',
                                                                                 'above_mode', 'above_max',
                                                                                 'above_min']]
                r2  = r2_score(y_true_list, y_pred_list)
                mse = mean_squared_error(y_true_list, y_pred_list)
            else:
                # Utiliza a divisão padrão (treino/teste) se houver amostras suficientes
                from sklearn.model_selection import train_test_split
                train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)
                X_train = train_data[features]
                y_train = train_data[target]
                X_test  = test_data[features]
                y_test  = test_data[target]

                mean_val   = y_train.mean()
                median_val = y_train.median()
                mode_series = y_train.mode()
                mode_val   = mode_series.iloc[0] if not mode_series.empty else np.nan
                max_val    = y_train.max()
                min_val    = y_train.min()

                lr = LinearRegression()
                lr.fit(X_train, y_train)
                y_pred = lr.predict(X_test)
                r2  = r2_score(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)

                test_data = test_data.copy()
                test_data['Predicted'] = y_pred
                test_data['above_mean'] = (y_pred > mean_val).astype(int)
                test_data['above_median'] = (y_pred > median_val).astype(int)
                test_data['above_mode'] = (y_pred > mode_val).astype(int)
                test_data['above_max'] = (y_pred > max_val).astype(int)
                test_data['above_min'] = (y_pred > min_val).astype(int)
                # Seleciona explicitamente as colunas desejadas (incluindo os features)
                result_df = test_data[['PLAYER_ID', 'PLAYER_NAME'] + features + [target, 'Predicted',
                                                                                 'above_mean', 'above_median',
                                                                                 'above_mode', 'above_max',
                                                                                 'above_min']]

            print(f"Thresholds para {target}: Média={mean_val:.2f}, Mediana={median_val:.2f}, "
                  f"Moda={mode_val:.2f}, Máximo={max_val:.2f}, Mínimo={min_val:.2f}")
            print(f"Desempenho do modelo para {target}: R2={r2:.2f}, MSE={mse:.2f}")

            # Renomeia as colunas para nomes em português
            rename_map = {
                'PLAYER_ID': 'ID Jogador',
                'PLAYER_NAME': 'Nome do Jogador',
                'MIN': 'Minutos',
                'FGA': 'Arremessos Tentados',
                'TOV': 'Turnovers',
                target: target_mapping[target],
                'Predicted': 'Predito',
                'above_mean': 'Acima da Media',
                'above_median': 'Acima da Mediana',
                'above_mode': 'Acima da Moda',
                'above_max': 'Acima do Maximo',
                'above_min': 'Acima do Minimo'
            }
            result_df.rename(columns=rename_map, inplace=True)

            # Define um identificador para a temporada (ex.: "2023_24")
            season_tag = season.replace("-", "_")

            # Define os nomes dos arquivos de saída com o prefixo rf3_
            csv_filename  = os.path.join(output_dir, f"rf3_linear_regression_{target}_{season_tag}.csv")
            html_filename = os.path.join(html_dir, f"rf3_linear_regression_{target}_{season_tag}.html")
            img_filename  = os.path.join(img_dir, f"rf3_linear_regression_{target}_{season_tag}.jpg")

            # Salva os resultados em CSV e HTML
            result_df.to_csv(csv_filename, index=False)
            print(f"Arquivo CSV salvo em: {csv_filename}")
            result_df.to_html(html_filename, index=False)
            print(f"Arquivo HTML salvo em: {html_filename}")

            # Gera e salva o gráfico comparando os valores reais e preditos com rótulos em português
            target_label = target_mapping[target]
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=result_df[target_label], y=result_df['Predito'], s=100)
            plt.plot([result_df[target_label].min(), result_df[target_label].max()],
                     [result_df[target_label].min(), result_df[target_label].max()],
                     color='red', linestyle='--', label='Linha ideal (y=x)')
            plt.xlabel(f"Valor Real de {target_label}")
            plt.ylabel(f"Valor Predito de {target_label}")
            plt.title(f"Regressão Linear para {target_label} - Temporada {season}\nR2={r2:.2f}, MSE={mse:.2f}")
            plt.legend()
            plt.tight_layout()
            plt.savefig(img_filename)
            plt.close()
            print(f"Gráfico JPG salvo em: {img_filename}")

        print(f"\nProcessamento finalizado para a temporada {season}.")

    print("\nAnálise de regressão linear finalizada para todas as temporadas desejadas!")
    print("Processamento concluído.")
