# ui/sales_ui.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from utils.filehandler import read_csv
from PyQt6.QtCore import Qt

SALES_FILE = "dataset/sales.csv"

class SalesHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Sale ID", "Customer", "Medicine", "Qty", "Price", "Total", "Date"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_sales)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)
        self.load_sales()

    def load_sales(self):
        try:
            data = read_csv(SALES_FILE)
        except Exception:
            self.table.setRowCount(0)
            return

        # Ensure header exists
        if not data or len(data[0]) < 7:
            self.table.setRowCount(0)
            return

        header = data[0]
        rows = data[1:]  # skip header

        self.table.setRowCount(0)
        for r_idx, row in enumerate(rows):
            self.table.insertRow(r_idx)
            for c_idx, value in enumerate(row):
                self.table.setItem(r_idx, c_idx, QTableWidgetItem(str(value)))
