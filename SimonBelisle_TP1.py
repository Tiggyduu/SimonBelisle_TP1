
from ctypes import resize
import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QScrollArea,
    QLineEdit,
    QCompleter,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt
    # J'inclus beaucoup de choses pour que mon code fontionne

def get_json_file():

    json_file = sys.argv[2]

    # Print dans la console pour indiquer uqe le fichier est en train de loader

    print(f"Loading data from {json_file}")

    return json_file

def load_json_data(json_file):

    # J'utilise le try tel que vu en classe pour ouvrir le fichier et envoyé le message d'erreur en cas d'échec
    # Encoding en utf-8 pour que les charactère spéciaux apparaisse normaux dans mon tableau

    try:

        file = open(json_file, encoding="utf-8")
        data = json.load(file)

        return data
    
    except:

        print(f"Could not load data from {json_file}")

        return None

def resize_to_fit_content(window, tableau):

    # Agrandi ou rétrécit la window pour que le tableau s'affiche au complet

    window.resize(tableau.horizontalHeader().length() + tableau.verticalHeader().width() + 20, 600)

def load_data_table(data):

    # Créer le tableau à partir de "data" avec le nombre de keys et de values par keys

    tableau = QTableWidget()

    tableau.setRowCount(len(data))
    tableau.setColumnCount(len(data[0]))

    # Créer des header labels à partir du [0, x] de data

    tableau.setHorizontalHeaderLabels(list(data[0].keys()))

    # Deux for loops pour remplir le talbeau horizontalement et verticalement [i, j].

    for i in range(len(data)):
        item = data[i]
        keys = list(item.keys())

        # Pour chaque row, la 2e for loop remplit le tableau avec les values de chaque keys (ou l'inverse?).

        for j in range(len(list(data[i].keys()))):

            # Vérifier si la value est un int ou un float pour trier l'item dans "item_nombre"
            # Ça sert à pouvoir trier les nombres correctement dans la fonction sort()

            nombre = item[keys[j]]
            item_nombre = QTableWidgetItem()

            if isinstance(nombre, (int, float)):

                item_nombre.setData(Qt.EditRole, nombre)

            else:

                item_nombre.setText(str(nombre))

            tableau.setItem(i, j, item_nombre) 

    return tableau

def sort(tableau):

    # Si SortingEnabled est vrai, le tableau se trie tout seul, si faux, il prend son ordre par défault

    tableau.setSortingEnabled(True)

class MainWindow(QMainWindow):

    # Ceci crée la window dans laquelle les widgets apparaissent.

    def __init__(self):

        super().__init__()

        self.setWindowTitle("TP1")
        self.resize(800, 600)

        # J'ai ajouté un scroller

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Je crée un container et je le met dans le scroll area et tantôt je met mon tableau dans le scoll area

        container = QWidget()
        self.container_layout = QVBoxLayout()
        container.setLayout(self.container_layout)

        self.scroll_area.setWidget(container)
        self.setCentralWidget(self.scroll_area)

        # Je crée une searchbar pour accéder au données du tableau plus facilement

        self.searchbar = QLineEdit(placeholderText="Rechercher")
        self.searchbar.textChanged.connect(self.update_display)
        self.container_layout.addWidget(self.searchbar)

        # Cette partie permet d'autocomplete la recherche

    def update_display(self, text):

        # "search est ce que ma loop cherche dans mon tableau"

        search = text.strip().casefold()

        for row in range(self.tableau.rowCount()):

            # On assume que le contient_text est faux pas défaut

            contient_text = False
            
            # Vérifier si au moins une column contient le texte
            # Une for loop qui vérifie chaque column et une autre qui véfifie chaque row

            for col in range(self.tableau.columnCount()):

                item = self.tableau.item(row, col)

                if item and search in item.text().casefold():

                    contient_text = True

            # Cacher ou afficher la ligne selon le résultat

            self.tableau.setRowHidden(row, not contient_text)

# Application

app = QApplication([])
window = MainWindow()

# Afficher le tableau

tableau = load_data_table(load_json_data(get_json_file()))

# Cette ligne permet à la window de mettre le comtenu de tableau dans le vecteur "mots" pour que la searchbar fonctionne.

window.tableau = tableau

# Mettre tableau dans le container

window.container_layout.addWidget(tableau)


resize_to_fit_content(window, tableau)
sort(tableau)

window.show()
sys.exit(app.exec())
