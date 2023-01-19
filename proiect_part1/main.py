import pandas as pd
import matplotlib.pyplot as plt

data_columns = ['Produs', 'MarimeaPortiei', 'Caloriile', 'CaloriiDinGrasime', 'GrasimeTotala',
                'GrasimiTotale(%valoareZilnica)', 'GrasimeSaturata', 'GrasimiSaturate(%valoareZilnica)',
                'GrasimiNesaturate', 'Colesterolul', 'Colesterol(%valoareZilnica)', 'Sodiu', 'Sodiu(%valoareZilnica)',
                'Carbohidrati', 'Carbohidrati(%valoareZilnica)', 'FibreDietetice', 'FibreDietetice(%valoareZilnica)',
                'Zaharuri', 'Proteina', 'VitaminaA(%valoareZilnica)', 'VitaminaC(%valoareZilnica)',
                'Calciu(%valoareZilnica)', 'Fier(%valoareZilnica)']
data = pd.read_csv('./dataIN/data.csv', usecols=data_columns, index_col=0)

categories_columns = ['Produs', 'MarimeaPortiei', 'Categorie']
categories = pd.read_csv('./dataIN/categories.csv', usecols=categories_columns, index_col=0)

# Exemplu operatii cu siruri de caractere, liste, tupluri si dictionare
portii = categories.MarimeaPortiei.to_list()
nrProduse = 0
for i in range(len(portii)):
    x = portii[i].count('1', 8, 9)
    nrProduse += x
print(str(nrProduse) + ' produse au gramajul mai mare sau cel putin egal cu 100')

categorii = categories.Categorie.to_list()
for i in range(len(categorii)):
    if '&' in categorii[i]:
        print('Categoria de mancare: ' + str(categorii[i]) + ' este compusa din doua cuvinte')

reuniune = data.merge(right=categories, how='outer', left_index=True, right_index=True)
print(reuniune)
reuniune.to_csv('./dataOUT/reuniune.csv')

details = list(data.columns.values[1:])
categorii = details + ['Categorie']
agregareCategorii = reuniune[categorii].groupby('Categorie').agg(func=min)
print(agregareCategorii)
agregareCategorii.to_csv('./dataOUT/agregarepecategorii.csv')

# scatter plot
plt.plot('Caloriile', 'Proteina', data=data, linestyle='none', marker='o')
plt.xlabel('Caloriile')
plt.ylabel('Proteina')
plt.title('Gramajul de proteina per calorii')
plt.show()

# bar plot
plt.bar('Zaharuri', 'Caloriile', data=data)
plt.xlabel('Zaharuri', verticalalignment='top')
plt.ylabel('Caloriile')
plt.title('Nivelul de zaharuri per calorii')
plt.show()

# pie chart
a = data.values[2].tolist()
a.remove('3.9 oz (111 g)')
names = 'Caloriile', 'CaloriiDinGrasime', 'GrasimeTotala', 'GrasimiTotale(%valoareZilnica)', 'GrasimeSaturata', 'GrasimiSaturate(%valoareZilnica)', 'GrasimiNesaturate', 'Colesterolul', 'Colesterol(%valoareZilnica)', 'Sodiu', 'Sodiu(%valoareZilnica)', 'Carbohidrati', 'Carbohidrati(%valoareZilnica)', 'FibreDietetice', 'FibreDietetice(%valoareZilnica)', 'Zaharuri', 'Proteina', 'VitaminaA(%valoareZilnica)', 'VitaminaC(%valoareZilnica)', 'Calciu(%valoareZilnica)', 'Fier(%valoareZilnica)'
plt.pie(a, labels=names)
plt.xlabel('')
plt.ylabel('')
plt.title('Valori nutritionale pe produsul Egg McMuffin')
plt.show()
