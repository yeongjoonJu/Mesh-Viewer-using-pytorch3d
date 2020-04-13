from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap, qRgb, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
        QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy, QInputDialog)
import os
import numpy as np
from matplotlib import cm
from PIL import Image, ImageFont, ImageDraw

import sys
sys.path.append(os.path.abspath(''))
from mesh_loader import MeshLoader

class MeshViewer(QMainWindow):
    def __init__(self):
        super(MeshViewer, self).__init__()

        self.gray_color_table = [qRgb(i, i, i) for i in range(256)]
               
        self.width = 1024
        self.height = 1024

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.setCentralWidget(self.imageLabel)

        self.loaded = False
        self.font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 15)

        self.initMenu()
        self.meshLoader = MeshLoader()
        
        self.setWindowTitle("Mesh Viewer by yj_ju")
        self.resize(self.width, self.height)
    
    def initMenu(self):
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open .obj file')
        openFile.triggered.connect(self.showFileDialog)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

    def showFileDialog(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open obj file', './data')        
        self.meshLoader.load(self.fname[0])
        self.loaded = True
        image = self.meshLoader.render()
        image = image * 255
        image = image.astype('uint8')
        self.openImage(image)
    

    def toQImage(self, im, copy=False):
        if im is None:
            return QImage()
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(self.gray_color_table)
                return qim.copy() if copy else qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                    return qim.copy() if copy else qim
    
    def openImage(self, image):
        self.imageLabel.setPixmap(QPixmap.fromImage(self.toQImage(image)))

        #self.fitToWindowAct.setEnabled(True)
        #self.updateActions()
        #if not self.fitToWindowAct.isChecked():
        #    self.imageLabel.adjustSize()

    def render_for_camera(self, dist, elev, azim):
        image = self.meshLoader.render(dist, elev, azim)
        image = image * 255
        image = image.astype('uint8')
        
        img = Image.fromarray(image)
        draw = ImageDraw.Draw(img)
        draw.text((10,10), "distance: {0}, elevation: {1}, azimuth: {2}"
        .format(round(dist,3), round(elev,3), round(azim,3)), (255,255,255), font=self.font)
            
        self.openImage(np.array(img))

    def mousePressEvent(self, e):
        self.prev_pos = (e.x(), e.y())

    def mouseMoveEvent(self, e):
        if not self.loaded:
            return
        
        dist, elev, azim = self.meshLoader.get_camera_params()
        # Adjust rotation speed
        azim = azim + (self.prev_pos[0] - e.x())*0.1
        elev = elev - (self.prev_pos[1] - e.y())*0.1
        self.render_for_camera(dist, elev, azim)

        self.prev_pos = (e.x(), e.y())

    def wheelEvent(self, e):
        if not self.loaded:
            return
        dist, elev, azim = self.meshLoader.get_camera_params()
        # Adjust rotation speed
        dist = dist - e.angleDelta().y()*0.001
        self.render_for_camera(dist, elev, azim)

            
    def keyPressEvent(self, e):
        if e.key() == 65:
            pass
                                                
        elif e.key() == 68:
            pass
