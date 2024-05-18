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
def filter_and_print_train_positions(positions):
    llista_trens = []
    if positions:
        for position in positions:
            print(position)
            # Filter out positions where 'tipo_unidad' is not 115
            if position.get('ocupacio_mi_percent') != None:
                continue

            """
            # Print the relevant data
            print(f"ID: {position.get('id', 'N/A')}")
            print(f"line: {position.get('lin', 'N/A')}")
            print(f"geolocalization: {position.get('geo_point_2d', 'N/A')}")
            print(f"direction: {position.get('dir', 'N/A')}")
            print(f"next_stops: {position.get('properes_parades', 'N/A')}")
            print(f"unit_type: {position.get('tipus_unitat', 'N/A')}")
            print(f"Mi_ocupation: {position.get('ocupacio_mi_percent', 'N/A')}")
            print(f"Ri_ocupation: {position.get('ocupacio_ri_percent', 'N/A')}")
            print(f"M1_ocupation: {position.get('ocupacio_m1_percent', 'N/A')}")
            print(f"M2_ocupation: {position.get('ocupacio_m2_percent', 'N/A')}")
            print("\n" + "-" * 40 + "\n")
            """
            ID = position.get('id', 'N/A')
            LINE = position.get('lin', 'N/A')
            GEO = position.get('geo_point_2d', 'N/A')
            DIR = position.get('dir', 'N/A')
            NEXT = position.get('properes_parades', 'N/A')
            TYPE = position.get('tipus_unitat', 'N/A')

            #convertim les següents parades a dict
            NEXT = NEXT.split(';')
            NEXT = [json.loads(element) for element in NEXT]
            print(NEXT)


            M1 = position.get('ocupacio_m1_percent', 'N/A')
            M2 = position.get('ocupacio_m2_percent', 'N/A')
            MI = position.get('ocupacio_mi_percent', 'N/A')
            RI = position.get('ocupacio_ri_percent', 'N/A')

            tren = Train(LINE, ID, DIR, NEXT, TYPE, GEO, M1, M2, MI, RI)
            llista_trens.append()


# Main function
if __name__ == "__main__":
    # Get train positions from the API
    train_positions = get_train_positions()

    # Filter and print the train positions
    filter_and_print_train_positions(train_positions)
