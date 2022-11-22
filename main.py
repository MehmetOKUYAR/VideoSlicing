from PyQt5.QtWidgets import QApplication
from VideoSlice_codes import VideoSlice_APP
app = QApplication([])
window = VideoSlice_APP()
window.setWindowTitle('Video Slice Application')
window.show()
app.exec_()

