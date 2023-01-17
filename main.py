#Traitement des données de propagation thermique dans le cadre du TIPE de Matteo Liagre

#IMPORT SEC
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

data = pd.read_csv('TIPE_MATTEO.csv')
temps = data['temps']
temps = list(temps)
temps = [i - temps[0] for i in temps]
temps = np.array(temps)

def colextractor(data):
    columns: list = []
    for i in range(1,9):
        c = data[f'C{i}']
        c = list(c)
        c = [str(elt).replace(',','.') for elt in c]
        c = [float(elt) for elt in c]
        c = np.array(c)
        columns.append(c)
    return columns
        
columns = colextractor(data)

#Make the data more readable
temps = [temps[i] for i in range(len(temps)) if i%17 == 0]
for i in range(len(columns)):
    columns[i] = [columns[i][j] for j in range(len(columns[i])) if j%17 == 0]

#Linear regressions
def coef():
    coefs = [[]]*8
    for i in range (len(columns)):
        coefs[i] = np.polyfit(temps,columns[i],1)
    return coefs
coefs = coef()

def trace():
    figure, axis = plt.subplots(2,1,sharex=True)
    colors = ['rx','bx','gx','bx','mx','yx','kx','cx']
    linecolors = ['--r','--b','--g','--b','--m','--y','--k','--c']
    for i in range(len(columns)):
        if i == 1 or i == 7 or i == 6 or i == 2 or i == 0:
            poly1d_fn = np.poly1d(coefs[i])
            axis[0].plot(temps,poly1d_fn(temps),linecolors[i])
            axis[0].errorbar(temps,columns[i],xerr=0,yerr=0.1,fmt=colors[i],markersize=2,alpha=0.3,label=f'C{i+1}')
   
        else:
            poly1d_fn = np.poly1d(coefs[i])
            axis[0].plot(temps,poly1d_fn(temps),linecolors[i])
            axis[0].errorbar(temps,columns[i],xerr=0,yerr=0.1,fmt=colors[i],markersize=2,alpha=0.3,label=f'C{i+1}')
            axis[1].plot(temps,poly1d_fn(temps),linecolors[i])
            axis[1].errorbar(temps,columns[i],xerr=0,yerr=0.1,fmt=colors[i],markersize=2,alpha=0.3,label=f'C{i+1}')   
    axis[0].legend(loc='upper left')
    axis[1].legend()
    axis[0].set_title('Evolution de la temperature au cours du temps')
    axis[0].set_ylabel('Temperature (en °C)')
    axis[1].set_xlabel('Temps (en s)')
    plt.tight_layout()
    plt.savefig('figure.jpg', dpi=300)

trace()
