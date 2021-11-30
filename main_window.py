
# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMessageBox

# import Opencv module
import cv2
#import faceme
import facemecv

from ui_main_window import *

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)
        #
        self.ui.pushButtonRegister.clicked.connect(self.pushButtonRegister_pressed)

        self.stage = 0
        self.faces_imglist = list()

        facemecv.initialize_SDK(license_key = 'insert license key here', password = 'insert password here or None')

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        if ret == False:
            return
        # flip image (not used with test video file)
        image = cv2.flip(image, 1)
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        facemeimage = facemecv.convert_image_to_faceimage(image)
        
        orig_image = image.copy()
        
        detect_results = facemecv.detect_face_from_faceimage(facemeimage)
        
        if len(detect_results) > 0:
            for detect_result in detect_results:
                image = cv2.rectangle(image, detect_result['boundingBox'][0], detect_result['boundingBox'][1], (255,0,0),2)
                
                pose = facemecv.get_pose_from_faceimage(facemeimage)
                print(pose)
                if pose is None:
                    continue
                (pose_yaw, pose_pitch, pose_roll) = pose
                
                if self.stage == 0:
                    self.ui.label_6.setText("Center your face")
                    if (pose_pitch > -5.0 and pose_pitch < 5.0) and (pose_yaw > -5.0 and pose_yaw < 5.0):
                        img = orig_image.copy()
                        self.faces_imglist.append(img)
                        # get image infos
                        height, width, channel = img.shape
                        step = channel * width
                        # create QImage from image
                        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
                        # show image in img_label
                        self.ui.label.setPixmap(QPixmap.fromImage(qImg).scaled(200,200, QtCore.Qt.KeepAspectRatio))
                        self.stage = 1
                elif self.stage == 1:
                    self.ui.label_6.setText("Turn your head to the right")
                    if (pose_pitch > -5.0 and pose_pitch < 5.0) and (pose_yaw > -65.0 and pose_yaw < -15.0):
                        img = orig_image.copy()
                        self.faces_imglist.append(img)
                        # get image infos
                        height, width, channel = img.shape
                        step = channel * width
                        # create QImage from image
                        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
                        # show image in img_label
                        self.ui.label_2.setPixmap(QPixmap.fromImage(qImg).scaled(200,200, QtCore.Qt.KeepAspectRatio))
                        self.stage = 2
                elif self.stage == 2:
                    self.ui.label_6.setText("Turn your head to the left")
                    if (pose_pitch > -5.0 and pose_pitch < 5.0) and (pose_yaw > 15.0 and pose_yaw < 65.0):
                        img = orig_image.copy()
                        self.faces_imglist.append(img)
                        # get image infos
                        height, width, channel = img.shape
                        step = channel * width
                        # create QImage from image
                        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
                        # show image in img_label
                        self.ui.label_3.setPixmap(QPixmap.fromImage(qImg).scaled(200,200, QtCore.Qt.KeepAspectRatio))
                        self.stage = 3
                elif self.stage == 3:
                    self.ui.label_6.setText("Look up")
                    if (pose_pitch > 15.0 and pose_pitch < 35.0) and (pose_yaw > -5.0 and pose_yaw < 5.0):
                        img = orig_image.copy()
                        self.faces_imglist.append(img)
                        # get image infos
                        height, width, channel = img.shape
                        step = channel * width
                        # create QImage from image
                        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
                        # show image in img_label
                        self.ui.label_4.setPixmap(QPixmap.fromImage(qImg).scaled(200,200, QtCore.Qt.KeepAspectRatio))
                        self.stage = 4
                elif self.stage == 4:
                    self.ui.label_6.setText("Look down")
                    if (pose_pitch > -35.0 and pose_pitch < -15.0) and (pose_yaw > -5.0 and pose_yaw < 5.0):
                        img = orig_image.copy()
                        self.faces_imglist.append(img)
                        # get image infos
                        height, width, channel = img.shape
                        step = channel * width
                        # create QImage from image
                        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
                        # show image in img_label
                        self.ui.label_5.setPixmap(QPixmap.fromImage(qImg).scaled(200,200, QtCore.Qt.KeepAspectRatio))
                        self.stage = 5
                elif self.stage == 5:
                    self.ui.label_6.setText("Great!!")
        
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            #self.cap = cv2.VideoCapture('videosample5.mp4')
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")

    def pushButtonRegister_pressed(self):
        username = self.ui.lineEdit.text()
        if len(username) == 0:
            QMessageBox.about(self, "Registration", "Username box is empty")
            return

        if len(self.faces_imglist) == 0:
            return

        results = None
        for face in self.faces_imglist:
            facemeimg = facemecv.convert_image_to_faceimage(face)
            results = facemecv.search_similar_face(facemeimg)

        if results is None:
            facemeimg = facemecv.convert_image_to_faceimage(self.faces_imglist[0])
            facemecv.register_user_with_faceimage(username, facemeimg)
            for face in self.faces_imglist[1:]:
                facemeimg = facemecv.convert_image_to_faceimage(face)
                results = facemecv.add_face_faceimage(username, facemeimg)
            QMessageBox.about(self, "Registration", "User " + "\""+ username +"\" successfully registered")
        elif len(results) == 0: ###
            facemeimg = facemecv.convert_image_to_faceimage(self.faces_imglist[0])
            facemecv.register_user_with_faceimage(username, facemeimg)
            for face in self.faces_imglist[1:]:
                facemeimg = facemecv.convert_image_to_faceimage(face)
                results = facemecv.add_face_faceimage(username, facemeimg)
            QMessageBox.about(self, "Registration", "User " + "\""+ username +"\" successfully registered")
        elif len(results) > 0:
            QMessageBox.about(self, "Registration", "User " + "\""+ username +"\" is already registered with name \""+results[0]['name']+"\"\r\n(confidence:"+str(results[0]['confidence'])+")")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
