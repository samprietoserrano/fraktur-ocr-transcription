import os
import re

def process_file_ln(file_path):
    """This file exclusively removes the line number of the text using the regions as markings."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    new_lines = []
    skip_next_line = False
    region_encountered = False

    for line in lines:
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

    with open(file_path, 'w') as file:
        file.writelines(new_lines)


def correct_line(line):
    """Uses several regex patterns to filter unneeded characters or substrings."""
    # Replacing every à character with a letter a character
    line = line.replace('à', 'a')
    
    # Replacing every >> or << with an s character
    line = line.replace('>>', 's').replace('<<', 's')
    
    # Replacing every = with a - character
    line = line.replace('=', '-')
    
    # Replacing every : with a period character
    line = line.replace(':', '.')
    
    # If the line contains "Google", remove the line
    if "Google" in line:
        return ''
    
    # If the line starts with a digit and is less than 7 characters long, remove any spaces in the line
    if len(line) < 7:
        line = line.replace(' ', '')
    
    # If the line starts with "ibid", remove any spaces
    if line.startswith('ibid'):
        line = line.replace(' ', '').replace('\t', '')

    # Define a regular expression pattern to find " . a" or " . b"
    # Use re.sub() to replace occurrences of the pattern with spaces removed
    pattern = r'\. [ab]'
    line = re.sub(pattern, lambda match: match.group().replace(' ', ''), line)

    return line


def process_lines(file_path, exitpath):
    """Processes the main index pages, no special ones."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    processed_lines = []
    region_count = 0
    for line in lines:
        # Sends line to receive several regex corrections
        corrected_line = correct_line(line)

        if not corrected_line: # if line got fully replaced
            continue
            
        # Add formatting between "regions" of the text/Transkribus export
        if "Region" in corrected_line:
            region_count += 1
            if region_count == 1:
                continue  # Remove the first line that contains "Region"
            processed_lines.append("\n")  # Add an new line for all other "Region"
            continue
        
        # Merges lines if there is something too short or numbers are hanging off
        if (re.match(r'^\d', corrected_line.strip()) and len(corrected_line.strip()) <= 7) \
                                    or corrected_line.strip().startswith('ibid') \
                                    or (len(re.findall(r'[a-zA-Z]', corrected_line)) < 3):
            if processed_lines:
                processed_lines[-1] = processed_lines[-1].strip()+ ' ' + corrected_line
            else:
                processed_lines.append(corrected_line)
        else:
            processed_lines.append(corrected_line.strip())

        # Uses regex to fix all the line endings with '.a' and '.b'
        if len(processed_lines) >= 2:
            if (processed_lines[-2].endswith('.a\n') or processed_lines[-2].endswith('.b\n') or processed_lines[-2].endswith('.\n')) \
                    and processed_lines[-1][0].isupper():
                processed_lines.append(processed_lines[-1])
                processed_lines[-2] = '\n'
        
        # Add empty line after index headings
        if corrected_line.lower().endswith('register.\n') or corrected_line.lower().endswith('pag.\n') :
            processed_lines.append('\n')

    with open(exitpath, 'w') as file:
        file.writelines(processed_lines)


def process_lines_special(file_path, exitpath):
    """Processes the special index pages."""
    
    # Find the 'page number' of file for filtering later
    temp = re.findall(r'\d+', exitpath)
    res = list(map(int, temp)) 
    file_n = res[1]

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    processed_lines = []
    region_count = 0
    for line in lines:
        line = line.replace('=', '-')

        # Add formatting between "regions" of the text/Transkribus export
        if "region" in line.lower():
            region_count += 1
            if region_count == 1:
                continue  # Remove the first line that contains "Region"
            processed_lines.append("\n")  # Add an new line for all other "Region"
            continue
        
        # Follow specific steps for certain regions of the special pages (req'd human inspection)
        if file_n == 76:
            processed_lines.append(line)
        else:
            if file_n == 77 and region_count == 1:
                processed_lines.append(line)
                continue
            if file_n == 80 and region_count == 3:
                processed_lines.append(line)
                continue
            if line[0].isalpha():
                if "pag" in line.lower():
                    continue
                if processed_lines:
                    if len(line) < 15:
                        processed_lines[-1] = processed_lines[-1].strip('\n') + ' ' + line
                    else: 
                        processed_lines.append("\t" + line)
                else:
                    processed_lines.append(line)
            else:
                if len(line) < 3:
                    continue
                temp = re.findall(r'\d+', line)
                nums = len(list(map(int, temp)))
                if nums < 3:
                    processed_lines.append("\t" + line)
                else:
                    processed_lines.append(line)
        
    with open(exitpath, 'w') as file:
        file.writelines(processed_lines)


def process_folder(folder_path, exit_folder, option):
    """Processes the index pages in three groups."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            if option == 1:
                process_file_ln(file_path)
                print(f"Processed line numbers for '{file_name}'")
            elif option == 2:
                pattern = re.compile(r'\b(76|77|78|79|80)\b')
                if bool(pattern.search(file_name)):
                    print(f"Skipped line corrections for '{file_name}'")
                else:
                    exit_path = os.path.join(exit_folder, file_name)
                    process_lines(file_path, exit_path)
                    print(f"Processed line corrections for '{file_name}'")
            elif option == 3:
                pattern = re.compile(r'\b(76|77|78|79|80)\b')
                if bool(pattern.search(file_name)):
                    exit_path = os.path.join(exit_folder, file_name)
                    process_lines_special(file_path, exit_path)
                    print(f"Processed special line corrections for '{file_name}'")

def main():
    input_folders = ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/index',
                     '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/index/pp1']
    exit_folders = ['/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/index/pp1',
                    '/Users/samxp/Documents/CESTA-Summer/output-txt/from-transkribus/index/pp2']

    select = 3
    # Options for 'select':
    #   1- Remove line numbers
    #   2- Correct lines for MAIN pages of index
    #   3- Correct lines for SPECIAL pages of index

    input_folder = input_folders[select-1]
    exit_folder = exit_folders[select-2]
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(exit_folder, exist_ok=True)

    process_folder(input_folder, exit_folder, select)


if __name__ == "__main__":
    main()
