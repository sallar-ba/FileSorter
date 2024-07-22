# FileSorter

FileSorter is a simple PyQt6 application designed to help you organize your files by automatically categorizing them into folders based on their file extensions. With FileSorter, you can easily monitor a selected folder and ensure that your files are neatly organized for easy access.

## Features

- **GUI Application:** FileSorter provides a user-friendly graphical interface for selecting a source folder and triggering the file monitoring process.
  
- **Automatic File Categorization:** Files are automatically sorted into folders based on their file extensions, such as images, videos, music, and documents.

- **Handling Duplicates:** FileSorter handles duplicate file names by appending a counter to the filename to prevent overwriting.

- **Document Subfolders:** Within the "Documents" folder, specific subfolders are created for different document types (PDF, CSV, TEXT, PPT, WORD) to further organize your files.

- **Error Handling:** Robust error handling to ensure smooth operation, including handling race conditions and file move errors.

## Installation

To use FileSorter, follow these steps:

1. **Download:** Download the latest release from the [Releases](https://github.com/sallar-ba/FileSorter/releases) page of this repository.

2. **Extract:** Extract the downloaded ZIP file to your desired location on your computer.

3. **Install Dependencies:** Install the required dependencies using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run:** Locate the main Python file (`FileSorter.py`) and run it:
   ```bash
   python main.py
   ```

## Usage

1. **Select Source Folder:** Click on the "Select Source Folder" button to choose the folder you want to monitor for file organization.

2. **Trigger Monitoring:** Click on the "Trigger Monitoring" button to start monitoring the selected folder. FileSorter will automatically categorize incoming files into appropriate folders.

3. **View Results:** Once the monitoring process is running, you can navigate to the selected source folder to view the organized files in their respective folders.

## Contributing

If you have any suggestions, bug reports, or feature requests, feel free to open an [issue](https://github.com/sallar-ba/FileSorter/issues) or submit a [pull request](https://github.com/sallar-ba/FileSorter/pulls) to contribute to the development of FileSorter.

## Acknowledgements

- Special thanks to the PyQt6 and Watchdog libraries for providing the tools necessary to build this application.
