import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton
)
from ui.medicine_ui import MedicineTab
from ui.sales_ui import SalesHistoryTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Based Pharmacy Management System")
        self.resize(1100, 700)

        # ---- FIXED PREMIUM THEME ----
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f6f9;
                color: #2d2d2d;
                font-size: 14px;
                font-family: 'Segoe UI';
            }

            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: #ffffff;
                padding: 8px;
            }

            QTabBar::tab {
                background: #e0e0e0;
                color: #333333;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 6px;
                font-weight: 500;
            }

            QTabBar::tab:hover {
                background: #d0d0d0;
                color: #000000;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                color: #0078d7;
                font-weight: bold;
                border: 1px solid #bbbbbb;
            }

            QWidget {
                background: #ffffff;
                color: #333333;
            }

            QLineEdit, QComboBox {
                padding: 7px;
                border: 1px solid #cccccc;
                border-radius: 6px;
                background: #fdfdfd;
            }

            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 10px 14px;
                border: none;
                border-radius: 6px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #005fa3;
            }

            QTableWidget {
                background: white;
                gridline-color: #dddddd;
                color: #333333;
                selection-background-color: #0078d7;
                selection-color: white;
            }
        """)

        # ---- MAIN LAYOUT FOR SIDEBAR + TABS ----
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -------------------------
        # SIDEBAR
        # -------------------------
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(18)

        btn_dashboard = QPushButton("📊 Dashboard")
        btn_medicine = QPushButton("💊 Medicines")
        btn_sales = QPushButton("💸 Sales History")
        btn_settings = QPushButton("⚙️ Settings")

        for btn in [btn_dashboard, btn_medicine, btn_sales, btn_settings]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495E;
                    color: white;
                    padding: 10px;
                    border-radius: 8px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3d566e;
                }
            """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # -------------------------
        # TABS AREA
        # -------------------------
        self.tabs = QTabWidget()
        self.tabs.addTab(MedicineTab(), "Medicines")
        self.tabs.addTab(SalesHistoryTab(), "Sales History")

        # Connect sidebar buttons → tab index
        btn_medicine.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        btn_sales.clicked.connect(lambda: self.tabs.setCurrentIndex(1))

        # (Dashboard & Settings will be added later)

        # Add sidebar + tabs to layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.tabs)

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
