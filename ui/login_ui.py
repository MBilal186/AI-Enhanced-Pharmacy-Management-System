import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QApplication
)
import csv

from ui.medicine_ui import current_user_role
from ui.main_windows import MainWindow


class LoginWindow(QWidget):
    def __init__(self, role=None):       # <-- NOW ACCEPTS ROLE
        super().__init__()
        self.role = role                 # <-- STORE ROLE
        self.setWindowTitle("Doctor Python Login")
        self.setGeometry(500, 200, 300, 260)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Show role chosen (Employee / Customer)
        if self.role:
            role_label = QLabel(f"{self.role} Login")
            role_label.setStyleSheet("font-size: 18px; font-weight: bold;")
            layout.addWidget(role_label)

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.handle_login)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        user_data = self.check_credentials(username, password)

        if user_data:
            global current_user_role
            current_user_role = user_data['role']

            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def check_credentials(self, username, password):
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "dataset",
            "employees.csv"
        )

        try:
            with open(csv_path, newline="", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    row = {k.strip(): v.strip() for k, v in row.items()}

                    # Role filter
                    if self.role and row.get("role") != self.role:
                        continue

                    if row.get("username") == username and row.get("password") == password:
                        return row

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"{csv_path} file not found!")

        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow(role="Employee")  # <- For manual test
    window.show()
    sys.exit(app.exec())
