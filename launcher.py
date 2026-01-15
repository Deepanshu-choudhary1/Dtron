import sys
import threading
import traceback

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QTimer

from Dtron_hud import DtronHUD
from main import Dtron_loop


# ─────────────────────────────────────────────
# Qt-SAFE SIGNAL BRIDGE
# ─────────────────────────────────────────────
class DtronBridge(QObject):
    set_status = Signal(str)
    set_message = Signal(str)


def safe_Dtron_start(bridge, stop_event):
    try:
        print("🚀 Starting Dtron loop")
        Dtron_loop(bridge, stop_event)
    except Exception:
        print("❌ Dtron THREAD CRASH")
        traceback.print_exc()


if __name__ == "__main__":
    print("🧠 Creating QApplication")

    app = QApplication(sys.argv)

    # 🚨 VERY IMPORTANT
    QApplication.setQuitOnLastWindowClosed(False)

    print("🖥 Creating HUD")
    hud = DtronHUD()
    hud.show()

    QTimer.singleShot(0, hud.enter_fullscreen)


    print("🔗 Creating signal bridge")
    bridge = DtronBridge()

    # Thread-safe UI updates
    bridge.set_status.connect(hud.set_status)
    bridge.set_message.connect(hud.set_message)

    # 🛑 STOP EVENT (THIS WAS MISSING)
    stop_event = threading.Event()

    # ─────────────────────────────────────────────
    # Start Dtron logic thread
    # ─────────────────────────────────────────────
    Dtron_thread = threading.Thread(
        target=safe_Dtron_start,
        args=(bridge, stop_event),
        daemon=False  # 🚨 MUST BE FALSE
    )

    print("🧵 Starting Dtron thread")
    Dtron_thread.start()

    print("🟢 Entering Qt event loop")
    exit_code = app.exec()

    # Ensure clean shutdown
    stop_event.set()
    Dtron_thread.join(timeout=2)

    print("🔴 Qt loop exited with code:", exit_code)
    sys.exit(exit_code)
