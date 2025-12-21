# ui/ai_support_ui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor


class AISupportTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0f0f1a;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # ---------- HEADER ----------
        header = QLabel("🤖 AI Support Chat")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00ffff;
            background-color: #1a001a;
            padding: 12px;
            border-radius: 14px;
            border: 2px solid #3498db;
        """)
        layout.addWidget(header)

        # ---------- CHAT AREA ----------
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #0f0f1a;
                border-radius: 14px;
                padding: 12px;
                font-size: 14px;
                color: #ffffff;
            }
        """)
        layout.addWidget(self.chat_area, stretch=1)

        # ---------- INPUT ----------
        input_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Describe your symptoms...")
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: #1a001a;
                border: 2px solid #3498db;
                border-radius: 14px;
                padding: 10px;
                font-size: 14px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #00ffff;
            }
        """)
        self.input_box.returnPressed.connect(self.send_message)

        send_btn = QPushButton("Send")
        send_btn.setFixedWidth(110)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #0f0f1a;
                font-weight: bold;
                border-radius: 14px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)

    # ---------- USER BUBBLE (RIGHT / YELLOW) ----------
    def user_bubble(self, message):
        self.chat_area.append(f"""
        <table width="100%" cellspacing="0" cellpadding="8">
            <tr>
                <td></td>
                <td align="right">
                    <div style="
                        background-color:#f1c40f;
                        color:#0f0f1a;
                        padding:14px;
                        border-radius:22px;
                        max-width:420px;
                        display:inline-block;
                        overflow:hidden;
                        font-weight:600;
                        box-shadow:0 0 6px rgba(241,196,15,0.6);
                    ">
                        {message}
                    </div>
                </td>
            </tr>
        </table>
        """)
        self.scroll()

    # ---------- AI BUBBLE (LEFT / LIGHT BLUE) ----------
    def ai_bubble(self, message):
        self.chat_area.append(f"""
        <table width="100%" cellspacing="0" cellpadding="8">
            <tr>
                <td align="left">
                    <div style="
                        background-color:#4cc9f0;
                        color:#0f0f1a;
                        padding:14px;
                        border-radius:22px;
                        max-width:420px;
                        display:inline-block;
                        overflow:hidden;
                        font-weight:600;
                        box-shadow:0 0 6px rgba(76,201,240,0.6);
                    ">
                        {message}
                    </div>
                </td>
                <td></td>
            </tr>
        </table>
        """)
        self.scroll()

    # ---------- TYPING ----------
    def typing_indicator(self):
        self.chat_area.append("""
        <table width="100%" cellpadding="6">
            <tr>
                <td align="left">
                    <span style="color:#00ffff;font-style:italic;font-weight:600;">
                        AI is typing...
                    </span>
                </td>
            </tr>
        </table>
        """)
        self.scroll()

    def remove_typing(self):
        cursor = self.chat_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()

    def scroll(self):
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)

    # ---------- SEND ----------
    def send_message(self):
        msg = self.input_box.text().strip()
        if not msg:
            return

        self.user_bubble(msg)
        self.input_box.clear()
        self.typing_indicator()

        QTimer.singleShot(1200, lambda: self.ai_reply(msg))

    # ---------- AI REPLY ----------
    def ai_reply(self, user_msg):
        self.remove_typing()
        reply = self.rule_based_ai(user_msg)
        self.ai_bubble(reply)

    # ---------- MEDICAL RULE-BASED AI ----------
    def rule_based_ai(self, text):
        text = text.lower()

        if "fever" in text:
            return "🩺 Recommended Medicine:\n• Paracetamol 500mg\n\nPlease ensure adequate hydration."
        elif "pain" in text or "headache" in text:
            return "🩺 Recommended Medicine:\n• Ibuprofen 400mg\n\nAvoid on empty stomach."
        elif "cough" in text:
            return "🩺 Recommended Medicine:\n• Dextromethorphan Cough Syrup"
        elif "cold" in text or "flu" in text:
            return "🩺 Recommended Medicine:\n• Antiflu\n• Vitamin C Chewable"
        elif "allergy" in text or "rash" in text:
            return "🩺 Recommended Medicine:\n• Cetirizine 10mg"
        elif "vomit" in text or "nausea" in text:
            return "🩺 Recommended Medicine:\n• Ondansetron 4mg"
        elif "diarrhea" in text:
            return "🩺 Recommended Medicine:\n• Loperamide 2mg\n• Oral Rehydration Salts"
        elif "acid" in text or "gas" in text:
            return "🩺 Recommended Medicine:\n• Omeprazole 20mg"
        elif "hello" in text or "hi" in text:
            return "Hello! Please describe your symptoms and I will recommend suitable medicine."
        else:
            return (
                "⚠️ No exact match found.\n\n"
                "Please consult a pharmacist or doctor for accurate diagnosis."
            )
