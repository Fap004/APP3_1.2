import numpy as np
import matplotlib.pyplot as plt
import argparse

def coincidence(h1,h2):
    temps = 0.01
    i = 0
    y = 0
    hC = []  # Liste pour stocker les résultats
    hN =[] # Liste pour stocker les résultats non concident
    while i < len(h1) and y < len(h2):
        if h2[y][1] <= h1[i][1] + temps and h1[i][1] <= h2[y][1] + temps:
            if h2[y][2] <= h1[i][2]:
                hC.append((h2[y][1], h2[y][2]))  # Utiliser append pour ajouter à la liste
                y+=1
                i+=1
            elif h1[i][2] < h2[y][2]:
                hC.append((h1[i][1], h1[i][2]))  # Utiliser append pour ajouter à la liste
                y += 1
                i += 1
        elif h2[y][1] < h1[i][1]:
            y += 1
        elif h1[i][1] < h2[y][1]:
            hN.append((h1[i][1], h1[i][2]))
            i += 1
    return hC, hN

def histogramme(error,fichier):
    donneesCompletes1 = np.genfromtxt('S2GE_APP3_Problematique_Detecteur_Primaire.csv',delimiter=',')
    donneesCompletes2 = np.genfromtxt('S2GE_APP3_Problematique_Detecteur_Secondaire.csv',delimiter=',')

    hS, hN= coincidence(donneesCompletes1, donneesCompletes2)
    tempsTotal= (donneesCompletes1[-1][1]-donneesCompletes1[0][1])/1000
    tempsMort= np.sum(donneesCompletes1[:,3])/1000
    moyTempsMort= tempsMort/len(donneesCompletes1)

    tempsActif=tempsTotal-tempsMort
    histogramme1 = donneesCompletes1[:, 2]
    histogramme2 = donneesCompletes2[:, 2]
    histogramme3 = [item[1] for item in hS]
    histogramme4 = [item[1] for item in hN]
    bins = np.logspace(1, 3, num=25)

    plt.figure()
    plt.xlabel('amplitude(mV)')
    plt.ylabel('Rate/bin[S-1]')
    plt.semilogx()
    plt.grid()

    if error:
        plt.hist(histogramme1, bins=bins, histtype="step", weights = (1 / tempsActif) * np.ones_like(histogramme1),label="Tous les évenements")
        y,edge, _= plt.hist(histogramme3, bins=bins, histtype="step",weights = (1 / tempsActif) * np.ones_like(histogramme3), label="Coincident")
        plt.hist(histogramme4, bins=bins, histtype="step", weights = (1 / tempsActif) * np.ones_like(histogramme4), label="Autres")
        plt.title('histogramme amplitude corrigé')

        erreur = 2*100*(np.sqrt(y)/(tempsActif))
        centre = (edge[:-1] + edge[1:]) / 2
        plt.errorbar(centre, y, yerr=erreur, fmt='none', capsize=3, color='pink', label='erreur sur la coincidence')

        plt.legend()
        if fichier:
            plt.savefig("PAIF1582-STPE6468--corrige")
        else:
            plt.show()
    else:
        plt.hist(histogramme1, bins=bins, histtype="step", weights = (1 / tempsTotal) * np.ones_like(histogramme1),label="Tous les évenements")
        y,edge, _= plt.hist(histogramme3, bins=bins, histtype="step",weights = (1 / tempsTotal) * np.ones_like(histogramme3), label="Coincident")
        plt.hist(histogramme4, bins=bins, histtype="step", weights = (1 / tempsTotal) * np.ones_like(histogramme4), label="Autres")
        plt.title('histogramme amplitude non-corrigé')

        erreur = 2*100*(np.sqrt(y) / (tempsTotal))
        centre = (edge[:-1] + edge[1:]) / 2
        plt.errorbar(centre, y, yerr=erreur, fmt='none', capsize=3, color='pink', label='erreur sur la coincidence')

        plt.legend()
        if fichier:
            plt.savefig("PAIF1582-STPE6468")
        else:
            plt.show()


parser=argparse.ArgumentParser(description='Fichier et temps mort')
parser.add_argument('-F','--fichier', action='store_true',help='0=print à écran, 1=print en png')
parser.add_argument('-T','--temps-mort', action='store_true',help='0=sans barre d erreur, 1=barre d erreurs')
args = parser.parse_args()

histogramme(args.temps_mort,args.fichier)
