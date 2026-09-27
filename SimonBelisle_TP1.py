# Importation de librairies
from ctypes import resize
import sys
import json # Pour lire les fihciers json.
import os # Pour afficher le nom, la taille en mémoire et le nombre d’éléments du fichier.

# Tous les Q** servent à créer l'app et ce qu'il y a dedans.

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QScrollArea,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QWidget,
)
from PySide6.QtCore import Qt

    # J'inclus beaucoup de choses pour que mon code fontionne
# Va cherche le fichier
def get_json_file(window):

    # Cette fonction prend le chemin d'accès dans la barre de recherche pour être utilisée dans load_json_data.

    json_file = window.input.text()

    # Print dans la console pour indiquer que le fichier est en train de loader.

    print(f"Loading data from {json_file}")

    return json_file
# Import le contenu du fichier
def load_json_data(json_file):

    # J'utilise le "try" tel que vu en classe pour ouvrir le fichier et envoyé le message d'erreur en cas d'échec.

    try:

        # Encoding en utf-8 pour que les charactère spéciaux apparaisse normaux dans mon tableau.

        file = open(json_file, encoding="utf-8")
        data = json.load(file)

        return data
    
    except:

        print(f"Could not load data from {json_file}")

        return None
# Ajuste la taille de l'app
def resize_to_fit_content(window, tableau):

    # Agrandi ou rétrécit la window pour que le tableau s'affiche au complet.

    # Calcule la largeur selon le header du tableau.

    if tableau.horizontalHeader().length() > 1000:
            
            largeur = 1000

    else:

        largeur = tableau.horizontalHeader().length() + tableau.verticalHeader().width() + 30

    # Calcule la hauteur selon la hauteur vertical du tableau.

    if tableau.verticalHeader().length() < 300:

        hauteur = 300

    else:

        hauteur = 600

    window.resize(largeur, hauteur)
# Rempli un tableau avec le json
def load_data_table(data):

    # Crée le tableau à partir de "data" avec le nombre de keys et de values par keys.

    tableau = QTableWidget()

    tableau.setRowCount(len(data))
    tableau.setColumnCount(len(data[0]))

    # Crée des header labels à partir des keys de la case 0 de data.

    tableau.setHorizontalHeaderLabels(list(data[0].keys()))

    # Loops pour remplir le tableau horizontalement et verticalement [i, j] (i est rempli les row, j rempli les columns)

    for i in range(len(data)):
        item = data[i]
        keys = list(item.keys())

        for j in range(len(list(data[i].keys()))):

            # Vérifie si la value est un int ou un float pour trier l'item dans "item_nombre" pour trier correctement dans "sort".

            nombre = item[keys[j]]
            item_nombre = QTableWidgetItem()

            if isinstance(nombre, (int, float)):

                # Stocke la valeur en in ou float.

                item_nombre.setData(Qt.EditRole, nombre)

            else:

                # Converti en texte ("str" transforme en string).

                item_nombre.setText(str(nombre))

            tableau.setItem(i, j, item_nombre) 

    return tableau
# Tri le contenu du tableau
def sort(tableau):

    # Si SortingEnabled est vrai, le tableau se trie tout seul, si faux, il prend son ordre par défault

    tableau.setSortingEnabled(True)
# Crée l'app, les widgets, etc.
def creating_window(window):

    window.setWindowTitle("TP1")

    # Scroller pour naviguer le tableau.

    window.scroll_area = QScrollArea()
    window.scroll_area.setWidgetResizable(True)

    # Création d'un container pour mettres les widgets dedans.

    container = QWidget()
    window.container_layout = QVBoxLayout()
    container.setLayout(window.container_layout)

    window.scroll_area.setWidget(container)
    window.setCentralWidget(window.scroll_area)

    # Input pour fichier json.

    input_json_box = QVBoxLayout()
    window.input = QLineEdit()
    window.input.setPlaceholderText("Entrez fihcier JSON")
    load_button = QPushButton("Load")

    input_json_box.addWidget(window.input)
    input_json_box.addWidget(load_button)
    window.container_layout.addLayout(input_json_box)

    def load_file_in_app():

        json_file = get_json_file(window)
        data = load_json_data(json_file)
        if data:

            # Supprime le tableau avant d'en créer un nouveau (pour pouvoir load plusieurs tableau sans redémarrer l'app).

            if hasattr(window, 'tableau') and window.tableau:
                window.container_layout.removeWidget(window.tableau)
                window.tableau.deleteLater()
                
            window.tableau = load_data_table(data)
            window.container_layout.addWidget(window.tableau)
            
            resize_to_fit_content(window, window.tableau)
            sort(window.tableau)

            # La search bar est cachée avant d'appeler cette fonction.

            window.searchbar.show()

            # Récupère les infos du fichier json et les affiche en bas de l'app.
            
            nom_fichier = os.path.basename(json_file)
            taille = os.path.getsize(json_file)
            nombre_elements = window.tableau.rowCount()
            window.status_label.setText(f"Fichier : {nom_fichier} | Taille : {taille:.2f} Ko | Nombre d'éléments : {nombre_elements}")

    load_button.clicked.connect(load_file_in_app)
    window.input.returnPressed.connect(load_file_in_app)


    def update_display(text):

        # Sert à ignorer les majuscules quand on cherche les fichiers dans le tableau.

        search = text.strip().casefold()

        # Vérifie chaque row pour voir si le text est dans une des colonnes.

        for row in range(window.tableau.rowCount()):

            # On assume que le contient_text est faux pas défaut.

            contient_text = False
            
            # Vérifie chaque column du row pour voir si elles contientennes le texte.

            for column in range(window.tableau.columnCount()):

             item = window.tableau.item(row, column)

             if item and search in item.text().casefold():

                   contient_text = True

            # Cacher ou afficher la ligne selon la recherche

            window.tableau.setRowHidden(row, not contient_text)

    # Crée une searchbar pour accéder au données du tableau plus facilement.

    window.searchbar = QLineEdit()
    window.searchbar.setPlaceholderText("Rechercher")
    window.searchbar.textChanged.connect(update_display)
    window.container_layout.addWidget(window.searchbar)

    # On cache la search bar parce que sinon elle apparaissait avant qu'on entre le chemin d'accès du fichier.

    window.searchbar.hide()
    
    # Pour afficher les infos du fichier en bas et au milieu de l'app.

    window.status_label = QLabel()
    window.status_label.setAlignment(Qt.AlignCenter)
    window.statusBar().addWidget(window.status_label, 1)
# Application
app = QApplication([]) # Crée l'app
window = QMainWindow() # Crée la window
creating_window(window) # Rempli la window
window.show() # Affiche la window
sys.exit(app.exec()) # Ferme l'app