
#Compares contents of two directory and contents of same files.
#It is my local SVN like code comparison

import os
import filecmp
from difflib import unified_diff

def list_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_list.append(os.path.join(root, file))
    return file_list

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    diff = unified_diff(file1_lines, file2_lines, fromfile=file1, tofile=file2, lineterm='')
    return '\n'.join(diff)

def compare_directories(dir1, dir2, output_file, summary_file):
    files1 = list_files(dir1)
    files2 = list_files(dir2)

    all_files = set(os.path.relpath(file, dir1) for file in files1).union(
                os.path.relpath(file, dir2) for file in files2)

    differences = {}
    summary = []
    
    for file in all_files:
        path1 = os.path.join(dir1, file)
        path2 = os.path.join(dir2, file)
        if os.path.exists(path1) and os.path.exists(path2):
            if not filecmp.cmp(path1, path2):
                differences[file] = compare_files(path1, path2)
                summary.append(path1)  # Full path from dir1
        else:
            if not os.path.exists(path1):
                differences[file] = f"{file} does not exist in {dir1}"
                summary.append(path1)
            if not os.path.exists(path2):
                differences[file] = f"{file} does not exist in {dir2}"
                summary.append(path2)

    with open(output_file, 'w') as f:
        for file, diff in differences.items():
            if diff:
                f.write(f"Differences in {file}:\n{diff}\n\n")

    with open(summary_file, 'w') as f:
        for file in summary:
            f.write(f"{file}\n")

# Usage
dir1 = r'C:\Users\xxx\Downloads\x-x-v262\'
dir2 = r'C:\Users\yyy\Downloads\y-y-v271\'
output_file = 'detailed_differences_report.txt'
summary_file = 'summary_report.txt'
compare_directories(dir1, dir2, output_file, summary_file)

 

 
