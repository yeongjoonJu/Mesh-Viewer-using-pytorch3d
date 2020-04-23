import sys, os
sys.path.append(os.path.abspath(''))
from viewer import MeshViewer

from PyQt5.QtWidgets import (QApplication, QFileDialog)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    meshViewer = MeshViewer()
    meshViewer.show()
    sys.exit(app.exec_())
