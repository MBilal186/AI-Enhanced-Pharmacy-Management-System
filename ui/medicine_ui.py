# ui/medicine_ui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from Medicine.medicine_functions import load_medicines, save_medicines

class MedicineTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- Search Bar ---
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search medicine by name...")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_medicine)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_table)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(refresh_btn)

        layout.addLayout(search_layout)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Quantity", "Expiry"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_medicine_ui)
        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.update_medicine_ui)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_medicine_ui)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_table()

    def load_table(self):
        self.table.setRowCount(0)
        self.medicines = load_medicines()
        for row_idx, row in enumerate(self.medicines):
            self.table.insertRow(row_idx)
            for col_idx, item in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def search_medicine(self):
        keyword = self.search_input.text().lower()
        if not keyword:
            self.load_table()
            return
        self.table.setRowCount(0)
        for row_idx, row in enumerate(self.medicines):
            if keyword in row[1].lower():
                self.table.insertRow(self.table.rowCount())
                for col_idx, item in enumerate(row):
                    self.table.setItem(self.table.rowCount()-1, col_idx, QTableWidgetItem(str(item)))

    # --- GUI Input for Add ---
    def add_medicine_ui(self):
        data = load_medicines()
        # Generate new ID
        new_id = str(len(data))
        name, ok1 = QInputDialog.getText(self, "Add Medicine", "Name:")
        if not ok1 or not name.strip():
            return
        price, ok2 = QInputDialog.getDouble(self, "Add Medicine", "Price:", min=0)
        if not ok2:
            return
        qty, ok3 = QInputDialog.getInt(self, "Add Medicine", "Quantity:", min=0)
        if not ok3:
            return
        exp, ok4 = QInputDialog.getText(self, "Add Medicine", "Expiry (YYYY-MM-DD):")
        if not ok4 or not exp.strip():
            return

        new_row = [new_id, name, price, qty, exp]
        data.append(new_row)
        save_medicines(data)
        QMessageBox.information(self, "Success", f"Medicine '{name}' added successfully!")
        self.load_table()

    # --- GUI Input for Update ---
    def update_medicine_ui(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Please select a medicine to update.")
            return

        data = load_medicines()
        row = data[selected]

        # Prompt user for new values (leave empty to keep old)
        name, ok1 = QInputDialog.getText(self, "Update Medicine", f"Name [{row[1]}]:")
        if ok1 and name.strip():
            row[1] = name
        price, ok2 = QInputDialog.getDouble(self, "Update Medicine", f"Price [{row[2]}]:", value=float(row[2]), min=0)
        if ok2:
            row[2] = price
        qty, ok3 = QInputDialog.getInt(self, "Update Medicine", f"Quantity [{row[3]}]:", value=int(row[3]), min=0)
        if ok3:
            row[3] = qty
        exp, ok4 = QInputDialog.getText(self, "Update Medicine", f"Expiry [{row[4]}]:")
        if ok4 and exp.strip():
            row[4] = exp

        data[selected] = row
        save_medicines(data)
        QMessageBox.information(self, "Success", f"Medicine '{row[1]}' updated successfully!")
        self.load_table()

    # --- GUI Input for Delete ---
    def delete_medicine_ui(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Please select a medicine to delete.")
            return

        data = load_medicines()
        row = data[selected]
        confirm = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete '{row[1]}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            data.pop(selected)
            save_medicines(data)
            QMessageBox.information(self, "Deleted", f"Medicine '{row[1]}' deleted successfully!")
            self.load_table()
