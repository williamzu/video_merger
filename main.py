import sys
import os
import subprocess
from ffmpeg_installer import (
    check_ffmpeg_installed,
    install_ffmpeg
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QDesktopWidget,
)


class VideoMerger(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Merger")
        self.setGeometry(0, 0, 400, 300)
        self.center()
        self.merge_btn = QPushButton("Merge Videos", self)
        self.merge_btn.clicked.connect(self.merge_videos)
        self.merge_btn.resize(self.merge_btn.sizeHint())
        self.merge_btn.move(150, 120)
        

        if not check_ffmpeg_installed():
            
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Question)
            message_box.setText("FFmpeg is required but is not installed. Do you want to install it?")
            message_box.setWindowTitle("Confirmation")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            button_clicked = message_box.exec_()
            oh_no_message = QMessageBox()
            oh_no_message.setText("Unfortunately, the application will not work")

            if button_clicked == QMessageBox.Yes:
                install_ffmpeg()
                if check_ffmpeg_installed():
                    QMessageBox.information(self, "Sucess", "FFMpeg installed sucessfully, you can proceed and use the application")
                    self.merge_btn.setEnabled(True)
                else:
                    oh_no_message.exec_()
                    self.merge_btn.setEnabled(False)
            else:
                oh_no_message.exec_()
                self.merge_btn.setEnabled(False)
                
        
        self.show()

    def center(self):
        # Get the screen geometry
        screen = QDesktopWidget().screenGeometry()

        # Calculate the center point
        x = (screen.width() - self.geometry().width()) // 2
        y = (screen.height() - self.geometry().height()) // 2

        # Move the window to the center
        self.move(x, y)

    def merge_videos(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        videos, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)",
            options=options,
        )

        if videos:
            save_options = QFileDialog.Options()
            save_options |= QFileDialog.ReadOnly
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Merged Video",
                os.path.dirname(videos[0]),
                "Video Files (*.mp4);;All Files (*)",
                options=save_options,
            )

            if save_path:
                if not save_path.endswith(".mp4"):
                    save_path += ".mp4"

                videos_concatenated = "|".join(videos)
                ffmpeg_command = (
                    f'ffmpeg -i "concat:{videos_concatenated}" -c copy "{save_path}" -y'
                )
                os.system(ffmpeg_command)

                QMessageBox.information(
                    self,
                    "Success",
                    f"Videos merged successfully and saved at {save_path}",
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vm = VideoMerger()
    sys.exit(app.exec_())
