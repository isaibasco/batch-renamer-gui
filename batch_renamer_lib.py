import os
import shutil
import logging


class BatchRenamer:
    def __init__(self, 
                 filepath=None,
                 copy_files=False,
                 filetypes=None,
                 strings_to_find=None,
                 string_to_replace='',
                 prefix=None,
                 suffix=None):
        self.filepath = filepath
        self.copy_files = copy_files
        self.filetypes = filetypes
        self.strings_to_find = strings_to_find
        self.string_to_replace = string_to_replace
        self.prefix = prefix
        self.suffix = suffix

        self.initialize_logger()


    def initialize_logger(self, print_to_screen=False):
        """
        Creates a logger

        Args:
          print_to_screen: for printing to screen as well as file
        """

        ###############
        # Basic Setup #
        ###############
        app_title = 'BatchRenamer'
        version_number = '1.0.0'
        # get the path the script was run from, storing with forward slashes
        source_path = os.path.dirname(os.path.realpath(__file__))
        # create a log filepath
        logfile_name = f'{app_title}.log'
        logfile = os.path.join(source_path, logfile_name)

        # tell the user where the log file is
        print(f'Logfile is {logfile}')

        # more initialization
        self.logger = logging.getLogger(f'{app_title} Logger')
        self.logger.setLevel(logging.INFO)
        
        ###############################
        # Formatter and Handler Setup #
        ###############################
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.INFO)
        # formatting information we want 
        # (time, self.logger name, version, etc.)
        formatter = logging.Formatter(
            f'%(asctime)s - %(name)s  {version_number} - ''%(levelname)s - %(message)s')
        # setting the log file format
        file_handler.setFormatter(formatter)
        # clean up old handlers
        self.logger.handlers.clear()

        # add handler
        self.logger.addHandler(file_handler)

        # allowing to print to screen
        if print_to_screen:
            # create a new "stream handler" for logging/printing to screen
            console = logging.StreamHandler()
            self.logger.addHandler(console)
            # setting the print log format
            console.setFormatter(formatter)

        self.logger.info('Logger Initiated')


    def get_renamed_file_path(self, existing_name, string_to_find, 
                              string_to_replace, prefix, suffix):
        """
        Returns the target file path given an existing file name and 
        string operations

        Args:
          existing_name: the existing file's name
          string_to_find: a string to find and replace in the existing 
          filename
          string_to_replace: the string you'd like to replace it with
          prefix: a string to insert at the beginning of the file path
          suffix: a string to append to the end of the file path
        """

        # Extract the base filename and its extension
        base_name, ext = os.path.splitext(existing_name)
        
        # If multiple strings are provided:
        # Replace them longest-first to avoid partial replacements
        if isinstance(string_to_find, (list, tuple)):
            sorted_strings = sorted(
                string_to_find, key=len, reverse=True
            )  # Avoid partial replacements
            for find in sorted_strings:
                base_name = base_name.replace(find, string_to_replace)
        # If it's a single string, apply direct replacement        
        elif string_to_find:
            base_name = base_name.replace(string_to_find, string_to_replace)

        # Return the new filename with prefix, base name, suffix, and extension
        return f"{prefix}{base_name}{suffix}{ext}"


    def get_files_with_extension(self, folder_path, extension):
        """
        Returns a collection of files in a given folder with an extension that 
        matches the provided extension

        Args:
          folder_path: The path of the folder whose files you'd like to search
          extension: The extension of files you'd like to include in the return
        """

        # Check if the folder path is valid
        if not os.path.isdir(folder_path):
            self.logger.error(f"Folder not found: {folder_path}")
            return []
        
        # Retrieve only files that match specified extension
        files = [
            f for f in os.listdir(folder_path) if f.endswith(f".{extension}")
            ]

        # Log a warning if no matching files are found
        if not files:
            self.logger.warning(
                f"No files with .{extension} found in {folder_path}"
                )
        return files


    def rename_file(self, existing_name, new_name, copy=False):
        """
        Renames a file if it exists
        By default, should move the file from its original path to its new path
        removing the old file
        If copy is set to True, duplicate the file to the new path

        Args:
          existing_name: full filepath a file that should already exist
          new_name: full filepath for new name
          copy_mode: copy instead of rename
        """

        # Ensure the file exists before renaming or copying
        if not os.path.isfile(existing_name):
            self.logger.error(f"File not found: {existing_name}")
            return
        
        # Ensure the new filename does not already exist to prevent overwriting
        if os.path.isfile(new_name):
            self.logger.error(f"Target filename already exists: {new_name}")
            return
        
        try:
            # Copy the file if 'copy' is set to True, otherwise rename it
            if copy:
                shutil.copy(existing_name, new_name)
                self.logger.info(f"Copied: {existing_name} -> {new_name}")
            else:
                shutil.move(existing_name, new_name)
                self.logger.info(f"Renamed: {existing_name} -> {new_name}")
        except Exception as e:
            # Log unexpected errors during the renaming process
            self.logger.error(
                f"Failed to rename {existing_name} to {new_name}: {e}"
                )


    def rename_files_in_folder(self, folder_path, extension, string_to_find,
                               string_to_replace, prefix, suffix, copy=False):
        """
        Renames all files in a folder with a given extension

        Args:
            folder_path: the path to the folder the renamed files are in
            extension: the extension of the files you'd like renamed
            string_to_find: the string in the filename you'd like to replace
            string_to_replace: the string you'd like to replace it with
            prefix: a string to insert at the beginning of the file path
            suffix: a string to append to the end of the file path
            copy: whether to rename/move the file or duplicate/copy it
        """
        
        self.logger.info(
            (
                f"Starting file processing in: {folder_path} "
                f"(Extension: .{extension})"
            )
        )

        # Retrieve files with the given extension
        files = self.get_files_with_extension(folder_path, extension)
        
        # If no files found, log a warning and exit the function
        if not files:
            self.logger.warning(
                f"No files found with .{extension} in {folder_path}"
                )
            return

        for file_name in files:
            # Generate full old and new file paths
            old_path = os.path.join(folder_path, file_name)
            new_name = self.get_renamed_file_path(file_name, string_to_find, 
                                                  string_to_replace, prefix, 
                                                  suffix)
            new_path = os.path.join(folder_path, new_name)

            # Log file being processed
            self.logger.info(f"Processing file: {file_name} -> {new_name}")

            # Perform the rename or copy operation
            self.rename_file(old_path, new_path, copy)

        self.logger.info(f"Completed processing for folder: {folder_path}")
