import os
import re

def sort_filenames(files):
    # Regular expression to match the file names with numbers
    txt_file_pattern = re.compile(r'(\d+)\.txt$')

    # Filter and sort files based on numeric value in descending order
    sorted_files = []
    for f in files:
        match = txt_file_pattern.match(f)
        if match:
            # Extract the numeric value using the capturing group
            numeric_value = int(match.group(1))
            # Append the tuple (numeric_value, filename) to the list
            sorted_files.append((numeric_value, f))

    # Sort the list of tuples based on the numeric value in descending order
    sorted_files.sort(reverse=True, key=lambda x: x[0])

    # Extract the sorted filenames
    return [(f, i) for i, f in sorted_files]

def rename_txt_files(folder_path):    
    # Get all files in the directory
    files = os.listdir(folder_path)
    
    # Filter and sort files based on numeric value in descending order
    txt_files_tupled = sort_filenames(files)
    
    # Rename files in decreasing order
    for file_name, number in txt_files_tupled:
        new_number = number + 1
        new_file_name = f"{new_number:02}.txt"  # Ensure two digits with leading zeros if needed
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{file_name}' to '{new_file_name}'")

# Paths for each page group map
group_paths = {
    # "pg_begin": '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/beginning',
    # "pg_toc": '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/toc',
    "pg_starts": '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/nonsimple-starters',
    "pg_index": '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/index',
    "pg_tables": '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/tables',
    "pg_other": '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/other',
    "pg_dict": '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/definitions'
}

def main():
    for path in group_paths:
        rename_txt_files(path)

if __name__ == "__main__":
    main()
