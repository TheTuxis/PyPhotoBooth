#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import cv
from PyQt4 import uic, QtGui, QtCore
from cv2 import *
from photo import Photo
from settings import AUTO_PRINT, PATCH_BACKGROUND_IMG, PATCH_LOGO_IMG


class PyPhotoBooth:
    def __init__(self):
        self.photo = Photo()
        self.photo_live = True
        self.global_count = 0
        self.MainWindow = uic.loadUi('main.ui')
        self.webcam = cv.CreateCameraCapture(-1)
        self.timer = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(
            self.timer, QtCore.SIGNAL('timeout()'), self.show_frame
        )
        self.MainWindow.connect(
            self.MainWindow.pushButton, QtCore.SIGNAL("clicked()"),
            self.take_photo
        )
        if AUTO_PRINT:
            self.MainWindow.pushButton_2.hide()
        else:
            self.MainWindow.connect(
                self.MainWindow.pushButton_2, QtCore.SIGNAL("clicked()"),
                self.print_photo_button
            )
        if PATCH_BACKGROUND_IMG is not None:
            palette = QtGui.QPalette()
            palette.setBrush(
                QtGui.QPalette.Background, QtGui.QBrush(
                    QtGui.QPixmap(PATCH_BACKGROUND_IMG)
                )
            )
            self.MainWindow.setPalette(palette)
        if PATCH_LOGO_IMG is not None:
            self.MainWindow.lblWebcam.setPixmap(
                QtGui.QPixmap(PATCH_LOGO_IMG)
            )
        self.timer.start(1)

    def take_photo(self):
        self.photo.take(self)

    def print_photo_button(self):
        result, count = self.photo.printing(self.global_count)
        if result:
            self.MainWindow.lcdNumber.display(0)
            self.MainWindow.lcdNumber.repaint()
            self.MainWindow.pick_01.setText(' ')
            self.MainWindow.pick_01.repaint()
            self.MainWindow.pick_02.setText(' ')
            self.MainWindow.pick_02.repaint()
            self.MainWindow.pick_03.setText(' ')
            self.MainWindow.pick_03.repaint()
            self.global_count = count

    def show_frame(self):
        if self.photo_live:
            ipl_image = cv.QueryFrame(self.webcam)
            data = ipl_image.tostring()
            image = QtGui.QImage(
                data, ipl_image.width, ipl_image.height, ipl_image.channels
                * ipl_image.width, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image.rgbSwapped())
            self.MainWindow.lblWebcam.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    pyphotobooth = PyPhotoBooth()
    pyphotobooth.MainWindow.show()
    app.exec_()
