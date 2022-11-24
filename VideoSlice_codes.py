import cv2
from datetime import datetime
from videoSlice import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QFileDialog,QMessageBox
from PyQt5.QtGui import  QImage, QPixmap

class VideoSlice_APP(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.load_video)
        self.ui.pushButton_2.clicked.connect(self.slice_video)
        self.ui.pushButton_3.clicked.connect(self.select_save_path)
        self.ui.pushButton_4.clicked.connect(self.close)

    
    def close(self):
        self.stopCap = False

    def slice_video(self):
        self.stopCap = True
        savedFrames = []
        cv2.namedWindow('Video Slice',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video Slice', 10,10)
        count = 0


        try: 
            if self.save_path == '':
                QMessageBox.warning(self, 'Warning', 'Select Save Path')
                self.select_save_path()
        except:
            self.select_save_path()



        while self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            if ret==False or self.stopCap == False:
                self.video_cap.release()
                cv2.destroyAllWindows()
                self.ui.label.clear()
                self.ui.label_7.clear()
                self.ui.label_2.clear()
                self.ui.label_3.clear()
                self.ui.label_4.clear()
                self.ui.label_5.clear()
                self.ui.label_6.clear()
                self.ui.lineEdit.clear()
                self.ui.label.setText('Complated Video Slice')
                self.ui.pushButton_3.setText('Kayıt Klasör seç')
                break
            
            if self.ui.lineEdit.text() == '':
                perFrame = 1
            else :
                perFrame = int(self.ui.lineEdit.text())

            if count % perFrame == 0:
                name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f') + '.jpg'
                cv2.imwrite(self.save_path + '/' + name, frame)
                savedFrames.append(frame)

                if len(savedFrames) > 5:
                    savedFrames.pop(0)

                if len(savedFrames) == 5:
                    for i,img in enumerate(savedFrames):
                        if i == 4:
                            self.setVideo_camera(img,self.ui.label_2)
                        elif i == 3:
                            self.setVideo_camera(img,self.ui.label_5)
                        elif i == 2:
                            self.setVideo_camera(img,self.ui.label_6)
                        elif i == 1:
                            self.setVideo_camera(img,self.ui.label_3)
                        elif i == 0:
                            self.setVideo_camera(img,self.ui.label_4)
                elif len(savedFrames) == 4:
                    for i,img in enumerate(savedFrames):
                        if i == 3:
                            self.setVideo_camera(img,self.ui.label_2)
                        elif i == 2:
                            self.setVideo_camera(img,self.ui.label_5)
                        elif i == 1:
                            self.setVideo_camera(img,self.ui.label_6)
                        elif i == 0:
                            self.setVideo_camera(img,self.ui.label_3)
                elif len(savedFrames) == 3:
                    for i,img in enumerate(savedFrames):
                        if i == 2:
                            self.setVideo_camera(img,self.ui.label_2)
                        elif i == 1:
                            self.setVideo_camera(img,self.ui.label_5)
                        elif i == 0:
                            self.setVideo_camera(img,self.ui.label_6)
                elif len(savedFrames) == 2:
                    for i,img in enumerate(savedFrames):
                        if i == 1:
                            self.setVideo_camera(img,self.ui.label_2)
                        elif i == 0:
                            self.setVideo_camera(img,self.ui.label_5)
                elif len(savedFrames) == 1:
                    for i,img in enumerate(savedFrames):
                        if i == 0:
                            self.setVideo_camera(img,self.ui.label_2)

            count += 1
            self.setVideo_camera(frame,self.ui.label)
            cv2.imshow('Video Slice',frame)
            cv2.waitKey(30)
        self.video_cap.release()
        cv2.destroyAllWindows()

    def load_video(self):
        video_path = QFileDialog.getOpenFileName(self, 'Open Video', 'C:\\Users\\', 'Video Files (*.mp4 *.avi *.flv *.mkv)')[0]

        if video_path != '':
            self.video_path = video_path
            self.video_cap = cv2.VideoCapture(self.video_path)  

            fps = self.video_cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            Text = f'FPS: {fps} Total Frame Count: {frame_count}'
            self.ui.label_7.setText(Text)

            ret, frame = self.video_cap.read()
            self.setVideo_camera(frame,self.ui.label)


    #========  video-kamera görüntüsünü ekranda göster =======================
    def setVideo_camera(self,img1,label_name):
        geo = label_name.geometry()
        w,h = geo.getRect()[2:]
        frame = cv2.resize(img1,(w,h))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame,frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        label_name.setPixmap(QPixmap.fromImage(image))


    def select_save_path(self):
        self.save_path = QFileDialog.getExistingDirectory(self, 'Select Save Path', 'C:\\Users\\')
        self.ui.pushButton_3.setText(self.save_path)

    