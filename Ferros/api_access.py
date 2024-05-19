import requests
import train
import time
import json

# Define the base URL for the specific dataset API
BASE_URL = "https://dadesobertes.fgc.cat/api/v2/catalog/datasets/posicionament-dels-trens/exports/json"


# Function to get train positions from the API
def get_train_positions():
    try:
        # Make the GET request to the API
        t0 = time.time()
        response = requests.get(BASE_URL)
        t1 = time.time()
        print(t1 - t0, "segons per accedir a l'API")

        # Check if the request was successful
        if response.status_code == 200:
            train_positions = response.json()
            return train_positions
        else:
            print(f"Failed to retrieve train positions: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Function to filter and print train positions
def inicialitza(positions, line):
    llista_trens_dict = []
    llista_trens_inst = []
    if positions:
        for position in positions:
            if not position.get('ocupacio_mi_percent'):
                continue

            ID = position.get('id', 'N/A')
            LINE = position.get('lin', 'N/A')
            if LINE != line:
                continue
            GEO = position.get('geo_point_2d', 'N/A')
            DIR = position.get('dir', 'N/A')
            NEXT = position.get('properes_parades', 'N/A')
            TYPE = position.get('tipus_unitat', 'N/A')

            NEXT = NEXT.split(';')
            NEXT = [json.loads(element) for element in NEXT]

            M1 = position.get('ocupacio_m1_percent', 'N/A')
            M2 = position.get('ocupacio_m2_percent', 'N/A')
            MI = position.get('ocupacio_mi_percent', 'N/A')
            RI = position.get('ocupacio_ri_percent', 'N/A')

            tren = train.Train(LINE, ID, DIR, NEXT, TYPE, GEO, M1, M2, MI, RI)
            tren_dict = tren.to_dict()
            llista_trens_dict.append(tren_dict)
            llista_trens_inst.append(tren)

    with open('trens.json', 'w') as f:
        json.dump(llista_trens_dict, f, indent=4)

    return llista_trens_inst


def actualitza(positions, ll_trens, line):
    llista_trens_dict = []
    llista_trens_inst = []

    dic_trens = {tren._ID: tren for tren in ll_trens}

    for position in positions:
        if not position.get('ocupacio_mi_percent'):
            continue

        ID = position.get('id', 'N/A')
        DIR = position.get('dir', 'N/A')

        NEXT = position.get('properes_parades', 'N/A')
        NEXT = NEXT.split(';')
        NEXT = [json.loads(element) for element in NEXT]

        GEO = position.get('geo_point_2d', 'N/A')
        M1 = position.get('ocupacio_m1_percent', 'N/A')
        M2 = position.get('ocupacio_m2_percent', 'N/A')
        MI = position.get('ocupacio_mi_percent', 'N/A')
        RI = position.get('ocupacio_ri_percent', 'N/A')

        if ID in dic_trens.keys():
            tren = dic_trens[ID]

            tren.set_direction(DIR)
            tren.set_stops(NEXT)
            tren.set_position(GEO)
            tren.set_carrier(M1, M2, MI, RI)


        else:

            LINE = position.get('lin', 'N/A')
            if LINE != line:
                continue
            GEO = position.get('geo_point_2d', 'N/A')
            DIR = position.get('dir', 'N/A')
            NEXT = position.get('properes_parades', 'N/A')
            TYPE = position.get('tipus_unitat', 'N/A')

            NEXT = NEXT.split(';')
            NEXT = [json.loads(element) for element in NEXT]

            M1 = position.get('ocupacio_m1_percent', 'N/A')
            M2 = position.get('ocupacio_m2_percent', 'N/A')
            MI = position.get('ocupacio_mi_percent', 'N/A')
            RI = position.get('ocupacio_ri_percent', 'N/A')

            tren = train.Train(LINE, ID, DIR, NEXT, TYPE, GEO, M1, M2, MI, RI)

        tren_dict = tren.to_dict()
        llista_trens_dict.append(tren_dict)
        llista_trens_inst.append(tren)

    with open('trens.json', 'w') as f:
        json.dump(llista_trens_dict, f, indent=4)

    return llista_trens_inst


def main():
    line = "S2"

    train_positions = get_train_positions()
    ll_trens = inicialitza(train_positions, line)

    while True:
        train_positions = get_train_positions()
        ll_trens = actualitza(train_positions, ll_trens, line)
        time.sleep(60)


if __name__ == "__main__":
    main()


