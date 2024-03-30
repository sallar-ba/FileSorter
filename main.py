import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import QTimer
from os import scandir, rename, makedirs
from os.path import splitext, exists, join
from shutil import move

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtGui import QIcon


# Define supported file extensions
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".txt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"]

# Define source directory
source_dir = ""

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):
        if any(name.lower().endswith(ext) for ext in audio_extensions):
            dest_dir = join(source_dir, "Music")
            move_file(entry, dest_dir, name)

    def check_video_files(self, entry, name):
        if any(name.lower().endswith(ext) for ext in video_extensions):
            dest_dir = join(source_dir, "Video")
            move_file(entry, dest_dir, name)

    def check_image_files(self, entry, name):
        if any(name.lower().endswith(ext) for ext in image_extensions):
            dest_dir = join(source_dir, "Image")
            move_file(entry, dest_dir, name)

    def check_document_files(self, entry, name):
        for ext in document_extensions:
            if name.lower().endswith(ext):
                dest_dir = join(source_dir, "Documents")
                if ext == ".pdf":
                    dest_dir = join(dest_dir, "PDF")
                elif ext == ".csv" or ext == ".xls" or ext == ".xlsx":
                    dest_dir = join(dest_dir, "CSV")
                elif ext == ".txt":
                    dest_dir = join(dest_dir, "Text")
                elif ext == ".doc" or ext == ".docx" or ext == ".odt":
                    dest_dir = join(dest_dir, "Word")
                elif ext == ".ppt" or ext == ".pptx":
                    dest_dir = join(dest_dir, "PPT")
                else:
                    return
                move_file(entry, dest_dir, name)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'FileSorter'
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowIcon(QIcon('assets\icon.png'))

        self.selectFolderBtn = QPushButton('Select Source Folder', self)
        self.selectFolderBtn.setGeometry(50, 50, 300, 30)
        self.selectFolderBtn.clicked.connect(self.selectFolder)

        self.triggerBtn = QPushButton('Trigger Monitoring', self)
        self.triggerBtn.setGeometry(50, 100, 300, 30)
        self.triggerBtn.clicked.connect(self.monitorFolder)

        self.folderLabel = QLabel('', self)
        self.folderLabel.setGeometry(50, 150, 300, 30)

        self.show()

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(
            self, 'Select Source Folder', '/home')
        if folder:
            global source_dir
            source_dir = folder
            self.folderLabel.setText(folder)

            # Create destination directories within selected folder
            dest_dirs = ["Music", "Video", "Image", "Documents"]
            for dest_dir in dest_dirs:
                dest_path = join(source_dir, dest_dir)
                if not exists(dest_path):
                    makedirs(dest_path)

            # Create subfolders within Documents folder
            document_subfolders = ["PDF", "CSV", "Text", "PPT", "Word"]
            documents_dir = join(source_dir, "Documents")
            for subfolder in document_subfolders:
                subfolder_path = join(documents_dir, subfolder)
                if not exists(subfolder_path):
                    makedirs(subfolder_path)

    def monitorFolder(self):
        if source_dir:
            with scandir(source_dir) as entries:
                for entry in entries:
                    name = entry.name
                    MoverHandler().check_audio_files(entry, name)
                    MoverHandler().check_video_files(entry, name)
                    MoverHandler().check_image_files(entry, name)
                    MoverHandler().check_document_files(entry, name)


def move_file(entry, dest_dir, name):
    dest_file_path = join(dest_dir, name)
    if exists(dest_file_path):
        filename, extension = splitext(name)
        counter = 1
        while exists(join(dest_dir, f"{filename}({counter}){extension}")):
            counter += 1
        dest_file_path = join(dest_dir, f"{filename}({counter}){extension}")

    move(entry, dest_file_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
