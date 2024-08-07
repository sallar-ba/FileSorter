import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal
from os import scandir, makedirs, remove
from os.path import splitext, exists, join, isfile, isdir
from shutil import move, rmtree
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define supported file extensions
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".txt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"]
design_extensions = [".psd", ".ai", ".indd", ".indt"]
archive_extensions = [".zip", ".rar", ".7z", ".tar", ".gz"]
script_extensions = [".py", ".java", ".cpp", ".c", ".cs", ".js", ".html", ".css", ".php", ".rb", ".r", ".go", ".sh", ".pl", ".swift", ".kt", ".ts", ".lua"]

# Define source directory
source_dir = ""


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            time.sleep(1)  # Small delay to handle race condition
            with scandir(source_dir) as entries:
                for entry in entries:
                    name = entry.name
                    self.check_audio_files(entry, name)
                    self.check_video_files(entry, name)
                    self.check_image_files(entry, name)
                    self.check_document_files(entry, name)
                    self.check_design_files(entry, name)
                    self.check_archive_files(entry, name)
                    self.check_script_files(entry, name)

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
        if any(name.lower().endswith(ext) for ext in document_extensions):
            dest_dir = join(source_dir, "Documents")
            if name.lower().endswith(".pdf"):
                dest_dir = join(dest_dir, "PDF")
            elif name.lower().endswith(".csv") or name.lower().endswith(".xls") or name.lower().endswith(".xlsx"):
                dest_dir = join(dest_dir, "CSV")
            elif name.lower().endswith(".txt"):
                dest_dir = join(dest_dir, "Text")
            elif name.lower().endswith(".doc") or name.lower().endswith(".docx") or name.lower().endswith(".odt"):
                dest_dir = join(dest_dir, "Word")
            elif name.lower().endswith(".ppt") or name.lower().endswith(".pptx"):
                dest_dir = join(dest_dir, "PPT")
            move_file(entry, dest_dir, name)

    def check_design_files(self, entry, name):
        if any(name.lower().endswith(ext) for ext in design_extensions):
            dest_dir = join(source_dir, "Design")
            move_file(entry, dest_dir, name)

    def check_archive_files(self, entry, name):
        if any(name.lower().endswith(ext) for ext in archive_extensions):
            dest_dir = join(source_dir, "Archives")
            move_file(entry, dest_dir, name)

    def check_script_files(self, entry, name):
        if any(name.lower().endswith(ext) for ext in script_extensions):
            dest_dir = join(source_dir, "Scripts")
            move_file(entry, dest_dir, name)


class MonitorThread(QThread):
    folder_selected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.observer = None

    def run(self):
        event_handler = MoverHandler()
        self.observer = Observer()
        self.observer.schedule(event_handler, source_dir, recursive=True)
        self.observer.start()
        self.exec()

    def stop(self):
        self.observer.stop()
        self.observer.join()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'FileSorter'
        self.width = 400
        self.height = 200
        self.initUI()
        self.monitor_thread = MonitorThread()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowIcon(QIcon(r'C:\Users\PMLS\Desktop\FileSorter\assets\icon.png'))

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
        folder = QFileDialog.getExistingDirectory(self, 'Select Source Folder', '/home')
        if folder:
            global source_dir
            source_dir = folder
            self.folderLabel.setText(folder)

            # Create destination directories within selected folder
            dest_dirs = ["Music", "Video", "Image", "Documents", "Design", "Archives", "Scripts"]
            for dest_dir in dest_dirs:
                dest_path = join(source_dir, dest_dir)
                if not exists(dest_path):
                    makedirs(dest_path, exist_ok=True)
                elif isfile(dest_path):
                    remove(dest_path)
                    makedirs(dest_path, exist_ok=True)

            # Create subfolders within Documents folder
            document_subfolders = ["PDF", "CSV", "Text", "PPT", "Word"]
            documents_dir = join(source_dir, "Documents")
            if not exists(documents_dir):
                makedirs(documents_dir, exist_ok=True)
            elif isfile(documents_dir):
                remove(documents_dir)
                makedirs(documents_dir, exist_ok=True)
            for subfolder in document_subfolders:
                subfolder_path = join(documents_dir, subfolder)
                if not exists(subfolder_path):
                    makedirs(subfolder_path, exist_ok=True)
                elif isfile(subfolder_path):
                    remove(subfolder_path)
                    makedirs(subfolder_path, exist_ok=True)

    def monitorFolder(self):
        if source_dir:
            if not self.monitor_thread.isRunning():
                self.monitor_thread.start()
            with scandir(source_dir) as entries:
                for entry in entries:
                    name = entry.name
                    MoverHandler().check_audio_files(entry, name)
                    MoverHandler().check_video_files(entry, name)
                    MoverHandler().check_image_files(entry, name)
                    MoverHandler().check_document_files(entry, name)
                    MoverHandler().check_design_files(entry, name)
                    MoverHandler().check_archive_files(entry, name)
                    MoverHandler().check_script_files(entry, name)


def move_file(entry, dest_dir, name):
    dest_file_path = join(dest_dir, name)
    if exists(dest_file_path):
        filename, extension = splitext(name)
        counter = 1
        while exists(join(dest_dir, f"{filename}({counter}){extension}")):
            counter += 1
        dest_file_path = join(dest_dir, f"{filename}({counter}){extension}")

    try:
        move(entry, dest_file_path)
    except FileNotFoundError:
        print(f"File not found: {entry}")
    except Exception as e:
        print(f"Error moving file {entry} to {dest_file_path}: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
