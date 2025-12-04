# ui/startup_ui.py
import sys, os, math, random
# Make project root discoverable so "from ui..." imports work when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QRadialGradient
from PyQt6.QtCore import Qt, QTimer, QPointF

# Import your existing windows (these must exist)
from ui.login_ui import LoginWindow
from ui.main_windows import MainWindow

# -------------------------
# Particle model
# -------------------------
class Particle:
    def __init__(self, w, h):
        # Initialize position randomly across the canvas
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        # Velocity small for gentle motion
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.15, 0.9)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        # size and color hue
        self.size = random.uniform(2.5, 6.5)
        self.hue = random.uniform(190, 220)  # blue-cyan range
        self.alpha = random.uniform(0.35, 0.95)

    def move(self, w, h):
        # gentle drift + wrap around edges
        self.x += self.vx
        self.y += self.vy

        border = 20
        if self.x < -border:
            self.x = w + border
        elif self.x > w + border:
            self.x = -border
        if self.y < -border:
            self.y = h + border
        elif self.y > h + border:
            self.y = -border

# -------------------------
# Animated Splash Widget
# -------------------------
class ParticleSplash(QWidget):
    def __init__(self, parent=None, particle_count=90):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.setInterval(16)  # ~60 FPS
        self.timer.timeout.connect(self.on_timer)
        self.particle_count = particle_count
        self._initialized = False

    def start(self):
        # Delay initialization until the widget has size
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
        # reinitialize particles to fit new size (keeps them distributed)
        self._initialized = False
        if self.isVisible():
            self._init_particles()
        super().resizeEvent(e)

    def on_timer(self):
        w, h = max(1, self.width()), max(1, self.height())
        # move particles and cause slight random flicker in alpha and small velocity noise
        for p in self.particles:
            # small noise
            p.vx += random.uniform(-0.02, 0.02)
            p.vy += random.uniform(-0.02, 0.02)
            # clamp speed
            max_speed = 1.6
            speed = math.hypot(p.vx, p.vy)
            if speed > max_speed:
                scale = max_speed / speed
                p.vx *= scale
                p.vy *= scale

            p.move(w, h)
            # subtle breathing in size/alpha
            p.alpha = min(1.0, max(0.2, p.alpha + random.uniform(-0.01, 0.01)))
            p.size = max(1.5, min(8.0, p.size + random.uniform(-0.08, 0.08)))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # base overlay (very dark)
        painter.fillRect(self.rect(), QColor(6, 10, 15))  # nearly black

        # Draw faint grid or lines (optional subtle tech-grid)
        self._draw_subtle_grid(painter)

        # draw particles with glow using radial gradients
        for p in self.particles:
            self._draw_particle(painter, p)

    def _draw_particle(self, painter, p: Particle):
        # center point
        cx, cy = p.x, p.y
        size = p.size
        # create radial gradient for glow
        rg = QRadialGradient(QPointF(cx, cy), size * 6)
        color_center = QColor.fromHsvF(p.hue / 360.0, 0.9, 1.0, p.alpha)
        color_mid = QColor.fromHsvF(p.hue / 360.0, 0.9, 0.6, p.alpha * 0.45)
        color_edge = QColor(10, 20, 30, 0)  # transparent
        rg.setColorAt(0.0, color_center)
        rg.setColorAt(0.15, color_mid)
        rg.setColorAt(1.0, color_edge)

        painter.setBrush(rg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(cx, cy), size * 4, size * 4)

        # bright core
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

        # FIXED — convert to QPointF
        grad = QRadialGradient(QPointF(self.rect().center()), max(w, h) * 0.9)

        grad.setColorAt(0.0, QColor(0, 0, 0, 0))
        grad.setColorAt(0.7, QColor(0, 0, 0, 120))
        grad.setColorAt(1.0, QColor(0, 0, 0, 200))

        painter.setBrush(grad)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())


# -------------------------
# Main startup screen (composition)
# -------------------------
class StartupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doctor Python")
        self.setGeometry(320, 120, 980, 640)
        # create layout layering: particle canvas behind, content on top
        self.particles = ParticleSplash(self, particle_count=100)
        self.particles.setGeometry(0, 0, self.width(), self.height())

        # top-level content
        self.title_label = QLabel("Doctor Python", self)
        self.title_label.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #e6f7ff;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle = QLabel("AI-powered Pharmacy — The Pharmacy That Talks Back", self)
        self.subtitle.setFont(QFont("Segoe UI", 14))
        self.subtitle.setStyleSheet("color: rgba(230,247,255,0.75);")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Continue button
        self.btn_continue = QPushButton("Continue", self)
        self.btn_continue.setFixedSize(220, 58)
        self.btn_continue.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self.btn_continue.setCursor(Qt.CursorShape.PointingHandCursor)
        # stylish CSS for button
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

        # add shadow for title
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(10, 30, 80, 180))
        self.title_label.setGraphicsEffect(shadow)

        # layout (center overlay)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(40, 48, 40, 40)
        vbox.setSpacing(18)
        vbox.addStretch()
        vbox.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addSpacing(18)
        vbox.addWidget(self.btn_continue, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch()

        # start particle animation
        self.particles.start()

        # ensure particles resize with the window
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.Resize:
            self.particles.setGeometry(0, 0, self.width(), self.height())
        return super().eventFilter(obj, event)

    def on_continue(self):
        # open role selection screen
        self.role_screen = RoleSelectionScreen()
        self.role_screen.show()
        self.particles.stop()
        self.close()

# -------------------------
# Role selection
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

        btn_customer = QPushButton("Customer")
        btn_employee = QPushButton("Employee")
        btn_customer.setFixedSize(180, 72)
        btn_employee.setFixedSize(180, 72)
        btn_customer.setStyleSheet("""
            QPushButton{ background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #041f6b, stop:1 #0078d7);
                       color: white; border-radius:12px; font-weight:600; }
            QPushButton:hover{ transform: translateY(-2px); }
        """)
        btn_employee.setStyleSheet("""
            QPushButton{ background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #002b36, stop:1 #00c2ff);
                       color: white; border-radius:12px; font-weight:600; }
        """)

        btn_customer.clicked.connect(self.open_customer)
        btn_employee.clicked.connect(self.open_employee)

        # central layout
        v = QVBoxLayout(self)
        v.addStretch()
        v.addWidget(title)
        v.addWidget(subtitle)
        v.addSpacing(24)

        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(btn_customer)
        h.addSpacing(40)
        h.addWidget(btn_employee)
        h.addStretch()
        v.addLayout(h)
        v.addStretch()
        v.setContentsMargins(24, 24, 24, 24)

    def open_employee(self):
        self.login_window = LoginWindow(role="Employee")
        self.login_window.show()
        self.close()

    def open_customer(self):
        self.login_window = LoginWindow(role="Customer")
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
