import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
# You'll need to make this ui in QtDesigner
# And convert it to a .py file using the MakeUIPy.bat file
from batch_renamer_ui import Ui_MainWindow 
# Recommend you rename this
import batch_renamer_lib as renamer


class BatchRenamerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # UI Setup
        super().__init__()
        super(Ui_MainWindow).__init__()
        self.setupUi(self)
        # Connect button to function
        self.pushButton_Browse.clicked.connect(self.get_filepath)
        # Connect your new "Run" button to self.run_renamer
        self.pushButton_Run.clicked.connect(self.run_renamer)

        # Instance the "back end"
        self.batch_renamer = renamer.BatchRenamer()
        
        # Show UI normal vs maximized
        self.showNormal()


    def get_filepath(self):
        """
        Open a file dialog for browsing to a folder
        """
        self.filepath = QFileDialog().getExistingDirectory()
        self.set_filepath()


    def set_filepath(self):
        """
        Set lineEdit text for filepath
        """
        self.lineEdit_FilePath.setText(self.filepath)
        self.update_list()


    def update_list(self):
        """
        Clear listwidget
        read files in filepath with os.walk
        Add files as new items
        """
        self.listWidget.clear()
        for root, dirs, files in os.walk(self.filepath):
            self.listWidget.addItems(files)


    # Add a function to gather and set parameters based upon UI
    # e.g. lineEdit.text() or radioButton.isChecked
    # remember that you may need to check to see if the result
    # was a tuple and correct like so:
    # self.filepath = self.filepathEdit.text()
    # if type(self.filepath) is tuple:
    #     self.filepath = self.filepath[0]


    def run_renamer(self):
        """
        Run back end batch renamer using self.batch_renamer
        self.batch_renamer is an instance of the BatchRenamer class
        """

        # Gather inputs from UI
        filepath = self.lineEdit_FilePath.text()
        filetypes = self.lineEdit_Filetypes.text()
        prefix = self.lineEdit_Prefix.text()
        suffix = self.lineEdit_Suffix.text()
        strings_to_find = self.lineEdit_StringsToFind.text().split(',')
        string_to_replace = self.lineEdit_StringsToReplace.text()
        copy_mode = self.radioButton_Copy.isChecked()

        # Update the BatchRenamer instance with new inputs
        self.batch_renamer.filepath = filepath
        self.batch_renamer.filetypes = filetypes
        self.batch_renamer.prefix = prefix
        self.batch_renamer.suffix = suffix
        self.batch_renamer.strings_to_find = strings_to_find
        self.batch_renamer.string_to_replace = string_to_replace
        self.batch_renamer.copy_files = copy_mode

        # Call the rename function
        self.batch_renamer.rename_files_in_folder(
            folder_path=filepath,
            extension=filetypes,
            string_to_find=strings_to_find,
            string_to_replace=string_to_replace,
            prefix=prefix,
            suffix=suffix,
            copy=copy_mode
        )

        # Refresh the file list in the ListWidget
        self.update_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatchRenamerWindow()
    sys.exit(app.exec())
 