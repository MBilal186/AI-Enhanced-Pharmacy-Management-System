import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from ui.medicine_ui import MedicineTab

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

            /* TAB BACKGROUND */
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: #ffffff;
                padding: 8px;
            }

            /* NORMAL TAB */
            QTabBar::tab {
                background: #e0e0e0;
                color: #333333;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 6px;
                font-weight: 500;
            }

            /* HOVER TAB */
            QTabBar::tab:hover {
                background: #d0d0d0;
                color: #000000;
            }

            /* SELECTED TAB */
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

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        tabs.addTab(MedicineTab(), "Medicines")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
