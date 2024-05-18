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
def filter_and_print_train_positions(positions, line):
    llista_trens = []
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
            tren_dict = tren.__dict__
            llista_trens.append(tren_dict)

    with open('trens.json', 'w') as f:
        json.dump(llista_trens, f, indent=4)


# Main function
if __name__ == "__main__":
    # Get train positions from the API
    train_positions = get_train_positions()

    # Filter and print the train positions
    line = input("Enter line: ")
    filter_and_print_train_positions(train_positions, line)
