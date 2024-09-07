import os

def get_source():
    """Generate the source file, either original or the remaining word list."""

    og_source = '/Users/samxp/Documents/CESTA-Summer/corpus-files/new-dta_kernkorpurs_plain/custom_words.txt'
    rem_source = '/Users/samxp/Documents/CESTA-Summer/corpus-files/new-dta_kernkorpurs_plain/manchck/custom_words-remaining.txt'

    if not os.path.exists(rem_source):
        return og_source, rem_source
    return rem_source, rem_source


def check_and_autoupdate(lines):
    """
    This version of the manual check (aka manual review) of works without saving yes/no lists.
    Instead, continually update the source word list by keeping or removing words. 
    Updating works by copying the word that the user terminates/pauses on as the first word of the list
    and continuing to read from that index forth. 
    """
    first_word = lines[0]
    if lines.count(first_word) > 2:
        lines.pop(0)
    next_line_index = lines.index(first_word)

    for i in range(next_line_index, len(lines)):
        next_word = lines[i][:-1]
        if not next_word:
            continue
        
        user_input = input(f"{next_word}: (y/n) ")
        
        if user_input == "":
            print("Terminating and saving progress...")
            next_word = next_word + "\n"
            lines.insert(0, next_word)
            remaining_lines = lines
            break
        elif user_input.lower() == "y":
            continue
        elif user_input.lower() == "n":
            lines.pop(i)
        else:
            print("Invalid input, please enter 'y', 'n', or just press enter to terminate.")
            continue
    else:
        remaining_lines = lines

    return remaining_lines

def main():
    source_file, future_file = get_source()

    try:
        with open(source_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{source_file}' does not exist.")
        return
    
    remaining_lines = check_and_autoupdate(lines)

    with open(future_file, 'w') as f:
        f.writelines(remaining_lines)
    print("Remaining lines saved to 'custom-words-remaining.txt'")

if __name__ == "__main__":
    main()
