import enchant
import json
import os
import re
from collections import Counter
from spellchecker import SpellChecker

# Initialize the German dictionary
german_dict = enchant.Dict("de_DE")

def enchant_word(word):
    """Uses PyEnchant dictionary to filter valid German words."""
    if not word or german_dict.check(word):
        return True
    
    return False


def pattern_match(word):
    """Checks whether word is of valid German characters."""
    german_letter_pattern = r'^[a-zA-ZäöüÄÖÜßſẞ-]+$'
    if re.fullmatch(german_letter_pattern, word):
        if '-' in word:
            spec_hyphen_pattern = r'[a-zA-ZäöüÄÖÜßſẞ]+(?:-[a-zA-ZäöüÄÖÜßſẞ]+)*'
            if re.fullmatch(spec_hyphen_pattern, word) and word.count('-') < 2:
                return True
            return False
        return True
    return False


def process_text(text):
    """Filters the line of text to only valid German word characters."""
    punct_pattern = r'[.,;\/\\:]'
    text = re.sub(punct_pattern, '', text)

    words = text.split()
    filtered_words = [word.lower() for word in words if pattern_match(word)]
    return filtered_words


def count_corpus_files(directories):
    """Returns the number of files in the directory."""
    count = 0
    for dir in directories:
        for path in os.scandir(dir):
            if path.is_file():
                count += 1
    return count


def load_and_preprocess_files(directories, dict_path, freq_path, save_freq):
    """Load the corpus text files, process every word in them, and create a word list.
       Optionally, can also create a frequency dictionary."""
    word_list = []

    corpus_count = count_corpus_files(directories)
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    processed_words = process_text(text)
                    word_list.extend(processed_words)

                    corpus_count -= 1
                    if corpus_count % 50 == 0:
                        print(f'{corpus_count} files left')

    with open(dict_path, 'w', encoding='utf-8') as f:
        for word in sorted(set(word_list)):
            f.write(f"{word}" + "\n")

    if save_freq:
        freq_obj = get_json_obj(word_list)
        dbl_save_freq(freq_path, freq_obj)


def load_corpus(filepath):
    """Load the word list file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.readlines()
    corpus = [word[:-1] for word in text]
    return corpus


def load_freq(freq_path, load_clarin=False, upd_corpus=[], save_update=True):
    """Load the frequency dictionary JSON file.
       Optionally, can merge that dict with the CLARIN word frequency list.
       Optionally, can also create a new freq dict JSON from the provided corpus file."""
    
    if not upd_corpus:
        with open(freq_path, 'r', encoding='utf-8') as file:
            json_obj = json.load(file)
    else:
        json_obj = get_json_obj(upd_corpus)
        if save_update:
            dbl_save_freq(freq_path, json_obj)
        
    if load_clarin:
        clarin_file = '/Users/USER/Documents/CESTA-Summer/corpus-files/clarin_GeMiCorpus_1500-1700/Wordlist.txt'
        
        with open(clarin_file, 'r', encoding='utf-16-le') as f:
            lines = f.readlines()
        
        clarin_dict = {}
        for line in lines[1:]:
            line = line.lower().replace(",", "")
            words = line.split()
            clarin_dict[words[0]] = int(words[1])

        merged_dict = json_obj | clarin_dict # makes DICT type
        # print(len(merged_dict.values())) # to print() number of uniq words
        print("Loading of freq-corpus done! \n")
        return merged_dict
    else:
        return json_obj # DICT type


def get_text(line):
    """Return list version of words in that line."""
    words = re.findall(r'\b[a-zA-ZäöüßÄÖÜſẞ]+\b', line) 
    words_lower = [word.lower() for word in words]
    return words, words_lower


def space_corretion(line):
    """Correct missing space characters."""
    # This regex finds a punctuation mark followed by a non-space character
    space_pattern = r'(?<=[^\s])([.,!?;:])(?=[^\s])'
    
    # Replace the pattern with the punctuation followed by a space
    corrected_line = re.sub(space_pattern, r'\1 ', line)
    
    return corrected_line


def get_json_obj_DEP(mylist):
    """DEPRECATED: Take a list and create a double-sorted JSON object with each word frequency."""
    word_freq = Counter(mylist)
    freq_most = word_freq.most_common()
    freq_sorted = sorted(freq_most, key=lambda x: (-x[1], x[0]))
    freq_dict = dict(freq_sorted)
    return json.dumps(freq_dict)


def get_json_obj(mylist):
    """Take a list and create a double-sorted JSON object with each word frequency."""
    word_freq = Counter(mylist)
    freq_most = word_freq.most_common()
    freq_sorted = sorted(freq_most, key=lambda x: (-x[1], x[0]))
    return dict(freq_sorted)


def dbl_save_freq(freq_path, freq_obj):
    with open(freq_path, 'w', encoding='utf-8') as f:
        json.dump(freq_obj, f, ensure_ascii=False, indent=4)

    freq_path_alpha = freq_path[:-5] + '-alphabetic.json'
    with open(freq_path_alpha, 'w', encoding='utf-8') as f:
            json.dump(freq_obj, f, sort_keys=True, ensure_ascii=False, indent=4)


def save_freq(meta_path, path_ending, word_list):
    path_out = os.path.join(meta_path, path_ending)
    freq_obj = get_json_obj(word_list)
    with open(path_out, 'w', encoding='utf-8') as f:
        json.dump(freq_obj, f, ensure_ascii=False, indent=4)


def get_starting_file(folder):
    filename = "starting_file.txt"
    filepath = os.path.join(folder, filename)
    
    if not os.path.exists(filepath):
        return []
    else:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    return lines[:1]


def save_interrupt_file(folder, filename_store):
    filename = "starting_file.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, 'w') as file:
        file.write(filename_store[0])


def remove_interrupt_file(folder):
    filename = "starting_file.txt"
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"File {filename} has been deleted.")
    else:
        print(f"File {filename} did not exist.")


def spellcheck(data, folder, output, option, redo=False, meta=True, space_corr=True):
    """Main spell checker function. Takes in either a word list or a frequency dictionary.
       Saves the corrected files, as well as several metadata files."""
    # Special case for spell checking the index pages
    if 'index' in folder:
        space_corr = True
    
    # Initialize the spell checker without a predefined language
    spell = SpellChecker(language=None, case_sensitive=False)
    
    if option == "list":
        # Load the custom word list
        spell.word_frequency.load_words(data)
    else:
        # Load the premade word frequency dict
        spell.word_frequency.load_json(data)

    nErrors_by_page = []
    misspelled_all, spck_corrections_used, missed_and_fixed, still_missing= [], [], [], []
    error_map = dict()
    countdown = count_corpus_files([folder])

    filename_store = []
    try:
        for filename in os.listdir(folder):
            errors_in_file = 0
            if filename.endswith('.txt'):
                if not redo and len(get_starting_file(output)) > 0:
                    filename_starting = get_starting_file(output)
                    if filename == filename_starting[0]:
                        print("Continuing where we left off!")
                        filename_starting = []
                    else:
                        countdown -= 1
                        continue
                elif redo:
                    remove_interrupt_file(output)
                    redo = False

                filename_store.insert(0, filename)
                
                path_in = os.path.join(folder, filename)
                with open(path_in, 'r') as file:
                    lines = file.readlines()
                
                for i in range(len(lines)):
                    line = lines[i]
                    words_normal, words_lower = get_text(line)
                    
                    unknowns = spell.unknown(words_lower)
                    errors_in_file += len(unknowns)

                    for word in unknowns:
                        if enchant_word(word[:-1]):
                            errors_in_file -= 1
                            continue
                        else: # removed CLARIN branch here, already part of freq_list loaded into SpellChecker
                            misspelled_all.append(word)
                            if word not in error_map:
                                error_map[word] = [filename, f'line {i}', 1]
                            else:
                                upd_count = error_map[word][2] + 1
                                error_map[word] = [filename, f'line {i}', upd_count]
                            
                            og_word = words_normal[words_lower.index(word)]
                            correction = str(spell.correction(word))
                            if correction == "None": # edit the line to note that word is misspelled but un-id.fiable
                                marked_word = "**" + og_word + "**"
                                lines[i] = lines[i].replace(og_word, marked_word)
                                still_missing.append(word)
                                continue

                            # missed_and_fixed.add(word) # if using a set()
                            missed_and_fixed.append(word)
                            spck_corrections_used.append(correction)

                            # continue
                            if og_word[0].isupper():
                                correction_new = correction[0].upper() + correction[1:]
                                lines[i] = lines[i].replace(og_word, correction_new)
                                # print(f"Misspelled: {og_word}, Correction: {correction_new}")
                            else:
                                # print(f"Misspelled: {og_word}, Correction: {correction}")
                                lines[i] = lines[i].replace(og_word, correction)

                # Create the target folder if it doesn't exist
                os.makedirs(output, exist_ok=True)

                path_out = os.path.join(output, filename)
                with open(path_out, 'w') as file:
                    for line in lines:
                        if space_corr:
                            corr_line = space_corretion(line)
                            file.write(corr_line)
                        else:
                            file.write(line)
            
                countdown -= 1
                print(f"Processed {filename}, with {errors_in_file} errors, {countdown} files left")
                nErrors_by_page.append("Processed {}, with {} errors".format(filename, errors_in_file))
                # break 

        remove_interrupt_file(output)

    except KeyboardInterrupt:
        # Handle the manual interruption (Ctrl-C)
        print("\nProcess interrupted by user.\n")
        save_interrupt_file(output, filename_store)
        print("Saved filename of interrupted file.")
        
    except Exception as e:
        # Handle any exceptions that may occur during the loop
        print(f"An error occurred: {e}")
        save_interrupt_file(output, filename_store)
        print("Saved filename of interrupted file.")

    finally:
        if meta:
            # Create the metadata folder if it doesn't exist
            meta_folder = 'metadata'
            meta_path = os.path.join(output, meta_folder)
            os.makedirs(meta_path, exist_ok=True)

            # Create metadata: count of errors per file
            ending = "file-error-counts.txt"
            path_out = os.path.join(meta_path, ending)
            with open(path_out, 'w') as file:
                for line in sorted(nErrors_by_page):
                    file.write(line + '\n')

            # Create metadata: count of freq per error (using spck items only for <<cleanliness>>)
            save_freq(meta_path, "file-error-freq.json", missed_and_fixed)

            # Create metadata: count of freq per correction (using spck items only for <<cleanliness>>)
            save_freq(meta_path, "file-error-spckcorrs-freq.json", spck_corrections_used)

            # Create metadata: SET of words misspelled against all of spck/CLARIN/Enchant
            ending = "file-error-allmisspelled.txt"
            path_out = os.path.join(meta_path, ending)
            with open(path_out, 'w') as file:
                for word in sorted(set(misspelled_all)):
                    file.write(word + '\n')

            # Create metadata: count of freq per error for words misspelled against all of spck/CLARIN/Enchant
            save_freq(meta_path, "file-error-allmisspelled-freq.json", misspelled_all)

            # Create metadata: SET of words misspelled and WITHOUT a spck correction
            ending = "file-error-unknowns.txt"
            path_out = os.path.join(meta_path, ending)
            with open(path_out, 'w') as file:
                for word in sorted(set(still_missing)):
                    file.write(word + '\n')

            # Create metadata: count of freq per error without a correction 
            save_freq(meta_path, "file-error-unknowns.json", still_missing)

            # Create metadata: LIST of words misspelled and file location
            ending = "file-error-map.txt"
            path_out = os.path.join(meta_path, ending)
            with open(path_out, 'w') as file:
                for key, value in sorted(error_map.items()):
                    file.write(f'{key} : {value}' + '\n')


def main():
    # Load and preprocess all text files
    directories = ['/Users/USER/Documents/CESTA-Summer/corpus-files/dta_kernkorpus_plain_1600-1699', 
                   '/Users/USER/Documents/CESTA-Summer/corpus-files/dta_kernkorpus_plain_1700-1799']
    
    corpus_path = '/Users/USER/Documents/CESTA-Summer/corpus-files/new-dta_kernkorpurs_plain/custom_words.txt'
    corpus_path_r = '/Users/USER/Documents/CESTA-Summer/corpus-files/new-dta_kernkorpurs_plain/manchck/custom_words-remaining.txt'
    freq_path = '/Users/USER/Documents/CESTA-Summer/corpus-files/new-dta_kernkorpurs_plain/custom_words-freq.json'

    choice = input("Continue with script (vs feeding custom paths)? (y/n): ")

    if choice == "y":
        txt_folder = '/Users/USER/Documents/CESTA-Summer/output-txt/from-transkribus/index/pp1-merged'
        txt_folder_save = '/Users/USER/Documents/CESTA-Summer/output-txt/from-transkribus/index/pp2-merged-pyspck'
    elif choice == "n":
        txt_folder = input("Enter path for folder of txt files: ")
        txt_folder_save = input("Enter path to folder for saving: ")

    select = 3
    corpus_path = corpus_path_r # optional, use manually-updated corpus list rather than code-produced one  
    if select == 1:
        # Load the corpus/freq, NO CLARIN DATA
        word_list = load_corpus(corpus_path)
        word_freq = load_freq(freq_path)
    elif select == 2:
        # Load the corpus/freq, YES CLARIN DATA
        word_list = load_corpus(corpus_path)
        word_freq = load_freq(freq_path, load_clarin=True)
    elif select == 3:
        # Load corpus + Update freq, CHECK CLARIN DATA
        word_list = load_corpus(corpus_path)
        word_freq = load_freq(freq_path, load_clarin=True, upd_corpus=word_list, save_update=False)
    elif select == 4:
        # Create + Load corpus ONLY
        load_and_preprocess_files(directories, corpus_path, freq_path, save_freq=False)
        word_list = load_corpus(corpus_path)
    elif select == 5:
        # Create + Load corpus/freq, CHECK CLARIN DATA
        load_and_preprocess_files(directories, corpus_path, freq_path, save_freq=True)
        word_list = load_corpus(corpus_path)
        word_freq = load_freq(freq_path, load_clarin=True)

    select2 = 2
    # print(f"Running spell checking with option {select2}!" + "\n")
    if select2 == 1:
        spellcheck(word_list, txt_folder, txt_folder_save, option="list")
    elif select2 == 2:
        spellcheck(word_freq, txt_folder, txt_folder_save, option="freq", redo=True, space_corr=True)
    elif select2 == 3:
        spellcheck(word_freq, txt_folder, txt_folder_save, option="freq", redo=False)
    elif select2 == 4:
        spellcheck(word_freq, txt_folder, txt_folder_save, option="freq", redo=True, meta=False)
    elif select2 == 5:
        spellcheck(word_freq, txt_folder, txt_folder_save, option="freq", redo=False, meta=False)


if __name__ == "__main__":
    main()