from src.data.coleta_dados import coletar_dados

def main():
    player_id = 2544  # ID de LeBron James (exemplo)
    season = '2024-25'

    try:
        dados = coletar_dados(player_id=player_id, season=season)
        if not dados.empty:
            print("Dados coletados com sucesso:")
            print(dados.head())
        else:
            print("Nenhum dado foi retornado. Verifique o ID do jogador ou a temporada.")
    except Exception as e:
        print(f"Erro ao coletar os dados: {e}")

if __name__ == "__main__":
    main()


