import subprocess
import time
from flask import Flask, request, jsonify

app = Flask(_name_)
# Adresse MAC de l'appareil Bluetooth
device_address = "D2:D1:D1:B8:54:1A"


# Fonction pour vérifier si la connexion est réussie
def check_connection():
    output = subprocess.run(["bluetoothctl", "info", device_address], capture_output=True, text=True)
    return "Connected: yes" in output.stdout


# Fonction pour se connecter à l'appareil Bluetooth
def connect_bluetooth():
    subprocess.run(["bluetoothctl", "connect", device_address])
    time.sleep(2)


@app.route('/control', methods=['POST'])
def control():
    try:
        data = request.get_json()

        # Convertir la trame en une liste d'entiers
        data_decimal = data['command']

        # Convertir la liste en une chaîne hexadécimale avec le préfixe "0x"
        command_str = ' '.join([f"0x{value:02X}" for value in data_decimal])

        # Afficher la chaîne hexadécimale
        print(command_str)

        # Exécuter la commande Bluetooth

        subprocess.run(["sudo", "bluetoothctl"],
                       input=f"menu gatt\nselect-attribute 75120002-56b4-4cc2-8b25-22729f38456b\nwrite '{command_str}'\n",
                       text=True, check=True)
        print(result.stdout)
        print(result.stderr)

        return jsonify({'message': 'Command received successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if _name_ == '_main_':
    while True:
        while not check_connection():
            connect_bluetooth()
        app.run(host='0.0.0.0', port=5000)