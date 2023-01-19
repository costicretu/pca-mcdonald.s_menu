from acp import acp
from functions import *
import pandas as pd

tabel = pd.read_csv("./dataIN/data.csv", index_col=1)
variabile_observate = list(tabel)[1:]
nan_replace_t(tabel)

# Construire model
model_acp = acp(tabel, variabile_observate)
model_acp.fit()

# Varianta
print("Varianta componente:", model_acp.alpha)
plot_varianta(model_acp.alpha, model_acp.criterii)
tabel_varianta = tabelare_varianta(model_acp.alpha)
tabel_varianta.to_csv("./dataOUT/Varianta.csv")

# Corelatii
r = model_acp.r
m = len(variabile_observate)
etichete_componente = ["C" + str(i + 1) for i in range(m)]
t_r = pd.DataFrame(r, variabile_observate, etichete_componente)
t_r.to_csv("./dataOUT/r.csv")
corelograma(t_r)
cerculCorelatiilor(matrice=t_r)

# Componente/Scoruri
c = model_acp.c
alpha = model_acp.alpha
s = c / np.sqrt(alpha)
t_componente = pd.DataFrame(c, tabel.index, etichete_componente)
t_componente.to_csv("./dataOUT/scoruri.csv")
k = min(model_acp.criterii) + 1
print("Criterii:", model_acp.criterii)
for i in range(k):
    for j in range(i + 1, k):
        plot_instante(t_componente, i, j)

# Cosinusuri
c2 = c * c
cosin = (c2.T / np.sum(c2, axis=1)).T
pd.DataFrame(cosin, tabel.index, etichete_componente).to_csv("./dataOUT/cosin.csv")

# Contributii
contrib = c2 / np.sum(c2, axis=0)
pd.DataFrame(contrib, tabel.index, etichete_componente).to_csv("./dataOUT/contrib.csv")
# Comunalitati
comm = np.cumsum(r * r, axis=1)
t_comm = pd.DataFrame(comm, t_r.index, t_r.columns)
t_comm.to_csv("./dataOUT/Comm.csv")
corelograma(t_comm, 0, titlu="Comunalitati")

show()
