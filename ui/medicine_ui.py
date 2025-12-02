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

SALES_FILE = "dataset/sales.csv"  # will be created if missing

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
        sell_btn = QPushButton("Sell")                # <-- SELL button
        sell_btn.clicked.connect(self.sell_medicine_ui)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(sell_btn)
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
            # defensive: ensure row has at least 2 columns (id,name,...)
            name = str(row[1]) if len(row) > 1 else ""
            if keyword in name.lower():
                self.table.insertRow(self.table.rowCount())
                for col_idx, item in enumerate(row):
                    self.table.setItem(self.table.rowCount()-1, col_idx, QTableWidgetItem(str(item)))

    # --- GUI Input for Add ---
    def add_medicine_ui(self):
        data = load_medicines()
        # Generate new ID (preserve existing format if possible)
        # If first row is header, ID count should be len(data)-1
        new_id = f"M{len(data)+1:03d}"
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

        new_row = [new_id, name.strip(), str(price), str(qty), exp.strip()]
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
        # if CSV has header, be careful — this implementation assumes rows match table rows
        row = data[selected]

        name, ok1 = QInputDialog.getText(self, "Update Medicine", f"Name [{row[1]}]:", text=str(row[1]))
        if ok1 and name.strip():
            row[1] = name.strip()

        try:
            current_price = float(row[2])
        except Exception:
            current_price = 0.0
        price, ok2 = QInputDialog.getDouble(self, "Update Medicine", f"Price [{row[2]}]:", value=current_price, min=0)
        if ok2:
            row[2] = str(price)

        try:
            current_qty = int(row[3])
        except Exception:
            current_qty = 0
        qty, ok3 = QInputDialog.getInt(self, "Update Medicine", f"Quantity [{row[3]}]:", value=current_qty, min=0)
        if ok3:
            row[3] = str(qty)

        exp, ok4 = QInputDialog.getText(self, "Update Medicine", f"Expiry [{row[4]}]:", text=str(row[4]))
        if ok4 and exp.strip():
            row[4] = exp.strip()

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

    # --- SELL / BILLING (NEW FEATURE) ---
    def sell_medicine_ui(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Please select a medicine to sell.")
            return

        data = load_medicines()
        row = data[selected]
        med_id = str(row[0])
        med_name = str(row[1])
        try:
            price = float(row[2])
        except Exception:
            QMessageBox.warning(self, "Error", "Invalid price stored for this medicine.")
            return
        try:
            available_qty = int(row[3])
        except Exception:
            QMessageBox.warning(self, "Error", "Invalid quantity stored for this medicine.")
            return

        # get customer name
        customer, ok1 = QInputDialog.getText(self, "Customer Name", "Enter customer name:")
        if not ok1 or not customer.strip():
            return
        # get quantity to sell
        qty, ok2 = QInputDialog.getInt(self, "Quantity", f"Enter quantity to sell (Available: {available_qty}):", min=1)
        if not ok2:
            return
        if qty > available_qty:
            QMessageBox.warning(self, "Stock error", "Not enough stock available.")
            return

        total = round(price * qty, 2)

        # confirm sale
        confirm = QMessageBox.question(
            self, "Confirm Sale",
            f"Sell {qty} x {med_name} @ Rs.{price} each\nTotal: Rs.{total}\nTo customer: {customer} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        # update stock in data and save
        data[selected][3] = str(available_qty - qty)
        save_medicines(data)
        self.load_table()

        # record sale in SALES_FILE (create if not exist)
        self.record_sale(customer, med_name, qty, price, total)

        # show bill in dialog
        bill_text = (
            "====== BILL ======\n"
            f"Customer: {customer}\n"
            f"Medicine: {med_name}\n"
            f"Quantity: {qty}\n"
            f"Price per unit: Rs.{price}\n"
            f"Total Amount: Rs.{total}\n"
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "=================="
        )
        QMessageBox.information(self, "Sale Recorded", bill_text)

    def record_sale(self, customer, medicine_name, qty, price, total):
        # ensure dataset folder exists
        os.makedirs(os.path.dirname(SALES_FILE), exist_ok=True)
        # try to read existing sales
        try:
            sales = read_csv(SALES_FILE)
        except Exception:
            sales = []

        # if file empty or first row not header, add header
        if not sales or not (len(sales[0]) and str(sales[0][0]).lower().startswith("sale")):
            header = ["sale_id", "customer_name", "medicine_name", "quantity", "price", "total", "date"]
            sales = [header] + sales

        sale_id = len(sales)  # simple incremental id based on rows
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [sale_id, customer, medicine_name, qty, price, total, date_str]
        sales.append(new_row)
        write_csv(SALES_FILE, sales)
