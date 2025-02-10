import scipy.sparse
if not hasattr(scipy.sparse.csr_matrix, 'A'):
    scipy.sparse.csr_matrix.A = property(lambda self: self.toarray())

# Patch para evitar o erro de deprecated do np.int (se necessário)
import numpy as np
np.int = int

import os
import pandas as pd
import matplotlib.pyplot as plt
from pygam import PoissonGAM, LinearGAM, s
from scipy.stats import poisson, norm, mode
from nba_api.stats.endpoints import playergamelog
import time

def gamlss_brooklyn_nets():

    print("Executando RF7: Fazendo previsão através de GAMLSS...")

    # Configura diretórios de saída para as tabelas e imagens
    csv_dir = 'reports/arquivos_csv/parte3'
    html_dir = 'reports/html/parte3'
    img_dir = 'reports/imagens/parte3'
    for d in [csv_dir, html_dir, img_dir]:
        os.makedirs(d, exist_ok=True)

    # Definir os jogadores e seus IDs (Brooklyn Nets)
    players = {
        1630560: 'Cam Thomas',
        1629661: 'Cameron Johnson',
        1626156: "D'Angelo Russell"
    }

    # Buscar dados reais através da API nba_api para as temporadas desejadas
    seasons = ["2023-24", "2024-25"]
    data_list = []
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
                # Filtrar jogos dos Brooklyn Nets usando a coluna "MATCHUP"
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

    def process_prediction(player_data, stat, player_name):
        X = player_data['game'].values.reshape(-1, 1)
        y = player_data[stat].values
        next_game = player_data['game'].max() + 1

        poisson_gam = PoissonGAM(s(0))
        poisson_gam.gridsearch(X, y)
        pred_poisson = poisson_gam.predict(np.array([[next_game]]))[0]

        linear_gam = LinearGAM(s(0))
        linear_gam.gridsearch(X, y)
        pred_linear = linear_gam.predict(np.array([[next_game]]))[0]
        residuals = y - linear_gam.predict(X)
        sigma = np.std(residuals)
        if sigma == 0:
            sigma = 1e-6

        mean_val = np.mean(y)
        median_val = np.median(y)
        mode_val = np.atleast_1d(mode(y).mode)[0]
        min_val = np.min(y)
        max_val = np.max(y)

        references = {
            'mean': mean_val,
            'median': median_val,
            'mode': mode_val,
            'min': min_val,
            'max': max_val
        }

        poisson_results = {}
        for ref_name, ref_val in references.items():
            ref_int = int(round(ref_val))
            prob_below = poisson.cdf(ref_int, pred_poisson)
            prob_above = 1 - poisson.cdf(ref_int - 1, pred_poisson)
            poisson_results[ref_name] = {
                'ref_value': ref_val,
                'prob_below': prob_below,
                'prob_above': prob_above
            }

        linear_results = {}
        for ref_name, ref_val in references.items():
            prob_below = norm.cdf(ref_val, loc=pred_linear, scale=sigma)
            prob_above = 1 - norm.cdf(ref_val, loc=pred_linear, scale=sigma)
            linear_results[ref_name] = {
                'ref_value': ref_val,
                'prob_below': prob_below,
                'prob_above': prob_above
            }

        result = {
            'player': player_name,
            'stat': stat,
            'next_game': next_game,
            'poisson_prediction': pred_poisson,
            'linear_prediction': pred_linear,
            'historical_mean': mean_val,
            'historical_median': median_val,
            'historical_mode': mode_val,
            'historical_min': min_val,
            'historical_max': max_val,
            'poisson_probs': poisson_results,
            'linear_probs': linear_results
        }
        return result

    stats = ['points', 'rebounds', 'assists']
    all_results = []
    for pid, player_name in players.items():
        player_data = data[data['player_id'] == pid]
        if player_data.empty:
            print(f"Sem dados para {player_name}.")
            continue
        for stat in stats:
            res = process_prediction(player_data, stat, player_name)
            all_results.append(res)

    if not all_results:
        print("Nenhuma previsão foi gerada.")
        return

    # Construção da tabela com títulos em português
    rows = []
    for res in all_results:
        base_info = {
            'jogador': res['player'],
            'estatistica': res['stat'],
            'proximo_jogo': res['next_game'],
            'previsao_poisson': res['poisson_prediction'],
            'previsao_linear': res['linear_prediction'],
            'media_historica': res['historical_mean'],
            'mediana_historica': res['historical_median'],
            'moda_historica': res['historical_mode'],
            'minimo_historico': res['historical_min'],
            'maximo_historico': res['historical_max']
        }
        for ref in res['poisson_probs']:
            base_info[f'probabilidade_abaixo_{ref}_poisson'] = res['poisson_probs'][ref]['prob_below']
            base_info[f'probabilidade_acima_{ref}_poisson'] = res['poisson_probs'][ref]['prob_above']
        for ref in res['linear_probs']:
            base_info[f'probabilidade_abaixo_{ref}_linear'] = res['linear_probs'][ref]['prob_below']
            base_info[f'probabilidade_acima_{ref}_linear'] = res['linear_probs'][ref]['prob_above']
        rows.append(base_info)

    results_df = pd.DataFrame(rows)

    csv_path = os.path.join(csv_dir, 'rf7_predictions.csv')
    results_df.to_csv(csv_path, index=False)
    print(f"Arquivo CSV salvo em: {csv_path}")

    html_path = os.path.join(html_dir, 'rf7_predictions.html')
    results_df.to_html(html_path, index=False)
    print(f"Arquivo HTML salvo em: {html_path}")

    fig, ax = plt.subplots(figsize=(max(12, results_df.shape[1] * 0.8),
                                    results_df.shape[0] * 0.5 + 2))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=results_df.values,
             colLabels=results_df.columns,
             cellLoc='center',
             loc='center')
    plt.title('Tabela de Previsões', fontsize=16)
    img_table_path = os.path.join(img_dir, 'rf7_predictions_table.jpg')
    plt.savefig(img_table_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Arquivo JPG da tabela salvo em: {img_table_path}")

    print("Processamento concluído. As tabelas foram geradas com sucesso!")