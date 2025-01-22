import sys
from PyQt5.QtWidgets import QApplication
from gui import MediaIngestGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MediaIngestGUI()
    gui.show()
    sys.exit(app.exec_())