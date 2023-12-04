from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog, QMainWindow
from PySide6.QtCore import Slot

from scene import Scene


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Refill")
        self.resize(640, 480)

        self.object = Scene()
        self.button = QPushButton("Open STL file...")
        self.button.clicked.connect(self.open_stl)
        self.setCentralWidget(self.object.get_view())
        self.statusBar().addWidget(self.button)

    @Slot()
    def open_stl(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open STL file...", "", "STL Files (*.stl)"
        )
        if filename:
            self.object.open_from_file(filename)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
