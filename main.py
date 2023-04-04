import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from moviepy.editor import concatenate_videoclips, VideoFileClip


class VideoMerger(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Merger")

        self.merge_btn = QPushButton("Merge Videos", self)
        self.merge_btn.clicked.connect(self.merge_videos)
        self.merge_btn.resize(self.merge_btn.sizeHint())
        self.merge_btn.move(50, 50)

        self.setGeometry(300, 300, 200, 150)
        self.show()

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
            clips = []
            for video in videos:
                try:
                    clip = VideoFileClip(video)
                    clips.append(clip)
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"Failed to load video file: {video}\n{str(e)}"
                    )
                    return

            final_clip = concatenate_videoclips(clips)

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

                final_clip.write_videofile(
                    save_path,
                    codec="libx264",
                    preset="ultrafast",
                    threads=os.cpu_count(),
                )
                QMessageBox.information(
                    self,
                    "Success",
                    f"Videos merged successfully and saved at {save_path}",
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vm = VideoMerger()
    sys.exit(app.exec_())
