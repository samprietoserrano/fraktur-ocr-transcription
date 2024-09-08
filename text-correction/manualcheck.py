import os

def get_source():
    """Generate the source file, either original or the remaining word list."""

    # Find dir where script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if 'USER' in script_dir:
        og_source = '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp5-pyspck/metadata/file-error-unknowns.txt'
        rem_source = '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp5-pyspck/metadata/manchck-proc/source-remaining.txt'
    
        if not os.path.exists(rem_source):
            return og_source, rem_source, script_dir
        return rem_source, rem_source, script_dir
    else:
        og_source = script_dir + '/file-error-unknowns.txt'
        rem_source = script_dir + 'manchck-proc/source-remaining.txt'

        if not os.path.exists(rem_source):
            return og_source, rem_source, script_dir
        return rem_source, rem_source, script_dir


def get_next_filename(folder, base_name, extension):
    """Generate the next available filename with an incrementing suffix."""
    counter = 1
    while True:
        filename = f"{base_name}{f'-{counter:02}' if counter > 1 else ''}.{extension}"
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            return filename
        counter += 1


def save_list_to_file(words_list, base_name, script_dir):
    """Save the list of words to a text file."""
    if 'USER' in script_dir:
        folder = '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp5-pyspck/metadata/manchck-proc'
    else:
        folder = script_dir + '/manchck-proc'
    os.makedirs(folder, exist_ok=True)

    filename = get_next_filename(folder, base_name, 'txt')

    path = os.path.join(folder, filename)
    with open(path, 'w') as f:
        f.write("\n".join(words_list))
    print(f"Saved {len(words_list)} words to {filename}")


def main():
    source_file, future_file, script_dir = get_source()

    try:
        with open(source_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{source_file}' does not exist.")
        return
    
    yes_list = []
    no_list = []
    
    for i, line in enumerate(lines):
        first_word = line.split()[0] if line.split() else ''
        if not first_word:
            continue
        
        user_input = input(f"{first_word}: (y/n) (return to terminate/save) ")
        
        if user_input == "":
            print("Terminating and saving progress...")
            remaining_lines = lines[i:]
            break
        
        elif user_input.lower() == "y":
            yes_list.append(first_word)
        elif user_input.lower() == "n":
            no_list.append(first_word)
        else:
            print("Invalid input, please enter 'y', 'n', or just press enter to terminate.")
            continue
    else:
        remaining_lines = []  # No lines left to process, terminate loop.
    
    # Save the yes_list and no_list to files
    save_list_to_file(yes_list, 'yes-list-words', script_dir)
    save_list_to_file(no_list, 'no-list-words', script_dir)
    
    # Save the remaining lines to a new source file
    if remaining_lines:
        with open(future_file, 'w') as f:
            f.writelines(remaining_lines)
        print("Remaining lines saved to 'source-remaining.txt'")
    else:
        print("No remaining lines to save.")


if __name__ == "__main__":
    main()
