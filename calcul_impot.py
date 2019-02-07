#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on quotient_familialun Feb  3 19:25:43 2019
SOURCE/
https://droit-finances.commentcamarche.com/faq/20217-impot-sur-le-revenu-bareme-2018-2019#reduction-degressive
https://www.legifiscal.fr/actualites-fiscales/1729-impots-2018-baisse-foyers-modestes.html
http://impotsurlerevenu.org/calcul-de-l-impot-par-etapes/71-etape-8-impot-net.php
http://impotsurlerevenu.org/simulateurs/1180-simulateur-impot-2018.php
@author: amine
"""

print("Ce script permis le calcul de l'impot")


import numpy as np


#%% parametres pour le calcul d'impot en 2019 pour revenu de 2018

def load_parametres_2019():

    tranch_marginal_impot = np.array([0, 9807, 27086, 72617, 153783])
    pourcentage = np.array([0, 0.14, 0.30, 0.41, 0.45])
    diff = np.diff(tranch_marginal_impot)

    return tranch_marginal_impot, pourcentage, diff


def calcul_de_parts():
    statu = input('Quel est votre sitution famillial? 1 :"Celibataire|Divorcé|Veuf" / 2 :"Couple" / 3 :"Autre" : \t')
    nbr_enfant = float(input('Veuiller saisir le nombre d"enfants à votre charges : '))
    assert(nbr_enfant >= 0)

    if statu == '1':
        parts = 1
    elif statu == '2':
        parts = 2
    else:
        print('Veuillez saisir le bon choix !')
#        break

    # Enfants à charges
    if (nbr_enfant <= 2) and (nbr_enfant >= 0) :
        parts +=  nbr_enfant * 0.5
    elif nbr_enfant > 2:
        parts += 1 + (nbr_enfant-2)

    print('Le nombre de part(s) fiscale est : {0:2.2f}'.format(parts))
    return parts, statu, nbr_enfant


def calcul_decote(impot_bareme, statu):
    decote = ((1177 - impot_bareme * 0.75)*(statu == '1') + \
              (1939 - impot_bareme * 0.75)*(statu == '2') + \
             0 * (statu=='3' or (statu != '1' and statu != '2') ))  if ((impot_total<=1594 and statu=='1') or (impot_total<=2626 and statu=='2')) else 0

    return decote



def application_bareme_sur_impot(quotient_familial):
    tranch_marginal_impot, pourcentage, diff = load_parametres_2019()
    i = 0
    impot_bareme = 0
    state = True

    while state:
        if quotient_familial < tranch_marginal_impot[i + 1]:
            impot_bareme += (quotient_familial - tranch_marginal_impot[i]) * pourcentage[i]
            state = False
        else:
            impot_bareme += diff[i] * pourcentage[i]

            state = True

        print('impot sur la tranche {0:d} ({1:2.2f}) = {2:2.2f} Euros'.format(i+1, pourcentage[i], impot_bareme))
        i = i + 1
    return impot_bareme


def calcul_reduc_RFR(impot_total, revenu, parts, nbr_enfant):
    """la réduction d’impôt sous condition de revenu fiscal de référence (RFR)"""
    #  calcul du plafond de revenu fiscale reference 
    pourcentage = 0
    
    if parts == 1 and revenu <= 18985 :
        plafond_RFR = 18984 + nbr_enfant * 3797    # 21036
        pourcentage = .20
        
    elif parts == 2 and revenu <= 37969 :
        plafond_RFR = 37968 + nbr_enfant * 3797  # 42072
        pourcentage = .20
        
    # réduction dégresive
    elif parts == 1 and revenu > 18984 and revenu < 21037:
        plafond_RFR = 21036 + nbr_enfant * 3797
        pourcentage = .20 * (plafond_RFR - revenu) / 2000
    
    elif parts == 2 and revenu > 37968 and revenu < 42073:
        plafond_RFR = 42072 + nbr_enfant * 3797
        pourcentage = .20 * (plafond_RFR - revenu) / 4000
            
    return pourcentage * impot_total if revenu < plafond_RFR else 0

#%%

parts, statu, nbr_enfant = calcul_de_parts()

revenu =  float(input('\nVeuiller saisir le montant des salaires net: '))
assert(revenu >= 0)


print('* Déduction 10 % ou frais réels')
revenu = revenu * 0.90
print('=> Revenu net imposable: = {0:2.2f} Euros'.format(revenu))

quotient_familial = revenu/parts # quatient familial
print('=> Quotient familial = {0:2.2f} Euros'.format(quotient_familial))


print('\n* Application du barème:')
impot_bareme = application_bareme_sur_impot(quotient_familial)

print('\nImpot 2019 sur les revenues de 2018 soumis au barème : {0:2.2f} Euros'.format(impot_bareme))
impot_total = impot_bareme


print('\n* Verification pour une possibilité de réduction d"impot sur le revenu:  "La décote et la réduction d’impôt sous condition de revenu fiscal de référence (RFR)" ')

decote = calcul_decote(impot_bareme, statu)
impot_total -= decote
print('Décote : {0:2.2f} Euros'.format(decote))


reduc_revenu = calcul_reduc_RFR(impot_total, revenu, parts, nbr_enfant)
print('Reduction de l"impot sous condition de RFR : {0:2.2f} Euros'.format(reduc_revenu))

impot_total = max(0, impot_total - reduc_revenu)
print('\nTOTAL D"IMPOSITION NETTE  A RECOUVRIR EN 2019 sur les revenus de 2018 >> {0:2.2f} Euros <<'.format(impot_total))
