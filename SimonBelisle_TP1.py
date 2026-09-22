import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem
)

json_file = sys.argv[1]
print("JSON FILE *****" + json_file)

try:
    file = open(json_file)
    data = json.load(file)
    print(type(data))
except:
    print(f"Could not load data from {json_file}")

for i in data:
    for k in i.values():
        print(f"    - {k}")
app = QApplication([])

tableau = QTableWidget()
tableau.setRowCount(3)
tableau.setColumnCount(3)
tableau.setHorizontalHeaderLabels(["name", "price", "type"])

# Fill the form
for i in range(len(data)):
    item = data[i]
    tableau.setItem(i, 0, QTableWidgetItem(item["name"]))
    tableau.setItem(i, 1, QTableWidgetItem(item["price"]))
    tableau.setItem(i, 2, QTableWidgetItem(item["type"]))

window = QMainWindow();
window.show()
sys.exit(app.exec())