from pygam import PoissonGAM

def aplicar_gamlss(X, y):
    model = PoissonGAM().fit(X, y)
    return model
