import sys
import math
import time
import psutil
import numpy as np

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import QTimer, Qt, Slot

# Optional mic
try:
    import sounddevice as sd
except ImportError:
    sd = None


class DtronHUD(QWidget):
    def __init__(self):
        super().__init__()

        # ───── WINDOW ─────
        self.setWindowTitle("Dtron HUD")
        self.setStyleSheet("background-color: black;")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_ShowWithoutActivating, False)

        self.setFocusPolicy(Qt.StrongFocus)
        self.activateWindow()
        self.raise_()


        # ───── STATE ─────
        self.angle = 0
        self.radar_angle = 0
        self.wave_phase = 0.0
        self.audio_level = 0.3

        self.status = "LISTENING"

        # Typing animation
        self.full_text = "Awaiting command..."
        self.display_text = ""
        self.char_index = 0
        self.typing_active = False

        self.vision_boxes = []

        # ───── AUDIO ─────
        self.audio_enabled = False
        if sd is not None:
            try:
                sd.InputStream(callback=self._audio_cb).start()
                self.audio_enabled = True
            except Exception as e:
                print("Audio disabled:", e)

        # ───── TIMERS ─────
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(16)

        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self._type_next_char)
        self.typing_timer.setInterval(25)

    # ─────────────────────────────────────────
    # ✅ QT SLOTS (CRITICAL FIX)
    # ─────────────────────────────────────────
    @Slot(str)
    def set_status(self, text):
        self.status = text
        self.update()

    @Slot(str)
    def set_message(self, text):
        self.full_text = text
        self.display_text = ""
        self.char_index = 0
        self.typing_active = True
        self.typing_timer.start()
        self.update()

    @Slot(list)
    def set_vision_boxes(self, boxes):
        self.vision_boxes = boxes
        self.update()

    # ───── AUDIO CALLBACK ─────
    def _audio_cb(self, indata, frames, time_info, status):
        vol = np.linalg.norm(indata) * 10
        self.audio_level = min(float(vol), 1.0)
        
    def enter_fullscreen(self):
        self.showFullScreen()
        self.activateWindow()
        self.raise_()


    # ───── TYPING EFFECT ─────
    def _type_next_char(self):
        if self.char_index < len(self.full_text):
            self.display_text += self.full_text[self.char_index]
            self.char_index += 1
            self.update()
        else:
            self.typing_timer.stop()
            self.typing_active = False
            
    # ───── PREVENT ESC / CLOSE ─────
    def keyPressEvent(self, event):
    # Block ESC key from closing fullscreen HUD
        if event.key() == Qt.Key_Escape:
            event.ignore()
            return
        super().keyPressEvent(event)


    def closeEvent(self, event):
    # Prevent accidental window close
        event.ignore()


    # ───── ANIMATION ─────
    def animate(self):
        self.angle = (self.angle + 1) % 360
        self.radar_angle = (self.radar_angle + 2) % 360
        self.wave_phase += 0.15

        if not self.audio_enabled:
            self.audio_level = abs(math.sin(self.wave_phase * 0.4)) * 0.6 + 0.1

        self.update()

    # ───── PAINT ─────
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2

        # Rings
        painter.setPen(QPen(QColor(0, 255, 255), 2))
        painter.drawEllipse(cx - 260, cy - 260, 520, 520)

        painter.setPen(QPen(QColor(0, 180, 255), 4))
        painter.drawArc(cx - 240, cy - 240, 480, 480,
                        int(self.angle * 16), 120 * 16)

        painter.setPen(QPen(QColor(0, 255, 150, 120), 2))
        painter.drawArc(cx - 300, cy - 300, 600, 600,
                        int(self.radar_angle * 16), 40 * 16)

        painter.setBrush(QColor(0, 255, 255))
        painter.drawEllipse(cx - 6, cy - 6, 12, 12)

        # Waveform
        wave_y = h - 120
        painter.setPen(QPen(QColor(0, 255, 255), 2))
        for x in range(0, w, 12):
            y_offset = math.sin(x * 0.02 + self.wave_phase) * 60 * self.audio_level
            painter.drawLine(x, wave_y, x, int(max(0, min(h, wave_y - y_offset))))

        # Left HUD text
        painter.setFont(QFont("Consolas", 14))
        painter.setPen(QColor(0, 255, 255))
        painter.drawText(40, 50, "Dtron AI CORE")
        painter.drawText(40, 85, f"STATUS: {self.status}")
        painter.drawText(40, 120, time.strftime("TIME: %H:%M:%S"))

        painter.setFont(QFont("Consolas", 11))
        painter.drawText(w - 220, 60, f"CPU: {psutil.cpu_percent()}%")
        painter.drawText(w - 220, 90, f"RAM: {psutil.virtual_memory().percent}%")

        # Glow text box
        text_x = 60
        text_y = cy - 140
        text_w = int(w * 0.38)
        text_h = 280

        glow_alpha = 140 if self.typing_active else 70
        painter.setPen(QPen(QColor(0, 255, 255, glow_alpha), 3))
        painter.drawRect(text_x - 10, text_y - 10, text_w + 20, text_h + 20)

        painter.setFont(QFont("Consolas", 18))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(
            text_x,
            text_y,
            text_w,
            text_h,
            Qt.AlignLeft | Qt.TextWordWrap,
            f"> {self.display_text}"
        )

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hud = DtronHUD()
    hud.show()
    sys.exit(app.exec())
