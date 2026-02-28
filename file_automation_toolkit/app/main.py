from services.file_organizer import organize_files

if __name__ == "__main__":
    folder_path = input("Enter folder path: ")
    organize_files(folder_path)
    print("Files organized successfully")
