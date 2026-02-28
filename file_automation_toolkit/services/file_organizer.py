import os
import shutil

def organize_files(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            extension = file.split(".")[-1]
            new_folder = os.path.join(folder, extension)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            shutil.move(file_path, os.path.join(new_folder, file))
