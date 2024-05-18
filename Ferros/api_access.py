import requests

# Define the base URL for the specific dataset API
BASE_URL = "https://dadesobertes.fgc.cat/api/v2/catalog/datasets/posicionament-dels-trens/exports/json"


# Function to get train positions from the API
def get_train_positions():
    try:
        # Make the GET request to the API
        response = requests.get(BASE_URL)

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
    if positions:
        for position in positions:

            # Filter out positions where 'tipo_unidad' is not 115
            if position.get('ocupacio_mi_percent') != None:
                continue

            # Print the relevant data
            print(f"ID: {position.get('id', 'N/A')}")
            print(f"line: {position.get('linia', 'N/A')}")
            print(f"geolocalization: {position.get('Geolocalizacion', 'N/A')}")
            print(f"direction: {position.get('direccion', 'N/A')}")
            print(f"next_stops: {position.get('proximas_paradas', 'N/A')}")
            print(f"unit_type: {position.get('tipo_unidad', 'N/A')}")
            print(f"Mi_ocupation: {position.get('ocupacio_mi_percent', 'N/A')}")
            print(f"Ri_ocupation: {position.get('ocupacio_ri_percent', 'N/A')}")
            print(f"M1_ocupation: {position.get('ocupacio_m1_percent', 'N/A')}")
            print(f"M2_ocupation: {position.get('ocupacio_m2_percent', 'N/A')}")
            print("\n" + "-" * 40 + "\n")


# Main function
if __name__ == "__main__":
    # Get train positions from the API
    train_positions = get_train_positions()

    # Filter and print the train positions
    filter_and_print_train_positions(train_positions)
