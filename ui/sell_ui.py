import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSpinBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt

from utils.filehandler import read_csv, write_csv
from Medicine.medicine_functions import load_medicines, reduce_stock

SALES_FILE = "dataset/sales.csv"


class SellTab(QWidget):
    def __init__(self):
        super().__init__()
        self.cart = []
        self.init_ui()
        self.load_medicines()

    def init_ui(self):
        main = QVBoxLayout(self)
        main.setSpacing(14)

        customer_layout = QHBoxLayout()
        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("Customer Name")

        date_label = QLabel(datetime.now().strftime("%Y-%m-%d"))
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        customer_layout.addWidget(QLabel("Customer:"))
        customer_layout.addWidget(self.customer_input)
        customer_layout.addStretch()
        customer_layout.addWidget(QLabel("Date:"))
        customer_layout.addWidget(date_label)

        main.addLayout(customer_layout)

        selector = QHBoxLayout()

        self.medicine_combo = QComboBox()
        self.price_label = QLabel("Price: Rs.0")
        self.stock_label = QLabel("Stock: 0")

        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setMaximum(1000)

        add_btn = QPushButton("➕ Add to Cart")
        add_btn.clicked.connect(self.add_to_cart)

        selector.addWidget(QLabel("Medicine"))
        selector.addWidget(self.medicine_combo, 2)
        selector.addWidget(self.price_label)
        selector.addWidget(self.stock_label)
        selector.addWidget(QLabel("Qty"))
        selector.addWidget(self.qty_spin)
        selector.addWidget(add_btn)

        main.addLayout(selector)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Medicine", "Price", "Quantity", "Total", "Remove"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        main.addWidget(self.table)

        summary = QHBoxLayout()
        self.total_label = QLabel("Grand Total: Rs. 0")
        self.total_label.setStyleSheet("font-size:16px;font-weight:bold;")

        checkout_btn = QPushButton("✅ Complete Sale")
        checkout_btn.setFixedHeight(40)
        checkout_btn.clicked.connect(self.complete_sale)

        summary.addStretch()
        summary.addWidget(self.total_label)
        summary.addSpacing(20)
        summary.addWidget(checkout_btn)

        main.addLayout(summary)

    def load_medicines(self):
        self.medicines = load_medicines()[1:]
        self.medicine_combo.clear()

        for m in self.medicines:
            self.medicine_combo.addItem(m[1], m)

        self.medicine_combo.currentIndexChanged.connect(self.update_info)
        self.update_info()

    def update_info(self):
        med = self.medicine_combo.currentData()
        if med:
            self.price_label.setText(f"Price: Rs.{med[2]}")
            self.stock_label.setText(f"Stock: {med[3]}")
            self.qty_spin.setMaximum(int(med[3]))

    def add_to_cart(self):
        med = self.medicine_combo.currentData()
        qty = self.qty_spin.value()

        if not med:
            return

        name, price = med[1], float(med[2])

        for item in self.cart:
            if item["name"] == name:
                QMessageBox.warning(self, "Duplicate", "Medicine already in cart")
                return

        total = price * qty
        self.cart.append({
            "name": name,
            "price": price,
            "qty": qty,
            "total": total
        })

        self.refresh_table()

    def remove_item(self, row):
        self.cart.pop(row)
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        grand = 0

        for row, item in enumerate(self.cart):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["price"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["qty"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item["total"])))

            btn = QPushButton("❌")
            btn.clicked.connect(lambda _, r=row: self.remove_item(r))
            self.table.setCellWidget(row, 4, btn)

            grand += item["total"]

        self.total_label.setText(f"Grand Total: Rs. {grand}")

    def complete_sale(self):
        customer = self.customer_input.text().strip()

        if not customer or not self.cart:
            QMessageBox.warning(self, "Missing Info", "Customer or cart empty")
            return

        bill_id = int(datetime.now().timestamp())
        date = datetime.now().strftime("%Y-%m-%d")

        try:
            sales = read_csv(SALES_FILE)
        except:
            sales = [["bill_id", "customer", "medicine", "qty", "price", "total", "date"]]

        for item in self.cart:
            if not reduce_stock(item["name"], item["qty"]):
                return

            sales.append([
                bill_id,
                customer,
                item["name"],
                item["qty"],
                item["price"],
                item["total"],
                date
            ])

        write_csv(SALES_FILE, sales)

        QMessageBox.information(self, "Success", f"Bill #{bill_id} completed!")
        self.cart.clear()
        self.refresh_table()
        self.customer_input.clear()