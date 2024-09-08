import os
from datetime import datetime

def get_word_list_from_files(folder, filter_keyword="yes"):
    """Reads all .txt files in the folder with 'filter_keyword' in the name and returns a combined word list."""
    combined_word_list = set()
    for filename in os.listdir(folder):
        if filename.endswith(".txt") and filter_keyword in filename:
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as file:
                words = file.read().splitlines()
                combined_word_list.update(words)
    return combined_word_list


def update_word_file(original_file, words_to_remove, suffix="_corrected"):
    """Removes specified words from the original word lisd and saves new one with a suffix."""

    with open(original_file, 'r', encoding='utf-8') as file:
        original_words = file.read().splitlines()

    # Remove the words from the original list
    corrected_words = [word for word in original_words if word not in words_to_remove]

    # Save the corrected word list with a new filename
    today = datetime.today()
    date_string = today.strftime('%Y-%m-%d')
    new_file_path = original_file[:-4] + suffix + "-" + date_string + ".txt"
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(corrected_words))

    print("Processed and saved:\n" + f"{new_file_path}")


def main():
    # Step 1: Create a combined word list from files with "yes" in their name (from the manualcheck program outputs)
    manchck_proc_folder = '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp5-pyspck/eren_manchck-proc'  # Set this to your folder path
    combined_word_list = get_word_list_from_files(manchck_proc_folder, filter_keyword="yes")

    # Step 2: Remove those words from other word list (file fed into the manualcheck porgram)
    original_words = '/Users/USER/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp5-pyspck/metadata/file-error-unknowns.txt' 
    update_word_file(original_words, combined_word_list, suffix="_corrected")

    # Step 3: Remove those words from being marked as misspelled in the txt files
    # --NOT IMPLEMENTED YET--

if __name__ == "__main__":
    main()
