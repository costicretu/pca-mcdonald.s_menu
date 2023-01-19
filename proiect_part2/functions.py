import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
from pandas.core.dtypes.common import is_numeric_dtype


def nan_replace_t(t):
    assert isinstance(t, pd.DataFrame)
    for v in t.columns:
        if any(t[v].isna()):
            if is_numeric_dtype(t[v]):
                t[v].fillna(t[v].mean(), inplace=True)
            else:
                t[v].fillna(t[v].mode()[0], inplace=True)


def plot_varianta(alpha, criterii, eticheta_x="Componente"):
    m = len(alpha)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title("Plot varianta", fontdict={"fontsize": 16})
    ax.set_xlabel(eticheta_x)
    ax.set_ylabel("Varianta")
    x = np.arange(1, m + 1)
    ax.set_xticks(x)
    ax.plot(x, alpha)
    ax.scatter(x, alpha, color="r")
    # Acoperire minimala
    ax.axhline(alpha[criterii[0]], color="b", label="Criteriul acoperirii minimale")
    # Criteriul Kaiser
    if criterii[1] is not None:
        ax.axhline(1, color="m", label="Criteriul Kaiser")
    # Criteriul Cattell
    if criterii[2] is not None:
        ax.axhline(alpha[criterii[2]], color="g", label="Crieriul Cattell")
    ax.legend()


def show():
    plt.show()


def tabelare_varianta(alpha):
    return pd.DataFrame(data={
        "Varianta": alpha,
        "Varianta cumulata": np.cumsum(alpha),
        "Procent varianta": alpha * 100 / sum(alpha),
        "Procent cumulat": np.cumsum(alpha) * 100 / sum(alpha)
    }, index=["C" + str(v + 1) for v in range(len(alpha))])


def corelograma(matrice=None, dec=1, titlu='Corelograma corelatii factoriale', valMin=-1, valMax=1):
    plt.figure(titlu, figsize=(15, 11))
    plt.title(titlu, fontsize=14, color='k', verticalalignment='bottom')
    sb.heatmap(data=np.round(matrice, dec), cmap='bwr', vmin=valMin, vmax=valMax, annot=True)


def plot_instante(t, k1=0, k2=1, titlu="Plot instante"):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(1, 1, 1, aspect=1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": "b"})
    ax.set_xlabel(t.columns[k1])
    ax.set_ylabel(t.columns[k2])
    ax.axvline(color="g")
    ax.axhline(color="g")
    ax.scatter(t.iloc[:, k1], t.iloc[:, k2], c="r")
    for i in range(len(t)):
        ax.text(t.iloc[i, k1], t.iloc[i, k2], t.index[i])


def cerculCorelatiilor(matrice=None, X1=0, X2=1, raza=1, dec=2, titlu='Cercul corelatiilor',
                       valMin=-1, valMax=1, etichetaX=None, etichetaY=None):
    plt.figure(titlu, figsize=(8, 8))
    plt.title(titlu, fontsize=14, color='k', verticalalignment='bottom')
    # construirea coordonatelor punctelor pe cerc
    T = [t for t in np.arange(0, np.pi * 2, 0.01)]
    X = [np.cos(t) * raza for t in T]
    Y = [np.sin(t) * raza for t in T]
    plt.plot(X, Y)
    plt.axhline(y=0, color='g')
    plt.axvline(x=0, color='g')
    if etichetaX == None or etichetaY == None:
        if isinstance(matrice, pd.DataFrame):
            plt.xlabel(xlabel=matrice.columns[X1], fontsize=14, color='b', verticalalignment='top')
            plt.ylabel(ylabel=matrice.columns[X2], fontsize=14, color='b', verticalalignment='bottom')
        else:
            plt.xlabel(xlabel='Var ' + str(X1 + 1), fontsize=14, color='b', verticalalignment='top')
            plt.ylabel(ylabel='Var ' + str(X2 + 1), fontsize=14, color='b', verticalalignment='bottom')
    else:
        plt.xlabel(xlabel=etichetaX, fontsize=14, color='b', verticalalignment='top')
        plt.ylabel(ylabel=etichetaY, fontsize=14, color='b', verticalalignment='bottom')

    if isinstance(matrice, np.ndarray):
        plt.scatter(x=matrice[:, X1], y=matrice[:, X2], c='r', vmin=valMin, vmax=valMax)
        for i in range(matrice.shape[0]):
            # plt.text(x=0.25, y=0.25, s='un text')
            # plt.text(x=matrice[i, X1], y=matrice[i, X2], s='eticheta')
            plt.text(x=matrice[i, X1], y=matrice[i, X2], s='(' +
                                                           str(np.round(matrice[i, X1], dec)) + ', ' +
                                                           str(np.round(matrice[i, X2], dec)) + ')')

    if isinstance(matrice, pd.DataFrame):
        # plt.text(x=0.25, y=0.25, s='avem un pandas.DataFrame')
        plt.scatter(x=matrice.iloc[:, X1], y=matrice.iloc[:, X2], c='r', vmin=valMin, vmax=valMax)
        # for i in range(matrice.index.shape[0]):
        # for i in range(len(matrice.index)):
        for i in range(matrice.values.shape[0]):
            # plt.text(x=matrice.iloc[i, X1], y=matrice.iloc[i, X2], s='(' +
            #            str(np.round(matrice.iloc[i, X1], dec)) + ', ' +
            #            str(np.round(matrice.iloc[i, X2], dec)) + ')')
            plt.text(x=matrice.iloc[i, X1], y=matrice.iloc[i, X2], s=matrice.index[i])
