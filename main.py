import sys
import os
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtGui import QPixmap, QImage, QDesktopServices
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from src.utils import video_to_frames, detect_video_orientation


def remove_black_borders(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(binary)
    x, y, w, h = cv2.boundingRect(coords)
    return img[y:y + h, x:x + w]


class StitchWorker(QThread):
    progress_update = pyqtSignal(int)
    log_message = pyqtSignal(str)
    result_ready = pyqtSignal(object)

    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.video_path = video_path

    def run(self):
        frame_dir = "outputs/frames"
        self.log_message.emit("Starting frame extraction...")
        frames = video_to_frames(self.video_path, frame_dir, num_frames=10)
        self.progress_update.emit(20)

        self.log_message.emit("Loading frame images...")
        images = []
        for f in frames:
            if os.path.exists(f):
                img = cv2.imread(f)
                if img is not None:
                    images.append(img)
        if len(images) < 2:
            self.log_message.emit("❌ Not enough frames to stitch.")
            return

        self.progress_update.emit(40)

        self.log_message.emit("Detecting video orientation...")
        orientation = detect_video_orientation(images)
        self.log_message.emit(f"Orientation: {orientation}")

        self.log_message.emit("Starting stitching process...")
        stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
        status, panorama = stitcher.stitch(images)
        self.progress_update.emit(70)

        if status == cv2.Stitcher_OK:
            if orientation == "portrait":
                panorama = cv2.rotate(panorama, cv2.ROTATE_90_CLOCKWISE)
            panorama = remove_black_borders(panorama)
            output_path = "outputs/panorama_result.jpg"
            cv2.imwrite(output_path, panorama)
            self.log_message.emit(f"✅ Panorama saved to {output_path}.")
            self.progress_update.emit(100)
            self.result_ready.emit(panorama)
        else:
            self.log_message.emit(f"❌ Stitching failed with error code: {status}.")
            self.progress_update.emit(0)


class PanoramaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📸 Panorama Stitcher - PyQt5")
        self.setMinimumSize(900, 600)
        self.video_path = None
        self.worker = None

        # UI widgets
        self.video_info_label = QLabel("Please select a video file")
        self.video_info_label.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFixedHeight(300)  # Limit height
        self.result_label.setScaledContents(True)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2c7;
                width: 20px;
            }
        """)

        self.choose_button = QPushButton("Choose Video")
        self.process_button = QPushButton("Start Stitching")
        self.open_output_button = QPushButton("Open Output Folder")
        self.open_output_button.setEnabled(False)

        # Event bindings
        self.choose_button.clicked.connect(self.choose_video)
        self.process_button.clicked.connect(self.start_stitching)
        self.open_output_button.clicked.connect(self.open_output_folder)

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.choose_button)
        btn_layout.addWidget(self.process_button)
        btn_layout.addWidget(self.open_output_button)

        layout = QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(self.video_info_label)
        layout.addWidget(QLabel("Stitched Result Preview:"))
        layout.addWidget(self.result_label, 3)
        layout.addWidget(QLabel("Log Messages:"))
        layout.addWidget(self.log_text, 1)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def choose_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Video File", "data/", "Videos (*.mp4 *.avi *.mov)")
        if file_path:
            self.video_path = file_path
            self.video_info_label.setText(f"✅ Selected: {os.path.basename(file_path)}")
            self.log("✅ Video path: " + file_path)
            self.open_output_button.setEnabled(False)

    def start_stitching(self):
        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please select a video file first.")
            return

        self.log("Processing video...")
        self.progress_bar.setValue(0)
        self.choose_button.setEnabled(False)
        self.process_button.setEnabled(False)

        self.worker = StitchWorker(self.video_path)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.log_message.connect(self.log)
        self.worker.result_ready.connect(self.show_result)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def log(self, message):
        self.log_text.append(message)

    def show_result(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.result_label.setPixmap(QPixmap.fromImage(q_image))

        QMessageBox.information(self, "Done", "🎉 Panorama stitching completed! Saved to 'outputs' folder.")
        self.open_output_button.setEnabled(True)

    def on_worker_finished(self):
        self.choose_button.setEnabled(True)
        self.process_button.setEnabled(True)

    def open_output_folder(self):
        output_path = os.path.abspath("outputs")
        QDesktopServices.openUrl(QUrl.fromLocalFile(output_path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PanoramaApp()
    window.show()
    sys.exit(app.exec_())
