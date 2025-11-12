from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        self.current_recognized_name = None
        self.ClockInButton.clicked.connect(self.manual_mark_attendance)

        #Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)

        self.image = None
        # store first face detection timestamps for delay logic
        self.first_seen = {}

    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        # Handle camera input type safely and choose numeric camera index
        if isinstance(camera_name, int):
            cam_index = camera_name
        else:
            try:
                cam_index = int(str(camera_name))
            except Exception:
                cam_index = 0  # fallback to default camera
        self.capture = cv2.VideoCapture(cam_index)
        self.timer = QTimer(self)  # Create Timer
        path = 'ImagesAttendance'
        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = []
        self.class_names = []
        self.encode_list = []
        self.TimeList1 = []
        self.TimeList2 = []
        attendance_list = os.listdir(path)

        for cl in attendance_list:
            file_path = os.path.join(path, cl)
            cur_img = cv2.imread(file_path)
            if cur_img is None:
                print(f"Warning: could not load image {file_path}, skipping.")
                continue
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])

        for img in images:
            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(img_rgb)
                if not boxes:
                    print("Warning: no face found in image, skipping.")
                    continue
                encodes_cur_frame = face_recognition.face_encodings(img_rgb, boxes)[0]
                self.encode_list.append(encodes_cur_frame)
            except Exception as e:
                print(f"Error processing image for encoding: {e}")
                continue
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # Upgraded RGB for better accuracy
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #  upgraded to CNN: model="cnn"
        faces_cur_frame = face_recognition.face_locations(rgb_frame)

        # Encode detected faces
        encodes_cur_frame = face_recognition.face_encodings(rgb_frame, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.45)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)
            y1, x2, y2, x1 = faceLoc

            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                color = (0, 255, 0)  # Green for known
            else:
                name = "UNKNOWN"
                color = (0, 0, 255)  # Red for unknown

            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), color, cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

            # delayed confirmation before asking to log attendance
            if name != "UNKNOWN":
                now = datetime.datetime.now()
                # first time seeing person in this cycle
                if name not in self.first_seen:
                    self.first_seen[name] = now
                    continue
                # check if 5 seconds passed
                if (now - self.first_seen[name]).total_seconds() >= 5:
                    del self.first_seen[name]
                    self.current_recognized_name = name
                else:
                    continue

        return frame

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)


    def ElapseList(self,name):
        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Clock In':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'Clock Out':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time2 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList2.append(Time2)
                                #print(Time2)

    def mark_attendance(self, name):
        if name != "UNKNOWN":
            last_action = None
            if os.path.exists('Attendance.csv'):
                with open('Attendance.csv', 'r') as f:
                    rows = list(csv.reader(f))
                    for row in rows[::-1]:
                        if len(row) >= 3 and row[0] == name:
                            last_action = row[2]
                            break

            if last_action == 'Present':
                action = "Clock Out"
                question = "Do you want to clock out?"
            else:
                action = "Clock In"
                question = "Do you want to clock in?"

            reply = QMessageBox.question(self, action, question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply != QMessageBox.Yes:
                return

            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")

            with open('Attendance.csv', 'a') as f:
                if last_action == 'Present':
                    f.writelines(f'\n{name},{date_time_string},Clock Out')
                    self.NameLabel.setText(name)
                    self.StatusLabel.setText('Clocked Out')
                    self.Time2 = datetime.datetime.now()
                    self.TimeList2.append(self.Time2)

                    if self.TimeList1:
                        CheckInTime = self.TimeList1[-1]
                        CheckOutTime = self.TimeList2[-1]
                        self.ElapseHours = (CheckOutTime - CheckInTime)
                        self.MinLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60) % 60) + 'm')
                        self.HoursLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60**2)) + 'h')
                else:
                    f.writelines(f'\n{name},{date_time_string},Present')
                    self.NameLabel.setText(name)
                    self.StatusLabel.setText('Present')
                    self.HoursLabel.setText('Measuring')
                    self.MinLabel.setText('')
                    self.Time1 = datetime.datetime.now()
                    self.TimeList1.append(self.Time1)

    def manual_mark_attendance(self):
        if not self.current_recognized_name:
            QMessageBox.information(self, "No Face Detected", "No recognized face to mark attendance.")
            return
        self.mark_attendance(self.current_recognized_name)

    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret or frame is None:
            # failed to read frame from camera; skip this tick
            return
        self.image = frame
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        if image is None:
            # nothing to display
            return
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
