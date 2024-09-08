import enchant
import os
import re
# from tqdm import tqdm

# Initialize the German dictionary
german_dict = enchant.Dict("de_DE")

def valid_fraktur_deu(word):
    """Bool on if the word has valid structure."""
    # Define a regex pattern for valid Fraktur characters
    pattern = re.compile(r'^[a-zA-ZäöüßÄÖÜſẞ]+$')
    
    # Check if the word matches the Fraktur character pattern
    if not pattern.match(word):
        return False
    
    # Check if the word is in the German dictionary
    return german_dict.check(word)


def correct_word(word):
    """Return the PyEchant suggestion, if needed and if available."""
    # Check if the word is valid
    if german_dict.check(word):
        return word
    
    # Get suggestions for the invalid word
    suggestions = german_dict.suggest(word)
    
    # If there are suggestions, return the best one
    if suggestions:
        return suggestions[0]
    
    # If no suggestions, return the original word
    return word


def correct_line(line):
    """Uses Py Enchant to include suggested corrections for words not recognized as valid."""
    # Define a regex pattern for valid Fraktur characters
    pattern = re.compile(r'\b[a-zA-ZäöüßÄÖÜſẞ]+\b')
    
    # Find all words in the line
    words = pattern.findall(line)
    
    # Correct each word
    corrected_words = [correct_word(word) for word in words]
    
    # Replace the original words with the corrected words in the line
    for original, corrected in zip(words, corrected_words):
        line = line.replace(original, corrected)
    
    return line


def correct_lines(file_path, output_path):
    """Goes line by line to correct the spelling in each.
        NOT RECOMMENDED, DEPRECATED."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    corrected_lines = [correct_line(line) for line in lines]
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(corrected_lines)


def other_head_endings(line):
    """RegEx function to match pattern of the page headings."""
    if line.endswith("2c.\n") or line.endswith("c.\n") or line.endswith("2.\n") \
        or line.endswith("Brief.\n") or line.endswith("Briefe.\n") \
            or line.endswith(":c\n") or line.endswith("..\n") or line.endswith(" t\n"):
        return True
    return False


def format_lines(file_path, exit_path):
    """This function adds formatting to the lines, specifically adding separation between 
        headings and parapgraphs."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    read_lines = []
    lines_c = 0
    for line in lines:
        words = re.findall(r'\b[a-zA-ZáäöüßÄÖÜſẞ]+\b', line)
        # Skip over empty or page-number lines 
        if len(words) < 1:
            continue
        
        # Add formatting/spacing between the headings of the page and the text
        if line[-2] == ".":
            last_word = words[-1] 
            head_pattern = re.compile(r'\d+\.$')
            if not valid_fraktur_deu(last_word):
                if len(words) > 3:
                    line = line[:-2] + '-\n'
                    read_lines.append(line)
                    lines_c += 1
                else:
                    read_lines.append(line)
                    read_lines.append('\n')
                    lines_c = 0
            elif bool(head_pattern.search(line)) or other_head_endings(line):
                read_lines.append(line)
                read_lines.append('\n')
                lines_c = 0
            elif lines_c > 5:
                read_lines.append(line)
                read_lines.append('\n')
                lines_c = 0
            else:
                read_lines.append(line)
                lines_c += 1
        else:
            if other_head_endings(line):
                read_lines.append(line)
                read_lines.append('\n')
                lines_c = 0
                continue
            read_lines.append(line)
            lines_c += 1

    # Write out all the other non-skipped lines
    with open(exit_path, 'w') as file:
        file.writelines(read_lines)


def process_lines(file_path, exit_path):
    """This function processes line to line errors, such as odd empties and odd short lines."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Define the regex pattern for lines starting with punctuation, and then skip those
    pattern = re.compile(r'^[\.,:;!?]+$')
    lines = [line for line in lines if not pattern.match(line)]

    processed_lines = []
    lines_c = 0
    page_n = True
    for line in lines:
        lines_c += 1
        # Skip over the 'digitize' line 
        if "digitize" in line.lower():
            continue
        
        # Skip over the very last line
        if lines_c == (len(lines) - 1):
            processed_lines.append(line)
            continue

        words = re.findall(r'\b[a-zA-ZáäöüßÄÖÜſẞ]+\b', line)  
        # Process lines that are oddly short      
        if len(words) <= 3:
            # Skip line with just a number, unless it could be the page number from the top
            if bool(re.match(r'^\d', line)) and page_n:
                if bool(re.match(r'^0', line)):
                    continue
                if len(processed_lines) > 10:
                    processed_lines.append("\n")
                processed_lines.append(line)
                processed_lines.append("\n")
                page_n = False
                continue
            elif bool(re.match(r'^\d', line)):
                continue

            # If line is not end of sentence, attach to prev line
            if line[-2] != '.' and line[-2] != ':':
                if len(processed_lines):
                    if len(processed_lines[-1]) < 40:
                        if len(line) <= 5:
                            processed_lines[-1] = processed_lines[-1].strip('\n') + ' ' + line
                    elif len(processed_lines[-1]) < 30:
                        if len(line) <= 10:
                            processed_lines[-1] = processed_lines[-1].strip('\n') + ' ' + line
                    else:
                        processed_lines.append(line)
            else:
                processed_lines.append(line)
        else:
            processed_lines.append(line)
    
    # Write out all the other non-skipped lines
    with open(exit_path, 'w') as file:
        file.writelines(processed_lines)


def process_folder(folder_path, exit_folder, opt):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            exit_path = os.path.join(exit_folder, file_name)
            if opt == 1:
                process_lines(file_path, exit_path)
            elif opt == 2:
                format_lines(file_path, exit_path)
            elif opt == 3:
                correct_lines(file_path, exit_path)
            print(f"Post-processed: '{file_name}'")


def main():
    input_folders = ['/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script',
                     '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp1',
                    '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp2']
    exit_folders = ['/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp1',
                    '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp2',
                    '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp3']

    select = 3
    # Options for 'select':
    #   1- First run of post-processing, only line to line
    #   2- Second run of post-processing, formats text in each line
    #   3- DEPRECATED: Third run of post-processing, corrects text in each line using PyEncant `suggest`

    input_folder = input_folders[select-1]
    exit_folder = exit_folders[select-1]
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(exit_folder, exist_ok=True)
    
    process_folder(input_folder, exit_folder, select)

if __name__ == "__main__":
    main()
