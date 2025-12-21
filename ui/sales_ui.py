# ui/sales_ui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt
from utils.filehandler import read_csv

SALES_FILE = "dataset/sales.csv"


class SalesHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f4f6f9;")  # Page background
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ---------- Table ----------
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Sale ID", "Customer", "Medicine", "Qty", "Price", "Total", "Date"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # ---------- Styling ----------
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #eaf0f6;       /* Table background */
                border-radius: 10px;
                gridline-color: #dcdcdc;
                font-size: 13px;
                color: #2c3e50;                  /* Text color */
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #ecf0f1;
            }
        """)

        layout.addWidget(self.table)

        # ---------- Refresh Button ----------
        refresh_btn = QPushButton("🔄 Refresh Sales")
        refresh_btn.setFixedHeight(36)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #1f6692;
            }
        """)
        refresh_btn.clicked.connect(self.load_sales)
        layout.addWidget(refresh_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.load_sales()

    def load_sales(self):
        try:
            data = read_csv(SALES_FILE)
        except Exception:
            self.table.setRowCount(0)
            return

        if not data or len(data[0]) < 7:
            self.table.setRowCount(0)
            return

        rows = data[1:]  # skip header
        self.table.setRowCount(0)

        for r_idx, row in enumerate(rows):
            self.table.insertRow(r_idx)
            for c_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(r_idx, c_idx, item)
