import numpy as np


def load_parametres_2019():

    tranch_marginal_impot = np.array([0, 9807, 27086, 72617, 153783])
    pourcentage = np.array([0, 0.14, 0.30, 0.41, 0.45])
    diff = np.diff(tranch_marginal_impot)

    return tranch_marginal_impot, pourcentage, diff


def calcul_de_parts():
    statu = input(
        'Quel est votre sitution famillial? 1 :"Celibataire|Divorcé|Veuf" / 2 :"Couple" / 3 :"Autre" : \t')
    nbr_enfant = float(
        input('Veuiller saisir le nombre d"enfants à votre charges : '))
    assert(nbr_enfant >= 0)

    if statu == '1':
        parts = 1
    elif statu == '2':
        parts = 2
    else:
        print('Veuillez saisir le bon choix !')

    # Enfants à charges
    if (nbr_enfant <= 2) and (nbr_enfant >= 0):
        parts += nbr_enfant * 0.5
    elif nbr_enfant > 2:
        parts += 1 + (nbr_enfant-2)

    print('Le nombre de part(s) fiscale est : {0:2.2f}'.format(parts))
    return parts, statu, nbr_enfant


def calcul_decote(impot_bareme, statu):
    decote = ((1177 - impot_bareme * 0.75)*(statu == '1') +
              (1939 - impot_bareme * 0.75)*(statu == '2') +
              0 * (statu == '3' or (statu != '1' and statu != '2')))  \
        if ((impot_bareme <= 1594 and statu == '1') or (impot_bareme <= 2626 and statu == '2')) else 0

    return decote


def application_bareme_sur_impot(quotient_familial):
    tranch_marginal_impot, pourcentage, diff = load_parametres_2019()
    i = 0
    impot_bareme = 0
    state = True

    while state:
        if quotient_familial < tranch_marginal_impot[i + 1]:
            impot_bareme += (quotient_familial -
                             tranch_marginal_impot[i]) * pourcentage[i]
            state = False
        else:
            impot_bareme += diff[i] * pourcentage[i]

            state = True

        print('impot sur la tranche {0:d} ({1:2.2f}) = {2:2.2f} Euros'.format(
            i+1, pourcentage[i], impot_bareme))
        i = i + 1
    return impot_bareme


def calcul_reduc_RFR(impot_total, revenu, parts, nbr_enfant):
    """la réduction d’impôt sous condition de revenu fiscal de référence (RFR)"""
    #  calcul du plafond de revenu fiscale reference
    pourcentage = 0

    if parts == 1 and revenu <= 18985:
        plafond_RFR = 18984 + nbr_enfant * 3797    # 21036
        pourcentage = .20

    elif parts == 2 and revenu <= 37969:
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
