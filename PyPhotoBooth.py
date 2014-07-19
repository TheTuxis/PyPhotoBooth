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
from PyQt4 import uic, QtGui, QtCore

import cv

from cv2 import *
import time


class PyPhotoBooth:
    def __init__(self):
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
        self.MainWindow.connect(
            self.MainWindow.pushButton_2, QtCore.SIGNAL("clicked()"),
            self.print_photo
        )
        self.timer.start(1)

    def take_photo(self):
        self.timer.stop()
        self.photo_live = False
        self.webcam = None
        count = 0
        while count < 3:
            cam = VideoCapture(0)
            s, img = cam.read()
            if s:
                imwrite(
                    "photo_temp/photo_"+str(
                        self.global_count
                    )+"_"+str(count)+".jpg",
                    img)
                image = QtGui.QImage(
                    "photo_temp/photo_"+str(
                        self.global_count
                    )+"_"+str(count)+".jpg"
                )
                self.MainWindow.lcdNumber.display(count+1)
                pp = QtGui.QPixmap.fromImage(image)
                pp = pp.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                if count == 0:
                    self.MainWindow.pick_01.setPixmap(pp)
                    self.MainWindow.pick_01.repaint()
                    self.MainWindow.lcdNumber.repaint()
                elif count == 1:
                    self.MainWindow.pick_02.setPixmap(pp)
                    self.MainWindow.pick_02.repaint()
                    self.MainWindow.lcdNumber.repaint()
                elif count == 2:
                    self.MainWindow.pick_03.setPixmap(pp)
                    self.MainWindow.pick_03.repaint()
                    self.MainWindow.lcdNumber.repaint()
            count += 1
            temp = 0
            while temp < 2 and count < 3:
                temp += 1
                time.sleep(1)
            cam = None
        self.webcam = cv.CreateCameraCapture(-1)
        self.timer.start(1)
        self.photo_live = True

    def print_photo(self):
        import Image
        import PIL
        import os
        basewidth = 280
        hsize = 210
        photo_01 = Image.open(
            "photo_temp/photo_"+str(self.global_count)+"_0.jpg"
        )
        photo_02 = Image.open(
            "photo_temp/photo_"+str(self.global_count)+"_1.jpg"
        )
        photo_03 = Image.open(
            "photo_temp/photo_"+str(self.global_count)+"_2.jpg"
        )

        #blank_image = Image.open("blank.jpg")
        blank_image = Image.new("RGB", (300, 670), (255, 255, 255, 255))
        blank_image.paste(
            photo_01.resize((basewidth, hsize), PIL.Image.ANTIALIAS), (10, 10)
        )
        blank_image.paste(
            photo_02.resize((basewidth, hsize), PIL.Image.ANTIALIAS), (10, 230)
        )
        blank_image.paste(
            photo_03.resize((basewidth, hsize), PIL.Image.ANTIALIAS), (10, 450)
        )
        blank_image.save(
            "photo_temp/photo_"+str(self.global_count)+"_final.jpg"
        )
        os.system("lp photo_temp/photo_"+str(self.global_count)+"_final.jpg")
        self.MainWindow.lcdNumber.display(0)
        self.MainWindow.lcdNumber.repaint()
        self.MainWindow.pick_01.setText(' ')
        self.MainWindow.pick_01.repaint()
        self.MainWindow.pick_02.setText(' ')
        self.MainWindow.pick_02.repaint()
        self.MainWindow.pick_03.setText(' ')
        self.MainWindow.pick_03.repaint()
        self.global_count += 1

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
