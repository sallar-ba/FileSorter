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

image_extensions = {".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"}
video_extensions = {".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"}
audio_extensions = {".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"}
document_extensions = {".doc", ".docx", ".odt", ".txt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"}
design_extensions = {".psd", ".ai", ".indd", ".indt"}
archive_extensions = {".zip", ".rar", ".7z", ".tar", ".gz"}
script_extensions = {".py", ".java", ".cpp", ".c", ".cs", ".js", ".html", ".css", ".php", ".rb", ".r", ".go", ".sh", ".pl", ".swift", ".kt", ".ts", ".lua"}

source_dir = ""

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            time.sleep(1)
            with scandir(source_dir) as entries:
                for entry in entries:
                    self.process_file(entry)

    def process_file(self, entry):
        name = entry.name.lower()
        ext = splitext(name)[1]
        
        if ext in audio_extensions:
            self.move_to_category(entry, "Music")
        elif ext in video_extensions:
            self.move_to_category(entry, "Video")
        elif ext in image_extensions:
            self.move_to_category(entry, "Image")
        elif ext in document_extensions:
            self.handle_document(entry, ext)
        elif ext in design_extensions:
            self.move_to_category(entry, "Design")
        elif ext in archive_extensions:
            self.move_to_category(entry, "Archives")
        elif ext in script_extensions:
            self.move_to_category(entry, "Scripts")

    def handle_document(self, entry, ext):
        base_dir = join(source_dir, "Documents")
        if ext == ".pdf":
            self.move_to_category(entry, join("Documents", "PDF"))
        elif ext in {".csv", ".xls", ".xlsx"}:
            self.move_to_category(entry, join("Documents", "CSV"))
        elif ext == ".txt":
            self.move_to_category(entry, join("Documents", "Text"))
        elif ext in {".doc", ".docx", ".odt"}:
            self.move_to_category(entry, join("Documents", "Word"))
        elif ext in {".ppt", ".pptx"}:
            self.move_to_category(entry, join("Documents", "PPT"))

    def move_to_category(self, entry, category):
        dest_dir = join(source_dir, category)
        move_file(entry, dest_dir, entry.name)

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
        if self.observer:
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
            self.create_directories()

    def create_directories(self):
        main_dirs = ["Music", "Video", "Image", "Design", "Archives", "Scripts"]
        doc_subdirs = ["PDF", "CSV", "Text", "PPT", "Word"]
        
        for dir_name in main_dirs:
            self.ensure_directory(join(source_dir, dir_name))
        
        documents_dir = join(source_dir, "Documents")
        self.ensure_directory(documents_dir)
        
        for subdir in doc_subdirs:
            self.ensure_directory(join(documents_dir, subdir))

    def ensure_directory(self, path):
        if exists(path):
            if isfile(path):
                remove(path)
        makedirs(path, exist_ok=True)

    def monitorFolder(self):
        if source_dir:
            if not self.monitor_thread.isRunning():
                self.monitor_thread.start()
            with scandir(source_dir) as entries:
                for entry in entries:
                    MoverHandler().process_file(entry)

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
    except Exception as e:
        print(f"Error moving file {entry} to {dest_file_path}: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
