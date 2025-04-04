# 📂 Batch Renamer GUI

This is a Python-based graphical tool designed for batch renaming or copying files. Built with PyQt6, it offers a user-friendly interface that allows artists, developers, and technical users to process files in bulk using prefix and suffix logic, targeted string replacement, and extension filtering. It supports both renaming in place and creating modified copies, while keeping a detailed log of all operations.

To use the tool, simply launch the Python script `batch_renamer_gui_starter.py`. Once the GUI opens, choose a folder containing the files you want to process. Specify the type of files to target by entering a file extension like `png`, `txt`, or `ma`. You can optionally provide a prefix or suffix to be added to each filename, or set up a simple find-and-replace operation to clean up or customize filenames further. Multiple find terms can be entered by separating them with commas. The tool then gives you the choice to either rename the files directly or make copies with the new names, leaving the originals intact.

The interface includes tooltips to help guide users through each input field. After clicking the Run button, the matched files will be displayed in a list, and the renaming or copying process will begin. All results — including skipped files, conflicts, and errors — are recorded in a log file named `BatchRenamer.log`, which is saved in the same directory.

The back-end logic is handled in `batch_renamer_lib.py`, where the renaming logic, string parsing, and logging system are defined. The front-end UI behavior and connections are defined in `batch_renamer_gui_starter.py`, and the layout itself is auto-generated from a Qt Designer `.ui` file into `batch_renamer_ui.py`. The tool is fully PEP 8 compliant and includes inline documentation to support extensibility.

No overwriting occurs unless explicitly allowed, and the tool has been structured to avoid destructive operations. It has been tested across different use cases, including naming cleanup for texture files, exporting organized animation scenes, and updating documentation filenames.

To run the tool, Python 3.10 or higher is recommended. Only one dependency is required, PyQt6, which can be installed using `pip install PyQt6`. Once the script is executed, all functionality is handled through the GUI — no command-line flags or additional configuration needed.

This project was created as part of a technical art curriculum, with a focus on clean architecture, effective logging, and practical utility for asset management workflows.

MIT licensed and maintained by Isa Ibasco.
