import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from pandas.plotting import table
import matplotlib.pyplot as plt

def coletar_jogos_basketball_reference(team_abbr, year):
    """
    Coleta os jogos de uma equipe para uma temporada no Basketball Reference.

    Args:
        team_abbr (str): Abreviação do time (ex.: 'BRK' para Brooklyn Nets).
        year (int): Ano da temporada (ex.: 2024 para a temporada 2023-24).

    Returns:
        pd.DataFrame: DataFrame contendo os jogos da temporada.
    """
    url = f"https://www.basketball-reference.com/teams/{team_abbr}/{year}_games.html"
    print(f"Coletando dados da URL: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Falha ao acessar a página: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'games'})

    # Extraindo cabeçalhos da tabela
    headers = [th.text.strip() if th.text.strip() else f"Unnamed_{i}" \
               for i, th in enumerate(table.find('thead').find_all('th'))][1:]  # Ignorar índice
    print(f"Colunas encontradas: {headers}")

    # Extraindo linhas da tabela
    rows = []
    for row in table.find('tbody').find_all('tr'):
        if 'class' in row.attrs and 'thead' in row['class']:  # Ignorar separadores de meses
            continue
        cols = [col.text.strip() for col in row.find_all('td')]
        if cols:  # Ignorar linhas vazias
            rows.append(cols)

    # Criar DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Renomear colunas para nomes significativos
    df.rename(columns={'Tm': 'PTS', 'Opp': 'PTS_Opp', 'Opponent': 'Adversário', 'Unnamed_5': 'Local'}, inplace=True)

    # Adicionar coluna indicando se o jogo foi em casa ou fora
    df['Casa/Fora'] = df['Local'].apply(lambda x: 'Fora' if '@' in x else 'Casa')

    # Criar a coluna duplicada Casa/Fora_id
    df['Casa/Fora_id'] = df['Casa/Fora'].apply(lambda x: 1 if x == 'Fora' else 0)

    # Selecionar apenas as colunas desejadas
    df = df[['Date', 'Adversário', 'PTS', 'PTS_Opp', 'W', 'L', 'Streak', 'Casa/Fora', 'Casa/Fora_id']]

    return df

def salvar_tabela_em_paginas_jpg(df, img_dir, file_prefix):
    """
    Salva a tabela em múltiplas imagens JPEG, caso os dados não caibam em uma única imagem.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados.
        img_dir (str): Diretório para salvar as imagens.
        file_prefix (str): Prefixo para os nomes dos arquivos de imagem.
    """
    rows_per_page = 20  # Número de linhas por imagem
    total_rows = len(df)
    total_pages = (total_rows // rows_per_page) + int(total_rows % rows_per_page > 0)

    for page in range(total_pages):
        start_row = page * rows_per_page
        end_row = start_row + rows_per_page
        df_page = df.iloc[start_row:end_row]

        img_path = os.path.join(img_dir, f"{file_prefix}_page_{page + 1}.jpg")
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('tight')
        ax.axis('off')
        tabela = table(ax, df_page, loc='center', colWidths=[0.1] * len(df.columns))
        tabela.auto_set_font_size(False)
        tabela.set_fontsize(10)
        tabela.scale(1.2, 1.2)
        plt.savefig(img_path, bbox_inches='tight')
        plt.close()
        print(f"Tabela salva como imagem em: {img_path}")

def apresentar_jogos_do_time(team_abbr, seasons, output_dir):
    """
    Apresenta os jogos do time e salva os dados em CSV, HTML e como imagens da tabela em JPEG.

    Args:
        team_abbr (str): Abreviação do time (ex.: 'BRK' para Brooklyn Nets).
        seasons (list): Lista de temporadas no formato 'YYYY-YY' (ex.: ['2023-24', '2024-25']).
        output_dir (str): Diretório base para salvar os arquivos.

    Returns:
        pd.DataFrame: Dados processados do time.
    """
    dados_completos = pd.DataFrame()

    for season in seasons:
        # Extrair o ano inicial da temporada
        year_start = int(season.split('-')[0])
        print(f"Coletando jogos para a temporada {year_start}-{year_start + 1}...")
        dados = coletar_jogos_basketball_reference(team_abbr, year_start + 1)
        dados_completos = pd.concat([dados_completos, dados], ignore_index=True)

    # Diretórios de saída
    csv_dir = os.path.join(output_dir, "arquivos_csv")
    html_dir = os.path.join(output_dir, "html/parte1")
    img_dir = os.path.join(output_dir, "imagens")
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # Salvar como CSV
    csv_path = os.path.join(csv_dir, "rf7_jogos_do_time.csv")
    dados_completos.to_csv(csv_path, index=False)
    print(f"Dados salvos como CSV em: {csv_path}")

    # Salvar como HTML
    html_path = os.path.join(html_dir, "rf7_jogos_do_time.html")
    dados_completos.to_html(html_path, index=False)
    print(f"Dados salvos como HTML em: {html_path}")

    # Salvar como múltiplas imagens (JPEG) da tabela
    salvar_tabela_em_paginas_jpg(dados_completos, img_dir, "rf7_jogos_do_time")

    return dados_completos

# Exemplo de uso
if __name__ == "__main__":
    team_abbr = "BRK"  # Abreviação do Brooklyn Nets
    seasons = ["2023-24", "2024-25"]  # Temporadas no formato 'YYYY-YY'
    output_dir = "reports"

    dados = apresentar_jogos_do_time(team_abbr, seasons, output_dir)
    print(dados.head())