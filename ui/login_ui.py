import sys, os, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QApplication
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from ui.main_windows import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doctor Python — Login")
        self.setFixedSize(360, 420)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #0b1220; color: #e6f7ff; }
            QLabel { color: #cfefff; }
            QLineEdit {
                background-color: #111a2e;
                border: 1px solid #1f3b57;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus { border: 1px solid #00c2ff; }
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00c2ff, stop:1 #0066ff
                );
                border-radius: 22px;
                padding: 12px;
                font-weight: 600;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3fe7ff, stop:1 #1780ff
                );
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)

        title = QLabel("Doctor Python")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Login")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: rgba(207,239,255,0.7);")

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Username")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Secure Login")
        self.btn_login.clicked.connect(self.handle_login)

        layout.addWidget(self.input_username)
        layout.addWidget(self.input_password)
        layout.addSpacing(18)
        layout.addWidget(self.btn_login)
        layout.addSpacing(12)

        btn_customer = QPushButton("Continue as Customer")
        btn_customer.setStyleSheet("""
            QPushButton { background-color: #1abc9c; color: white; border-radius: 22px; padding: 12px; font-weight: 600; }
            QPushButton:hover { background-color: #16a085; }
        """)
        btn_customer.clicked.connect(self.continue_as_customer)
        layout.addWidget(btn_customer)

        layout.addStretch()

    def handle_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Missing Info", "Please enter username and password.")
            return

        user_data = self.check_credentials(username, password)

        if user_data:
            user_role = user_data["role"].lower()  
            self.main_window = MainWindow(role=user_role)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

    def check_credentials(self, username, password):
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "dataset",
            "users.csv"
        )

        try:
            with open(csv_path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row = {k.strip().lower(): v.strip() for k, v in row.items()}
                    if row.get("username") == username and row.get("password") == password:
                        return row
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "users.csv not found")

        return None

    def continue_as_customer(self):
        self.main_window = MainWindow(role="customer")
        self.main_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())
