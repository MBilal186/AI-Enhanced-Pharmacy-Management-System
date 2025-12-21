# ui/startup_ui.py
import sys, os, math, random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QRadialGradient
from PyQt6.QtCore import Qt, QTimer, QPointF

from ui.login_ui import LoginWindow

# -------------------------
# Particle model
# -------------------------
class Particle:
    def __init__(self, w, h):
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.15, 0.9)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = random.uniform(2.5, 6.5)
        self.hue = random.uniform(190, 220)
        self.alpha = random.uniform(0.35, 0.95)

    def move(self, w, h):
        self.x += self.vx
        self.y += self.vy
        border = 20
        if self.x < -border: self.x = w + border
        elif self.x > w + border: self.x = -border
        if self.y < -border: self.y = h + border
        elif self.y > h + border: self.y = -border

# -------------------------
# Particle splash
# -------------------------
class ParticleSplash(QWidget):
    def __init__(self, parent=None, particle_count=90):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self.on_timer)
        self.particle_count = particle_count
        self._initialized = False

    def start(self):
        if not self._initialized:
            self._init_particles()
            self._initialized = True
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def _init_particles(self):
        w, h = max(1, self.width()), max(1, self.height())
        self.particles = [Particle(w, h) for _ in range(self.particle_count)]

    def resizeEvent(self, e):
        self._initialized = False
        if self.isVisible():
            self._init_particles()
        super().resizeEvent(e)

    def on_timer(self):
        w, h = max(1, self.width()), max(1, self.height())
        for p in self.particles:
            p.vx += random.uniform(-0.02, 0.02)
            p.vy += random.uniform(-0.02, 0.02)
            max_speed = 1.6
            speed = math.hypot(p.vx, p.vy)
            if speed > max_speed:
                scale = max_speed / speed
                p.vx *= scale
                p.vy *= scale
            p.move(w, h)
            p.alpha = min(1.0, max(0.2, p.alpha + random.uniform(-0.01, 0.01)))
            p.size = max(1.5, min(8.0, p.size + random.uniform(-0.08, 0.08)))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(6, 10, 15))
        self._draw_subtle_grid(painter)
        for p in self.particles:
            self._draw_particle(painter, p)

    def _draw_particle(self, painter, p: Particle):
        cx, cy = p.x, p.y
        size = p.size
        rg = QRadialGradient(QPointF(cx, cy), size * 6)
        color_center = QColor.fromHsvF(p.hue / 360.0, 0.9, 1.0, p.alpha)
        color_mid = QColor.fromHsvF(p.hue / 360.0, 0.9, 0.6, p.alpha * 0.45)
        color_edge = QColor(10, 20, 30, 0)
        rg.setColorAt(0.0, color_center)
        rg.setColorAt(0.15, color_mid)
        rg.setColorAt(1.0, color_edge)
        painter.setBrush(rg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(cx, cy), size * 4, size * 4)
        core_color = QColor.fromHsvF(p.hue / 360.0, 0.95, 1.0, min(1.0, p.alpha + 0.15))
        pen = QPen(core_color)
        pen.setWidthF(0.6)
        painter.setPen(pen)
        painter.setBrush(core_color)
        painter.drawEllipse(QPointF(cx, cy), size, size)

    def _draw_subtle_grid(self, painter):
        pen = QPen(QColor(255, 255, 255, 6))
        pen.setWidth(1)
        painter.setPen(pen)
        w, h = self.width(), self.height()
        step = 120
        for x in range(-step, w + step, step):
            painter.drawLine(x, 0, x - w, h)
        grad = QRadialGradient(QPointF(self.rect().center()), max(w, h) * 0.9)
        grad.setColorAt(0.0, QColor(0, 0, 0, 0))
        grad.setColorAt(0.7, QColor(0, 0, 0, 120))
        grad.setColorAt(1.0, QColor(0, 0, 0, 200))
        painter.setBrush(grad)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

# -------------------------
# Startup screen
# -------------------------
class StartupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doctor Python")
        self.setGeometry(320, 120, 980, 640)
        self.particles = ParticleSplash(self, particle_count=100)
        self.particles.setGeometry(0, 0, self.width(), self.height())

        self.title_label = QLabel("Doctor Python", self)
        self.title_label.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #e6f7ff;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle = QLabel("AI-powered Pharmacy — The Pharmacy That Talks Back", self)
        self.subtitle.setFont(QFont("Segoe UI", 14))
        self.subtitle.setStyleSheet("color: rgba(230,247,255,0.75);")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_continue = QPushButton("Continue", self)
        self.btn_continue.setFixedSize(220, 58)
        self.btn_continue.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self.btn_continue.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_continue.setStyleSheet("""
            QPushButton{
                border-radius: 29px;
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #00e5ff, stop:1 #0066ff);
                color: white;
                padding: 12px;
            }
            QPushButton:hover{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #3fe7ff, stop:1 #1780ff);
            }
            QPushButton:pressed{
                padding-left:2px; padding-top:2px;
            }
        """)
        self.btn_continue.clicked.connect(self.on_continue)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(10, 30, 80, 180))
        self.title_label.setGraphicsEffect(shadow)

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(40, 48, 40, 40)
        vbox.setSpacing(18)
        vbox.addStretch()
        vbox.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addSpacing(18)
        vbox.addWidget(self.btn_continue, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch()

        self.particles.start()
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.Resize:
            self.particles.setGeometry(0, 0, self.width(), self.height())
        return super().eventFilter(obj, event)

    def on_continue(self):
        self.role_screen = RoleSelectionScreen()
        self.role_screen.show()
        self.particles.stop()
        self.close()

# -------------------------
# Role selection screen
# -------------------------
class RoleSelectionScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Role")
        self.setGeometry(420, 170, 640, 420)
        self.setStyleSheet("background-color: #0f1724; color: #e6f7ff;")
        self.init_ui()

    def init_ui(self):
        title = QLabel("Who are you?", self)
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #cfefff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Choose a role to continue", self)
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: rgba(207,239,255,0.7);")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # buttons
        btn_customer = QPushButton("Customer")
        btn_employee = QPushButton("Employee")
        btn_admin = QPushButton("Admin")

        for btn, color1, color2 in [
            (btn_customer, "#041f6b", "#0078d7"),
            (btn_employee, "#002b36", "#00c2ff"),
            (btn_admin, "#7f00ff", "#e100ff")
        ]:
            btn.setFixedSize(180, 72)
            btn.setStyleSheet(f"""
                QPushButton{{ background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {color1}, stop:1 {color2});
                                 color: white; border-radius:12px; font-weight:600; }}
                QPushButton:hover{{ transform: translateY(-2px); }}
            """)

        btn_customer.clicked.connect(self.open_customer)
        btn_employee.clicked.connect(self.open_employee)
        btn_admin.clicked.connect(self.open_admin)

        v = QVBoxLayout(self)
        v.addStretch()
        v.addWidget(title)
        v.addWidget(subtitle)
        v.addSpacing(24)

        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(btn_customer)
        h.addSpacing(20)
        h.addWidget(btn_employee)
        h.addSpacing(20)
        h.addWidget(btn_admin)
        h.addStretch()
        v.addLayout(h)
        v.addStretch()
        v.setContentsMargins(24, 24, 24, 24)

    def open_employee(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_customer(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_admin(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

# -------------------------
# Run entrypoint
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = StartupScreen()
    s.show()
    sys.exit(app.exec())
