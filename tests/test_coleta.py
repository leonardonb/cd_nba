from src.data.coleta_dados import coletar_dados_jogador


def test_coletar_dados_jogador():
    data = coletar_dados_jogador(player_id=123, season="2024-25")
    assert not data.empty
