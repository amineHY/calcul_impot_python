# Simulateur de l'impot en python !

*Ce mini projet en python est consacré pour le calcul de l'impot, l'idée m'est venu après avoir été frustré lors de la lecture des chiffres incompréhensible sur mon avis d'imposition ! et surout je voulais confirmer que le comptes est bon pour mes impots.
Enfin j'ai eu le curiosité de décortiquer l'usine de calcul des impots. 
En effet, il reste encore des choses a prendre en comptes.
*

## Ce script permis le calcul de l'impot 2019 pour revnu 2018
En entrée, l'algorithm prend trois information

1.**Quel est votre sitution famillial? choisir :**
    1. Celibataire, Divorcé, Veuf
    2. Couple
    3. Autre 

2.**Veuiller saisir le nombre d"enfants à votre charges** : xxx
    * Le nombre de part(s) fiscale est : xxx

3.**Veuiller saisir le montant des vos revenu imposable (en euro)**: xxx

## Le calcul commence par ici:

        * calcul du Revenu net imposable (Déduction 10 % ou frais réels) = xxx Euros



        * calcul du Quotient familial = xxx Euros

    * Application du barème:

        1. impot sur la tranche 1 (0.00) = xxx Euros

        2. impot sur la tranche 2 (0.14) = xxx Euros

        3. ...

        * Impot 2019 sur les revenues de 2018 soumis au barème est : xxx Euros

## Verification d'une possibilité de réduction d"impot sur le revenu: 
    "La décote et la réduction d’impôt sous condition de revenu fiscal de référence (RFR)"

    1. Décote = xxx Euros

    2. Reduction de l"impot sous condition de RFR = xxx Euros

TOTAL D"IMPOSITION NETTE  A RECOUVRIR EN 2019 sur les revenus de 2018 >> xxx Euros <<


## webpage: [Link](https://aminehy.github.io/calcul_impot_python/)




## Voici l'ensemble des routines developpé pour ce simulateur

``` python
def load_parametres_2019():

    tranch_marginal_impot = np.array([0, 9807, 27086, 72617, 153783])
    pourcentage = np.array([0, 0.14, 0.30, 0.41, 0.45])
    diff = np.diff(tranch_marginal_impot)

    return tranch_marginal_impot, pourcentage, diff
```

``` python
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

    print('* Le nombre de part(s) fiscale est : {0:2.2f}'.format(parts))
    return parts, statu, nbr_enfant
```

``` python
def calcul_decote(impot_bareme, statu):
    plafond_impot = [1594, 2626]
    param = [1196, 1970]
    decote = ((param[0] - impot_bareme * 0.75)*(statu == '1') +
              (param[1] - impot_bareme * 0.75)*(statu == '2') +
              0 * (statu == '3' or (statu != '1' and statu != '2')))  \
        if ((impot_bareme <= plafond_impot[0] and statu == '1') or
            (impot_bareme <= plafond_impot[1] and statu == '2')) else 0

    return decote
``` 

``` python
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
```

``` python
def calcul_reduc_RFR(impot_total, revenu, parts, nbr_enfant):
    """la réduction d’impôt sous condition de revenu fiscal de référence (RFR)"""
    #  calcul du plafond de revenu fiscale reference
    pourcentage = 0
    limites = [18985, 37969, 21037, 42073, 3797]
    if parts == 1 and revenu <= limites[0]:
        plafond_RFR = limites[0] + nbr_enfant * limites[-1]
        pourcentage = .20

    elif parts == 2 and revenu <= limites[1]:
        plafond_RFR = limites[1] + nbr_enfant * limites[-1]
        pourcentage = .20

    # réduction dégresive
    elif parts == 1 and revenu > limites[0] and revenu < limites[2]:
        plafond_RFR = limites[2] + nbr_enfant * limites[-1]
        pourcentage = .20 * (plafond_RFR - revenu) / 2000

    elif parts == 2 and revenu > limites[2] and revenu < limites[3]:
        plafond_RFR = limites[3] + nbr_enfant * limites[-1]
        pourcentage = .20 * (plafond_RFR - revenu) / 4000

    return pourcentage * impot_total if revenu < plafond_RFR else 0
```

