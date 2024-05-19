import requests
import train
import time
import json


def queden_minusvalids(dicc):
    return not (all(element["minusvalid"] == 0 for element in dicc["carriers"].values()))


def queden_reservats(dicc):
    return not (all(element["reservats"] == 0 for element in dicc["carriers"].values()))


def troba_tren(parada_inical, parada_final, sindrome):
    with open('trens.json', 'r') as f:
        ll_trens = json.load(f)

    dic_parades = {"Plaça Catalunya": "PC", "Provença": "PR", "Gràcia": "GR", "Sant Gervasi": "SG", "Muntaner": "MN",
                   "La Bonanova": "BN", "Les Tres Torres": "TT", "Sarrià": "SR", "Peu del Funicular": "PF",
                   "Baixador de Vallvidrera": "VL", "Les Planes": "LP", "La Floresta": "LF", "Valldoreix": "VD",
                   "Sant Cugat Centre": "VD", "Volpelleres": "VO", "Sant Joan": "SJ", "Bellaterra": "BT",
                   "Universitat Autònoma": "UN", "Sant Quirze": "SQ", "Can Feu | Gràcia": "CF",
                   "Sabadell Plaça Major": "PJ", "La Creu Alta": "CT", "Sabadell Nord": "NO",
                   "Sabadell Parc del Nord": "PN"}

    inicial = dic_parades[parada_inical]
    final = dic_parades[parada_final]
    direccio = None

    for value in dic_parades.values():
        if value == inicial:
            direccio = "A"
            break
        if value == final:
            direccio = "D"
            break

    final = None
    minim = float("inf")

    for tren in ll_trens:
        if sindrome in ["Cadira de rodes", "Cotxet"] and not queden_minusvalids(tren):
            continue
        if sindrome in ["Lisiat/da", "Embaraçada", "3a Edat", "Família"] and not queden_reservats(tren):
            continue
        cont = 0
        if tren["direction"] == direccio:
            for parada_tren in tren["stops"]:
                cont += 1
                if list(parada_tren.values())[0] == inicial:
                    if cont < minim:
                        final, minim = tren, cont

    selected_train = train.Train(final["line"], final["ID"], final["direction"], final["stops"], final["train_type"],
                                 final["position"], int(list(final["carriers"].values())[0]["percent"]),
                                 int(list(final["carriers"].values())[0]["percent"]),
                                 int(list(final["carriers"].values())[0]["percent"]),
                                 int(list(final["carriers"].values())[0]["percent"]))
    if sindrome in ["Cadira de rodes", "Cotxet"]:
        selected_train.decrementa_minusvalids()
    if sindrome in ["Lisiat/da", "Embaraçada", "3a Edat", "Família"]:
        selected_train.decrementa_reservats()

    return selected_train


if __name__ == "__main__":

    tren = troba_tren("Valldoreix", "Les Planes", "Cadira de rodes")
    print(tren)

    for _ in range(20):
        cotxe = tren.decrementa_minusvalids()
        print(tren, "\n", cotxe, "\n------------")



