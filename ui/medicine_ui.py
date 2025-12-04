# ui/medicine_ui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from Medicine.medicine_functions import load_medicines, save_medicines
from utils.filehandler import read_csv, write_csv
from datetime import datetime
import os
from functools import wraps

# -------------------- GLOBAL ROLE VARIABLE --------------------
current_user_role = None  # Will be set after login

# -------------------- ROLE DECORATOR --------------------
def require_role(allowed_roles):
    """
    Decorator to restrict access based on roles.
    Usage: @require_role(["Admin"]) or @require_role(["Admin", "Employee"])
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user_role not in allowed_roles:
                QMessageBox.warning(None, "Access Denied", f"Your role ({current_user_role}) cannot perform this action.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator

# -------------------- MEDICINE TAB --------------------
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
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_medicine_ui)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_medicine_ui)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_medicine_ui)
        self.sell_btn = QPushButton("Sell")
        self.sell_btn.clicked.connect(self.sell_medicine_ui)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.sell_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_table()
        self.adjust_ui_for_role()  # Hide buttons based on role

    # -------------------- Role-Based UI --------------------
    def adjust_ui_for_role(self):
        if current_user_role == "Customer":
            self.add_btn.hide()
            self.update_btn.hide()
            self.delete_btn.hide()
            self.sell_btn.hide()
        elif current_user_role == "Employee":
            self.delete_btn.hide()  # Employees cannot delete

    # -------------------- Table Load --------------------
    def load_table(self):
        self.table.setRowCount(0)
        self.medicines = load_medicines()

        if self.medicines and self.medicines[0][0].lower() == "id":
            self.medicines = self.medicines[1:]

        for row_idx, row in enumerate(self.medicines):
            self.table.insertRow(row_idx)
            med_id, name, price, qty, expiry = str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])
            for col_idx, val in enumerate([med_id, name, price, qty, expiry]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(val))

            # Highlight expired or low stock
            expired = False
            try:
                exp_date = datetime.strptime(expiry, "%Y-%m-%d")
                if exp_date < datetime.now():
                    expired = True
            except:
                pass

            for col in range(5):
                cell = self.table.item(row_idx, col)
                if expired:
                    cell.setBackground(Qt.GlobalColor.red)
                    cell.setForeground(Qt.GlobalColor.white)
                elif int(qty) < 10:
                    cell.setBackground(Qt.GlobalColor.yellow)
                    cell.setForeground(Qt.GlobalColor.black)

        # Alerts
        low_stock = [m for m in self.medicines if int(m[3]) < 10]
        expired_list = []
        for m in self.medicines:
            try:
                exp_date = datetime.strptime(m[4], "%Y-%m-%d")
                if exp_date < datetime.now():
                    expired_list.append(m)
            except:
                pass

        msg = ""
        if low_stock:
            msg += f"{len(low_stock)} medicines are LOW in stock!\n"
        if expired_list:
            msg += f"{len(expired_list)} medicines are EXPIRED!\n"

        if msg:
            QMessageBox.warning(self, "Inventory Alerts", msg)

    # -------------------- Search --------------------
    def search_medicine(self):
        keyword = self.search_input.text().lower()
        if not keyword:
            self.load_table()
            return
        self.table.setRowCount(0)
        for row in self.medicines:
            if keyword in str(row[1]).lower():
                row_index = self.table.rowCount()
                self.table.insertRow(row_index)
                for col_idx, item in enumerate(row):
                    self.table.setItem(row_index, col_idx, QTableWidgetItem(str(item)))

    # -------------------- Add Medicine --------------------
    @require_role(["Admin", "Employee"])
    def add_medicine_ui(self):
        data = load_medicines()
        new_id = f"M{len(data)+1:03d}"
        name, ok1 = QInputDialog.getText(self, "Add Medicine", "Name:")
        if not ok1 or not name.strip(): return
        price, ok2 = QInputDialog.getDouble(self, "Add Medicine", "Price:", min=0)
        if not ok2: return
        qty, ok3 = QInputDialog.getInt(self, "Add Medicine", "Quantity:", min=0)
        if not ok3: return
        exp, ok4 = QInputDialog.getText(self, "Add Medicine", "Expiry (YYYY-MM-DD):")
        if not ok4 or not exp.strip(): return
        data.append([new_id, name.strip(), str(price), str(qty), exp.strip()])
        save_medicines(data)
        QMessageBox.information(self, "Success", f"Medicine '{name}' added successfully!")
        self.load_table()

    # -------------------- Update Medicine --------------------
    @require_role(["Admin", "Employee"])
    def update_medicine_ui(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Please select a medicine to update.")
            return
        data = load_medicines()
        row = data[selected]

        name, ok1 = QInputDialog.getText(self, "Update Medicine", f"Name [{row[1]}]:", text=row[1])
        if ok1 and name.strip(): row[1] = name.strip()
        price, ok2 = QInputDialog.getDouble(self, "Update Medicine", f"Price [{row[2]}]:", value=float(row[2]), min=0)
        if ok2: row[2] = str(price)
        qty, ok3 = QInputDialog.getInt(self, "Update Medicine", f"Quantity [{row[3]}]:", value=int(row[3]), min=0)
        if ok3: row[3] = str(qty)
        exp, ok4 = QInputDialog.getText(self, "Update Medicine", f"Expiry [{row[4]}]:", text=row[4])
        if ok4 and exp.strip(): row[4] = exp.strip()
        data[selected] = row
        save_medicines(data)
        QMessageBox.information(self, "Updated", f"Medicine '{row[1]}' updated successfully!")
        self.load_table()

    # -------------------- Delete Medicine --------------------
    @require_role(["Admin"])
    def delete_medicine_ui(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Select a medicine to delete.")
            return
        data = load_medicines()
        row = data[selected]
        confirm = QMessageBox.question(self, "Confirm Delete", f"Delete '{row[1]}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            data.pop(selected)
            save_medicines(data)
            QMessageBox.information(self, "Deleted", f"Medicine '{row[1]}' deleted successfully!")
            self.load_table()

    # -------------------- Sell Medicine --------------------
    @require_role(["Admin", "Employee"])
    def sell_medicine_ui(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Select a medicine to sell.")
            return

        data = load_medicines()
        row = data[selected]
        med_id, med_name, price, available_qty = row[0], row[1], float(row[2]), int(row[3])

        customer, ok1 = QInputDialog.getText(self, "Customer Name", "Enter customer name:")
        if not ok1 or not customer.strip(): return

        qty, ok2 = QInputDialog.getInt(self, "Quantity", f"Enter quantity to sell (Available: {available_qty}):", min=1)
        if not ok2: return
        if qty > available_qty:
            QMessageBox.warning(self, "Stock Error", "Not enough stock!")
            return

        total = round(price * qty, 2)
        confirm = QMessageBox.question(self, "Confirm Sale",
                                       f"Sell {qty} x {med_name} @ Rs.{price}\nTotal: Rs.{total}\nTo: {customer}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm != QMessageBox.StandardButton.Yes: return

        # Update stock
        data[selected][3] = str(available_qty - qty)
        save_medicines(data)
        self.load_table()
        self.record_sale(customer, med_name, qty, price, total)

        bill_text = (
            "====== BILL ======\n"
            f"Customer: {customer}\n"
            f"Medicine: {med_name}\n"
            f"Qty: {qty}\n"
            f"Price/unit: Rs.{price}\n"
            f"Total: Rs.{total}\n"
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "=================="
        )
        QMessageBox.information(self, "Sale Recorded", bill_text)

    # -------------------- Record Sale --------------------
    def record_sale(self, customer, medicine_name, qty, price, total):
        SALES_FILE = "dataset/sales.csv"
        os.makedirs("dataset", exist_ok=True)

        try:
            sales = read_csv(SALES_FILE)
        except:
            sales = []

        if not sales or not (len(sales[0]) and str(sales[0][0]).lower().startswith("sale")):
            sales = [["sale_id", "customer_name", "medicine_name", "quantity", "price", "total", "date"]]

        sale_id = len(sales)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sales.append([sale_id, customer, medicine_name, qty, price, total, date_str])
        write_csv(SALES_FILE, sales)
