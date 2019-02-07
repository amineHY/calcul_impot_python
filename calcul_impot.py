# %% SETUP
# #!/usr/bin/env python3
# -*- coding: utf-8 -*-
from routine import *
import numpy as np
"""
Created on quotient_familialun Feb  3 19:25:43 2019
SOURCE/
https://droit-finances.commentcamarche.com/faq/20217-impot-sur-le-revenu-bareme-2018-2019#reduction-degressive
https://www.legifiscal.fr/actualites-fiscales/1729-impots-2018-baisse-foyers-modestes.html
http://impotsurlerevenu.org/calcul-de-l-impot-par-etapes/71-etape-8-impot-net.php
http://impotsurlerevenu.org/simulateurs/1180-simulateur-impot-2018.php
@author: amine
"""

print("Ce script permis le calcul de l'impot 2019 pour revnu 2018")


# %% parametres pour le calcul d'impot en 2019 pour revenu de 2018

parts, statu, nbr_enfant = calcul_de_parts()

revenu = float(input('\nVeuiller saisir le montant des salaires net: '))
assert(revenu >= 0)

# %%
print('* Déduction 10 % ou frais réels')
revenu = revenu * 0.90
print('=> Revenu net imposable: = {0:2.2f} Euros'.format(revenu))

quotient_familial = revenu/parts  # quatient familial
print('=> Quotient familial = {0:2.2f} Euros'.format(quotient_familial))


print('\n* Application du barème:')
impot_bareme = application_bareme_sur_impot(quotient_familial)

print('\nImpot 2019 sur les revenues de 2018 soumis au barème est : {0:2.2f} Euros'.format(
    impot_bareme))

# %%
print('\nVerification pour une possibilité de réduction d"impot sur le revenu:  "La décote et la réduction d’impôt sous condition de revenu fiscal de référence (RFR)" ')

decote = calcul_decote(impot_bareme, statu)
print('* Décote : {0:2.2f} Euros'.format(decote))

impot_total = impot_bareme - decote
reduc_revenu = calcul_reduc_RFR(impot_total, revenu, parts, nbr_enfant)
print('* Reduction de l"impot sous condition de RFR : {0:2.2f} Euros'.format(
    reduc_revenu))

impot_total = max(0, impot_total - reduc_revenu)
print('\nTOTAL D"IMPOSITION NETTE  A RECOUVRIR EN 2019 sur les revenus de 2018 >> {0:2.2f} Euros <<\n'.format(
    impot_total))


print('Le taux de prélèvement personnaliser est : {0:2.2f} %\n'.format(impot_total * 100 / revenu))
