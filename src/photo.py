#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image
import PIL
import os
from settings import TEMP_PHOTO_DIR, PREFIX_PHOTO_NAME, AUTO_PRINT

from PyQt4 import QtGui, QtCore
import time
import cv
from cv2 import *


class Photo:

    def take(self, main):
        main.timer.stop()
        main.photo_live = False
        main.webcam = None
        count = 0
        while count < 3:
            temp = 0
            while temp < 3 and count < 3:
                main.MainWindow.lbltimer.setText(str(3-temp))
                main.MainWindow.lbltimer.repaint()
                temp += 1
                time.sleep(1)
            main.MainWindow.lbltimer.setText(str('Foto!!'))
            main.MainWindow.lbltimer.repaint()
            cam = VideoCapture(0)
            s, img = cam.read()
            if s:
                imwrite(
                    TEMP_PHOTO_DIR + "/" + PREFIX_PHOTO_NAME + str(
                        main.global_count
                    )+"_"+str(count)+".jpg",
                    img)
                image = QtGui.QImage(
                    TEMP_PHOTO_DIR + "/" + PREFIX_PHOTO_NAME + str(
                        main.global_count
                    )+"_"+str(count)+".jpg"
                )
                main.MainWindow.lcdNumber.display(count+1)
                pp = QtGui.QPixmap.fromImage(image)
                pp = pp.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                if count == 0:
                    main.MainWindow.pick_01.setPixmap(pp)
                    main.MainWindow.pick_01.repaint()
                    main.MainWindow.lcdNumber.repaint()
                elif count == 1:
                    main.MainWindow.pick_02.setPixmap(pp)
                    main.MainWindow.pick_02.repaint()
                    main.MainWindow.lcdNumber.repaint()
                elif count == 2:
                    main.MainWindow.pick_03.setPixmap(pp)
                    main.MainWindow.pick_03.repaint()
                    main.MainWindow.lcdNumber.repaint()
            count += 1
            cam = None
        if AUTO_PRINT:
            tmp = Photo()
            result, count = tmp.printing(main.global_count)
            if result:
                main.global_count = count
        main.MainWindow.lbltimer.setText(str(''))
        main.MainWindow.lbltimer.repaint()
        main.webcam = cv.CreateCameraCapture(-1)
        main.timer.start(1)
        main.photo_live = True

    def printing(self, global_count):
        try:
            basewidth = 280
            hsize = 210
            photo_01 = Image.open(
                TEMP_PHOTO_DIR + "/" + PREFIX_PHOTO_NAME + str(
                    global_count
                ) + "_0.jpg"
            )
            photo_02 = Image.open(
                TEMP_PHOTO_DIR + "/" + PREFIX_PHOTO_NAME + str(
                    global_count
                ) + "_1.jpg"
            )
            photo_03 = Image.open(
                TEMP_PHOTO_DIR + "/" + PREFIX_PHOTO_NAME + str(
                    global_count
                ) + "_2.jpg"
            )
            blank_image = Image.new("RGB", (300, 670), (255, 255, 255, 255))
            blank_image.paste(
                photo_01.resize(
                    (basewidth, hsize), PIL.Image.ANTIALIAS
                ), (10, 10)
            )
            blank_image.paste(
                photo_02.resize(
                    (basewidth, hsize), PIL.Image.ANTIALIAS
                ), (10, 230)
            )
            blank_image.paste(
                photo_03.resize(
                    (basewidth, hsize), PIL.Image.ANTIALIAS
                ), (10, 450)
            )
            blank_image.save(
                TEMP_PHOTO_DIR + "/" + PREFIX_PHOTO_NAME + str(
                    global_count
                ) + "_final.jpg"
            )
            os.system("lp " + TEMP_PHOTO_DIR + "/" + PREFIX_PHOTO_NAME + str(
                global_count
            ) + "_final.jpg")
            global_count += 1
            return True, global_count
        except:
            return False, global_count
