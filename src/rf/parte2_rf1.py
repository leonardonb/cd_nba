from bs4 import BeautifulSoup
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import requests

def calculate_age(birthdate):
    """
    Calcula a idade a partir da data de nascimento.
    """
    try:
        birthdate = birthdate.split("T")[0] if "T" in birthdate else birthdate
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    except Exception as e:
        print(f"Erro ao calcular idade: {e}")
        return "N/A"


def fetch_player_salary(player_name): 
    """ 
    Busca o salário do jogador no site HoopsHype. 
    """ 
    url = 'https://hoopshype.com/salaries/players/' 
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser') 

    table = soup.find('table', {'class': 'hh-salaries-ranking-table'}) 
    rows = table.find_all('tr')
    
    for row in rows[1:]:
        cols = row.find_all('td') 
        name = cols[1].text.strip() 
        if player_name.lower() in name.lower(): 
            salary = row.find('td', {'class': 'hh-salaries-sorted'}).text.strip()
            return salary 
        
    return "N/A"

def apresentar_dados_jogadores(player_names, output_dir, html_dir, img_dir):
    """
    P2-RF1: Apresentar dados dos jogadores especificados por nome.

    Args:
        player_names (list): Lista de nomes completos dos jogadores.
        output_dir (str): Diretório para salvar os relatórios em CSV.
        html_dir (str): Diretório para salvar os relatórios em HTML.
        img_dir (str): Diretório para salvar os relatórios como imagens.
    """
    all_players = players.get_players()
    player_data_list = []

    # Criar diretórios para salvar os resultados
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for player_name in player_names:
        # Buscar jogador pelo nome (case-insensitive)
        player = next((p for p in all_players if p['full_name'].lower() == player_name.lower()), None)
        if not player:
            print(f"Jogador não encontrado: {player_name}")
            continue

        # Obter detalhes do jogador
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id']).get_dict()
            player_data = player_info['resultSets'][0]['rowSet'][0]

            # Dados do jogador
            id = player_data[0]
            name = player_data[3]
            height = player_data[11]
            weight = player_data[12]
            birthdate = player_data[7]
            age = calculate_age(birthdate)  # Calcular idade
            experience = int(player_data[13]) if player_data[13] != 'R' else 0  # Experiência
            position = player_data[15]
            college = player_data[8]
            salary = fetch_player_salary(name)  # Salário

            player_data_list.append({
                "ID": id,
                "Nome": name,
                "Altura": height,
                "Peso": weight,
                "Idade": age,
                "Experiência": experience,
                "Posição": position,
                "Universidade": college,
                "Salário": salary
            })
        except Exception as e:
            print(f"Erro ao obter dados do jogador {player_name}: {e}")

    # Criar DataFrame
    df_players = pd.DataFrame(player_data_list)

    if df_players.empty:
        print("Nenhum dado válido encontrado para os jogadores especificados.")
        return

    # Salvar em CSV
    csv_path = os.path.join(output_dir, "p2_rft1_dados_jogadores.csv")
    df_players.to_csv(csv_path, index=False)
    print(f"Tabela CSV salva em: {csv_path}")

    # Salvar em HTML
    html_path = os.path.join(html_dir, "p2_rft1_dados_jogadores.html")
    df_players.to_html(html_path, index=False)
    print(f"Tabela HTML salva em: {html_path}")

    # Salvar como imagem
    img_path = os.path.join(img_dir, "p2_rft1_dados_jogadores.jpg")
    salvar_tabela_como_imagem(df_players, img_path, "Dados dos Jogadores")

    print('Processamento da Parte2-RF1 concluído.')
    return df_players


def salvar_tabela_como_imagem(df, img_path, title):
    if df.empty:
        print("DataFrame vazio. Não é possível salvar como imagem.")
        return

    fig, ax = plt.subplots(figsize=(12, len(df) * 0.6))
    ax.axis("off")
    ax.axis("tight")
    ax.set_title(title, fontsize=16, weight="bold")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(img_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Tabela salva como imagem em: {img_path}")
