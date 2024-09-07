import os
import re
import shutil

def make_map(map_path):
    """Takes in the mapping file and creates actual dictionary object."""
    with open(map_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    mapping = {}
    for line in lines:
        extr = re.findall(r'\d+', line)
        nums = list(map(int, extr)) 
        realp, filep = nums[0], nums[1]
        mapping[filep] = realp
    return mapping


def copy_txt(map_path, source_folder, target_folder):
    """Takes in the mapping file and copies the files with their mapped names instead."""
    # Create the target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # Make a dictionary out of our mapping file
    mapping = make_map(map_path)
    copies = 0
    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith('.txt'):
            tmp = re.findall(r'\d+', file_name)
            n = list(map(int, tmp)) 
            file_n = n[0]

            output_n = mapping[file_n]
            output_s = str(output_n) + '.txt'
            source_path = os.path.join(source_folder, file_name)
            target_path = os.path.join(target_folder, output_s)
            shutil.copy2(source_path, target_path)

            copies +=1 
            # if copies < 10:
            #     continue
            # break
    print(str(copies) + " copies made.")


def copy_txt_simple(source_folder, target_folder):
    """Copies the files with their same names, no mapping."""
    copies = 0
    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith('.txt'):
            source_path = os.path.join(source_folder, file_name)
            target_path = os.path.join(target_folder, file_name)
            shutil.copy2(source_path, target_path)

            copies +=1 
            # if copies < 10:
            #     continue
            # break
    print(str(copies) + " copies made.")


def remove_files(folder):
    """Remove every file in the folder."""
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                # print(f"File {file_name} has been deleted.")
            else:
                print(f"File {filename} did not exist.")


group_paths = {
    "begin": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/beginning/pp1', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/beg-text-map.txt'],
    "toc": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/toc/pp1', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/toc-text-map.txt'],
    "starts": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/nonsimple-starters/pp2-nm-pyspck', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/nonsimple-text-map.txt'],
    "main": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp5-pyspck', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/main-text-map.txt'],
    "tables": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/tables/pp-no-margin', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/tables-text-map.txt'],
    "other": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/other/pp-no-margin', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/other-text-map.txt'],
    "index": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/index/pp2-merged-pyspck', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/index-text-map.txt'],
    "dict": ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/definitions/pp1', 
              '/Users/samxp/Documents/CESTA-Summer/mappings/dict-text-map.txt']
}

def main():
    target_folder = '/Users/samxp/Documents/CESTA-Summer/output-txt/merged' 

    task = input("Do you want to 'remove' or 'load'? ")
    if 'remove' in task:
        remove_files(target_folder)
        print("All txt files in folder removed.")
    else:
        for group in group_paths:
            if 'begin' in group or 'toc' in group:
                copy_txt_simple(group_paths[group][0], target_folder)
            else:
                copy_txt(group_paths[group][1], group_paths[group][0], target_folder)

if __name__ == "__main__":
    main()
