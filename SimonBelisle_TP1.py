
from ctypes import resize
import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem
)

def get_json_file():
    json_file = sys.argv[1]
    print(f"Loading data from {json_file}")
    return json_file

def load_json_data(json_file):
    try:
        file = open(json_file, encoding="utf-8")
        data = json.load(file)
        print(type(data))
        return data
    except:
        print(f"Could not load data from {json_file}")
        return None


json_file = get_json_file()
data = load_json_data(json_file)

# Créer le tableau à partir de "data" avec le nombre de keys et de values par keys
app = QApplication([])
tableau = QTableWidget()
tableau.setHorizontalHeaderLabels(list(data[0].keys()))
tableau.setRowCount(len(data))
tableau.setColumnCount(len(data[0]))

# Deux for loops pour remplir le talbeau horizontalement et verticalement.

for i in range(len(data)):
    item = data[i]
    keys = list(item.keys())

    # Pour chaque row, la 2e for loop remplit le tableau avec les values de chaque keys (ou l'inverse?).

    for j in range(len(list(data[i].keys()))):

        tableau.setItem(i, j, QTableWidgetItem(str(item[list(item.keys())[j]]))) 


window = QMainWindow()
window.setCentralWidget(tableau)
window.show()
sys.exit(app.exec())