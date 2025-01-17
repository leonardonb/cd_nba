from src.models.regressao_linear import aplicar_regressao


def test_regressao_linear():
    X = [[1], [2], [3]]
    y = [2, 4, 6]
    model = aplicar_regressao(X, y)
    assert model.coef_[0] == 2
