import os
import csv
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt

class CashierTab(QWidget):
    def __init__(self):
        super().__init__()
        self.csv_file = os.path.join(os.path.dirname(__file__), "../dataset/users.csv")
        self.init_ui()
        self.ensure_csv_exists()
        self.load_cashiers()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        header = QLabel("💼 Cashier Management")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(header)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Username", "Password", "Role"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, stretch=1)

        form_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.role_input = QLineEdit()
        self.role_input.setText("cashier")
        self.role_input.setReadOnly(True)  

        add_btn = QPushButton("Add Cashier")
        add_btn.clicked.connect(self.add_cashier)

        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.role_input)
        form_layout.addWidget(add_btn)
        layout.addLayout(form_layout)

        del_btn = QPushButton("Delete Selected Cashier")
        del_btn.clicked.connect(self.delete_cashier)
        layout.addWidget(del_btn)

    def ensure_csv_exists(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["username", "password", "role"])
                writer.writeheader()

    def load_cashiers(self):
        self.table.setRowCount(0)
        if not os.path.exists(self.csv_file):
            return
        with open(self.csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("role", "").lower() != "cashier":
                    continue  
                row_pos = self.table.rowCount()
                self.table.insertRow(row_pos)
                self.table.setItem(row_pos, 0, QTableWidgetItem(row.get("username", "")))
                self.table.setItem(row_pos, 1, QTableWidgetItem(row.get("password", "")))
                self.table.setItem(row_pos, 2, QTableWidgetItem(row.get("role", "")))

    def add_cashier(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = "cashier"

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and Password are required!")
            return

        with open(self.csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("username") == username:
                    QMessageBox.warning(self, "Duplicate", "Username already exists!")
                    return

        with open(self.csv_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password", "role"])
            writer.writerow({"username": username, "password": password, "role": role})

        QMessageBox.information(self, "Success", f"Cashier '{username}' added successfully!")
        self.username_input.clear()
        self.password_input.clear()
        self.load_cashiers()

    def delete_cashier(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select at least one cashier to delete.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete the selected cashier(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        users = []
        with open(self.csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)

        usernames_to_delete = [self.table.item(r, 0).text() for r in selected_rows]
        users = [u for u in users if u.get("username") not in usernames_to_delete]

        with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password", "role"])
            writer.writeheader()
            for row in users:
                writer.writerow(row)

        QMessageBox.information(self, "Deleted", "Selected cashier(s) deleted successfully!")
        self.load_cashiers()