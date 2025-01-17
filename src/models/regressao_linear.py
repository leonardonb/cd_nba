from sklearn.linear_model import LinearRegression

def aplicar_regressao(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model
