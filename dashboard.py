import streamlit as st
import pandas as pd
import os
from src.rf.parte1.parte1_rf2 import apresentar_classificacao_atual
from src.rf.parte1.parte1_rf8 import rf_graficos_desempenho_brooklyn_nets
from src.rf.parte2.parte2_rf5 import calcular_e_apresentar_medias
from src.rf.parte2.parte2_rf6 import calcular_e_apresentar_medianas
from src.rf.parte2.parte2_rf7 import calcular_e_apresentar_modas
from src.rf.parte2.parte2_rf8 import calcular_e_apresentar_desvios

# Configuração da página
st.set_page_config(page_title="NBA Dashboard", layout="wide")

st.title("NBA Dashboard 📊")
st.sidebar.header("Opções de Visualização")

# Opção de menu
menu = st.sidebar.radio("Selecione uma análise:", [
    "Classificação Geral",
    "Desempenho do Brooklyn Nets",
    "Estatísticas dos Jogadores",
    "Análise Individual de Jogadores"
])

if menu == "Classificação Geral":
    st.subheader("Classificação Atual da NBA")

    # Caminho do CSV gerado
    csv_path = "reports/arquivos_csv/parte1/rf2_classificacao_unificada.csv"

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.dataframe(df)
    else:
        st.error("Erro ao carregar a classificação. O arquivo CSV não foi encontrado.")

elif menu == "Desempenho do Brooklyn Nets":
    st.subheader("Desempenho do Brooklyn Nets")

    img_dir = "reports/imagens/parte1/"
    img_files = [
        "rf8_barras_empilhado_vitorias_derrotas.jpg",
        "rf8_pizza_vitorias_derrotas_2023-24.jpg",
        "rf8_pizza_vitorias_derrotas_2024-25.jpg",
        "rf8_radar_fora_media.jpg",
        "rf8_radar_casa_media.jpg",
        "rf8_linha_seq_2023-24.jpg",
        "rf8_linha_seq_2024-25.jpg",
        "rf8_scatter_media_pontos.jpg"
    ]

    found = False
    for img in img_files:
        img_path = os.path.join(img_dir, img)
        if os.path.exists(img_path):
            st.image(img_path, caption=img)
            found = True

    if not found:
        st.error("Nenhuma imagem encontrada. Certifique-se de que os relatórios foram gerados corretamente.")

elif menu == "Estatísticas dos Jogadores":
    st.subheader("Estatísticas dos Jogadores")

    possible_paths = [
        "data/jogadores.csv",
        "reports/arquivos_csv/parte2/p2_rft1_dados_jogadores.csv"
    ]

    players_csv_path = next((path for path in possible_paths if os.path.exists(path)), None)

    if players_csv_path:
        players_df = pd.read_csv(players_csv_path)
        players = players_df.to_dict(orient="records")
    else:
        st.error("Arquivo de jogadores não encontrado. Verifique os diretórios 'data/' ou 'reports/arquivos_csv/'.")
        players = []

    if players:
        st.dataframe(pd.DataFrame(players))
    else:
        st.warning("Nenhum jogador encontrado.")

elif menu == "Análise Individual de Jogadores":
    st.subheader("Análise Individual de Jogadores")

    player_files = [f for f in os.listdir("data/processed/") if f.endswith(".csv")]
    player_names = [f.replace(".csv", "") for f in player_files]

    selected_player = st.selectbox("Selecione um jogador:", player_names)

    if selected_player:
        player_data_path = os.path.join("data/processed/", selected_player + ".csv")
        if os.path.exists(player_data_path):
            player_df = pd.read_csv(player_data_path)
            st.dataframe(player_df)
        else:
            st.error("Dados do jogador não encontrados.")

st.sidebar.write("Desenvolvido por você 🚀")