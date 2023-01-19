import numpy as np
import pandas as pd


class acp():
    def __init__(self, t, variabile=None):
        assert isinstance(t, pd.DataFrame)
        if variabile is None:
            self.variabile = list(t)
        else:
            self.variabile = variabile
        self.__x = t[self.variabile].values

    def fit(self, std=True, nlib=0, procent_minimal=80):
        n, m = self.__x.shape
        x_ = self.__x - np.mean(self.__x, axis=0)
        if std:
            x_ = x_ / np.std(self.__x, axis=0)
        r_v = (1 / (n - nlib)) * x_.T @ x_
        valp, vecp = np.linalg.eig(r_v)
        k = np.flip(np.argsort(valp))
        self.__alpha = valp[k]
        self.__a = vecp[:, k]
        self.__c = x_ @ self.__a
        # Criteriul acoperirii minimale
        k1 = np.where(np.cumsum(self.alpha) * 100 / sum(self.__alpha) > procent_minimal)[0][0]
        # Criteriul Kaiser
        if std:
            k2 = np.where(self.__alpha < 1)[0][0] - 1
        else:
            k2 = None
        # Criteriul Cattell
        eps = self.__alpha[:(m - 1)] - self.__alpha[1:]
        sigma = eps[:(m - 2)] - eps[1:]
        sunt_negative = sigma < 0
        if any(sunt_negative):
            k3 = np.where(sunt_negative)[0][0] + 1
        else:
            k3 = None
        self.__criterii = (k1, k2, k3)
        # Calcul corelatii factoriale
        if std:
            self.__r = self.__a * np.sqrt(self.__alpha)
        else:
            self.__r = np.corrcoef(x_, self.__c, rowvar=False)[:m, m:]

    @property
    def alpha(self):
        return self.__alpha

    @property
    def criterii(self):
        return self.__criterii

    @property
    def c(self):
        return self.__c

    @property
    def r(self):
        return self.__r

    @property
    def a(self):
        return self.__a
