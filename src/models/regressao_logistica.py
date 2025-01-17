from sklearn.linear_model import LogisticRegression

def regressao_logistica(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    return model
