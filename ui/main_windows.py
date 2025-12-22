# ui/main_windows.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from ui.dashboard_ui import DashboardTab
from ui.medicine_ui import MedicineTab
from ui.sales_ui import SalesHistoryTab
from ui.sell_ui import SellTab
from ui.ai_support_ui import AISupportTab
from ui.cashier_ui import CashierTab

class MainWindow(QMainWindow):
    def __init__(self, role=None):
        super().__init__()
        self.role = role.lower() if role else ""
        self.setWindowTitle("AI-Based Pharmacy Management System")
        self.resize(1100, 700)

        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- Sidebar ----------------
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #1f2a36;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 20, 14, 20)
        sidebar_layout.setSpacing(10)

        title = QLabel("Doctor Python")
        title.setStyleSheet("color: #ecf0f1; font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        # Sidebar buttons
        btn_dashboard = QPushButton("📊 Dashboard")
        btn_medicine = QPushButton("💊 Medicines")
        btn_sell = QPushButton("🛒 Sell Medicine")
        btn_sales = QPushButton("💸 Sales History")
        btn_ai = QPushButton("🤖 AI Support")
        btn_cashier = QPushButton("👤 Cashiers")

        self.sidebar_buttons = [btn_dashboard, btn_medicine, btn_sell, btn_sales, btn_ai, btn_cashier]
        for btn in self.sidebar_buttons:
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; color: #ecf0f1;
                    padding: 14px 18px; border-radius: 8px; text-align: left; font-size: 14px;
                }
                QPushButton:hover { background-color: #2f3f4f; }
                QPushButton:checked { background-color: #1abc9c; color: #0b2e2e; font-weight: bold; }
            """)
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()

        # ---------------- Tabs ----------------
        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()

        self.dashboard_tab = DashboardTab()
        self.medicine_tab = MedicineTab(role=self.role)
        self.sell_tab = SellTab()
        self.sales_tab = SalesHistoryTab()
        self.ai_tab = AISupportTab()
        self.cashier_tab = CashierTab() if self.role == "admin" else None

        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        settings_label = QLabel("⚙️ Settings\n\nSystem & role management")
        settings_layout.addWidget(settings_label)

        # Add tabs in fixed order
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.medicine_tab, "Medicines")
        self.tabs.addTab(self.sell_tab, "Sell")
        self.tabs.addTab(self.sales_tab, "Sales History")
        self.tabs.addTab(self.ai_tab, "AI Support")
        if self.role == "admin":
            self.tabs.addTab(self.cashier_tab, "Cashiers")
        self.tabs.addTab(settings_tab, "Settings")

        # ---------------- Role-based access ----------------
        self.apply_role_restrictions()

        # ---------------- Sidebar navigation ----------------
        def activate(btn, index):
            for b in self.sidebar_buttons:
                b.setChecked(False)
            btn.setChecked(True)
            self.tabs.setCurrentIndex(index)

        btn_dashboard.clicked.connect(lambda: activate(btn_dashboard, 0))
        btn_medicine.clicked.connect(lambda: activate(btn_medicine, 1))
        btn_sell.clicked.connect(lambda: activate(btn_sell, 2))
        btn_sales.clicked.connect(lambda: activate(btn_sales, 3))
        btn_ai.clicked.connect(lambda: activate(btn_ai, 4))
        if self.role == "admin":
            btn_cashier.clicked.connect(lambda: activate(btn_cashier, 5))

        # ---------------- Default tab ----------------
        if self.role == "admin":
            btn_dashboard.setChecked(True)
            self.tabs.setCurrentIndex(0)
        else:
            btn_medicine.setChecked(True)
            self.tabs.setCurrentIndex(1)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.tabs)
        self.setCentralWidget(container)

    def apply_role_restrictions(self):
        # Disable tabs/buttons based on role
        if self.role == "cashier":
            # Cashier sees only Medicines and Sell
            for i in [0, 3, 4, 5, 6]:
                self.tabs.setTabEnabled(i, False)
                if i < len(self.sidebar_buttons):
                    self.sidebar_buttons[i].setEnabled(False)
        elif self.role == "customer":
            # Customer sees only Medicines
            for i in [0, 2, 3, 4, 5, 6]:
                self.tabs.setTabEnabled(i, False)
                if i < len(self.sidebar_buttons):
                    self.sidebar_buttons[i].setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(role="admin")  # Example: admin / cashier / customer
    window.show()
    sys.exit(app.exec())
