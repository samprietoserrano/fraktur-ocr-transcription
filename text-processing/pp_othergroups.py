import os
import re

def process_file_ln(file_path, exit_path=None):
    """This file exclusively removes the line number of the text using the regions as markings."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    new_lines = []
    skip_next_line = False
    region_encountered = False

    for line in lines:
        if not line.split():
            continue
        if "Region" in line:
            region_encountered = True
            new_lines.append(line)
            skip_next_line = True  # Skip the line immediately after "Region"
        elif skip_next_line:
            skip_next_line = False  # Skip this line
        elif region_encountered:
            new_lines.append(line)  # Keep this line
            skip_next_line = True  # Skip the next line
        else:
            new_lines.append(line)  # This case handles lines before the first "Region"

    path = file_path if exit_path is None else exit_path
    with open(path, 'w') as file:
        file.writelines(new_lines)


def process_lines(file_path, nm_path, ym_path):
    """Cleans the text in each line and saves output with and without margin lines."""

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    processed_lines = []
    non_margin = []
    region_count = 0
    before_margin = True
    for line in lines:
        if "margin" in line.lower():
            before_margin = False

        line = line.replace('=', '-').replace('¬', '-')
        if "region" in line.lower():
            region_count += 1
            if region_count == 1:
                continue  # Remove the first line that contains "Region"
            if before_margin:
                non_margin.append('\n')
            processed_lines.append("\n")  # Add an new line for all other "Region"
            continue

        if before_margin:
            non_margin.append(line)
        processed_lines.append(line)

        if line.lower().endswith('register.\n') or line.lower().endswith('pag.\n'):
            if before_margin:
                non_margin.append(line)
            processed_lines.append('\n')  

        if len(processed_lines) >= 2:
            if line[0].islower() and len(processed_lines[-2]) < 3:
                if before_margin:
                    non_margin[-2] = line
                    del non_margin[-1]

                processed_lines[-2] = line
                del processed_lines[-1]

    # Save the non-margin-containing lines
    with open(nm_path, 'w') as file:
        file.writelines(non_margin)

    # Save the yes-margin-containing lines
    with open(ym_path, 'w') as file:
        file.writelines(processed_lines)


def process_folder(folder_path, option, exit_folders=[]):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            if option == "lines":
                exit_path = None if len(exit_folders) == 0 else os.path.join(exit_folders[0], file_name)
                process_file_ln(file_path, exit_path)
                print(f"Processed line number removal for '{file_name}'")
            elif option == "text":
                exits = []
                for folder in exit_folders:
                    os.makedirs(folder, exist_ok=True)
                    exit = os.path.join(folder, file_name)
                    exits.append(exit)
                process_lines(file_path, exits[0], exits[1])
                print(f"Processed line corrections for '{file_name}'")


def main():
    ### This script is highly CUSTOMIZABLE since it handled 8 different page groups with different needs. ###

    folder_in = '/Users/USER/Documents/CESTA-Summer/output-txt/from-transkribus/tables'
    folders_out = ['/Users/USER/Documents/CESTA-Summer/output-txt/from-transkribus/tables/pp-no-margin',
                  '/Users/USER/Documents/CESTA-Summer/output-txt/from-transkribus/tables/pp-w-margin']

    select = 1
    if select == 1:
        # Remove line numbers, save in place
        process_folder(folder_in, "lines")
    elif select == 2:    
        # Correct lines, save output seperately
        process_folder(folder_in, "text", folders_out)
    elif select == 3:
        # DO BOTH (remove line numbers and then corrent the lines)
        process_folder(folder_in, "lines")
        process_folder(folder_in, "text", folders_out)

if __name__ == "__main__":
    main()
