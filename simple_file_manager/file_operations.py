# Question: File operations for a simple file manager
# Name - ADITYA BHARDWAJ
# Section - D2
# Roll No - 07
# Course – B TECH
# Branch – CSE

import os

def list_files(folder_path):
    return os.listdir(folder_path)

def open_file(file_path):
    os.startfile(file_path)

def delete_file(file_path):
    os.remove(file_path)

def create_file(file_path):
    with open(file_path, "w"):
        pass
