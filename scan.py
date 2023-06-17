import os
from virus_total import scan_file
import re
import concurrent.futures

# Function to recursively scan a directory and retrieve file paths
def scan_directory(directory, file_extension):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_extension):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths

# Function to scan the Windows file system for executable files
def scan_windows_filesystem():
    # Specify the root directory to start scanning (e.g., C:\)
    root_directory = 'C:\\'

    # Specify the file extension to filter (e.g., .exe)
    file_extension = '.exe'

    # Scan the directory and retrieve file paths
    file_paths = scan_directory(root_directory, file_extension)

    # Create a list to store the suspicious file paths
    suspicious_file_paths = []

    # Check each file path for suspicious files
    for file_path in file_paths:
        if is_file_suspicious(file_path):
            suspicious_file_paths.append(file_path)

    # Scan the suspicious file paths using multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scan_file, suspicious_file_paths)

# Function to check if a file is suspicious
def is_file_suspicious(file_path):
    # Define a regex pattern to match suspicious file names
    pattern = r'^(?!trusted_)[a-zA-Z0-9_]+\.exe$'

    # Extract the file name from the file path
    file_name = os.path.basename(file_path)

    # Check if the file name matches the regex pattern
    if re.match(pattern, file_name):
        return True  # File name is suspicious
    else:
        return False

