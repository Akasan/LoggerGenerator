class AlreadySetFolderException(Exception):
    def __init__(self):
        super().__init__("Folder for saveing log file is already set.")
