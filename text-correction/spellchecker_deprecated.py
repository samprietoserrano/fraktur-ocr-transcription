import os
import re
import json
from collections import Counter
from spellchecker import SpellChecker

def preprocess_text(text):
    # text = re.sub(r'[^a-zA-ZäöüÄÖÜß ]', ' ', text)
    german_letter_pattern = r'^[a-zA-ZäöüÄÖÜß]+$'

    words = text.split()
    filtered_words = [word.lower() for word in words if re.match(german_letter_pattern, word)]
    return ' '.join(filtered_words)


def load_and_preprocess_files(directories, dict_path, freq_path, save_freq):
    word_list = []
    
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    processed_text = preprocess_text(text)
                    words = processed_text.split()
                    word_list.extend(words)

    with open(dict_path, 'w', encoding='utf-8') as f:
        for word in sorted(word_list):
            f.write(f"{word}\n")

    if save_freq:
        word_freq = Counter(word_list)
        json_obj = json.dumps(word_freq, sort_keys=True)
        with open(freq_path, 'w', encoding='utf-8') as f:
            f.write(json_obj)


def load_corpus(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.readlines()
    corpus = [word[:-1] for word in text]
    return corpus


def load_freq(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        json_obj = json.load(file)
    
    return json_obj


def get_text(line):
    # words = re.findall(r'\b[a-zA-ZáäöüßÄÖÜſẞ]+\b', line) 
    words = re.findall(r'\b[a-zA-ZäöüßÄÖÜſẞ]+\b', line) 
    words_lower = [word.lower() for word in words]
    return words, words_lower


def spellcheck(data, folder, output, option):
    # Initialize the spell checker without a predefined language
    spell = SpellChecker(language=None, case_sensitive=False)
    
    if option == "list":
        # Load the custom word list
        spell.word_frequency.load_words(data)
    else:
        # Load the premade word frequency dict
        spell.word_frequency.load_json(data)

    error_list = []
    used_cor = []
    missed_og= set()
    for filename in os.listdir(folder):
        errors = 0
        if filename.endswith('.txt'):
            path_in = os.path.join(folder, filename)
            with open(path_in, 'r') as file:
                lines = file.readlines()

            for line in lines:
                text, text_lower = get_text(line)
                
                misspelled = spell.unknown(text_lower)
                errors += len(misspelled)

                for word in misspelled:
                    missed_og.add(word)
        
                    correction = str(spell.correction(word))
                    if correction == "None":
                        continue
                    used_cor.append(correction)
                    og_word = text[text_lower.index(word)]
                    if og_word[0].isupper():
                        correction_new = correction[0].upper() + correction[1:]
                        text[text_lower.index(word)] = correction_new
                    else:
                        text[text_lower.index(word)] = correction

                    # print(f"Misspelled: {og_word}, Correction: {correction}")

            # Create the target folder if it doesn't exist
            os.makedirs(output, exist_ok=True)

            path_out = os.path.join(output, filename)
            with open(path_out, 'w') as file:
                for line in lines:
                    file.write(line)

        
        print(f"Processed {filename}, with {errors} errors")
        error_list.append("Processed {}, with {} errors".format(filename, errors))
        # break 

    # Create the metadata folder if it doesn't exist
    meta_folder = 'metadata'
    meta_path = os.path.join(output, meta_folder)
    os.makedirs(meta_path, exist_ok=True)

    # Create metadata: count of errors per file
    ending = "file-error-counts.txt"
    path_out = os.path.join(meta_path, ending)
    with open(path_out, 'w') as file:
        for line in sorted(error_list):
            file.write(line + '\n')

    # Create metadata: count of freq per error
    ending = "file-error-freq.json"
    path_out = os.path.join(meta_path, ending)
    word_freq = Counter(used_cor)
    freq_sorted = word_freq.most_common() # this outputs a list! not a dict!
    json_obj = json.dumps(freq_sorted)
    with open(path_out, 'w', encoding='utf-8') as f:
        f.write(json_obj)

    # Create metadata: list of original words "misspelled" (a set)
    ending = "file-error-originals.txt"
    path_out = os.path.join(meta_path, ending)
    with open(path_out, 'w') as file:
        for word in sorted(missed_og):
            file.write(word + '\n')


def main():
    # Load and preprocess all text files
    directories = ['/Users/samxp/Documents/CESTA-Summer/corpus-files/dta_kernkorpus_plain_1600-1699', 
                   '/Users/samxp/Documents/CESTA-Summer/corpus-files/dta_kernkorpus_plain_1700-1799']
    
    corpus_save = '/Users/samxp/Documents/CESTA-Summer/corpus-files/new-dta_kernkorpurs_plain/custom_words.txt'
    freq_save = '/Users/samxp/Documents/CESTA-Summer/corpus-files/new-dta_kernkorpurs_plain/custom_words-freq.json'

    txt_folder = '/Users/samxp/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp4-unhyphen-2'
    txt_folder_save = '/Users/samxp/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp5-pyspck'

    select = 2
    if select == 1:
        # Load the corpus previously created
        word_list = load_corpus(corpus_save)
    elif select == 2:
        # Load the freq previously created
        word_freq = load_freq(freq_save)
    elif select == 3:
        # Load the corpus AND freq previously created
        word_list = load_corpus(corpus_save)
        word_freq = load_freq(freq_save)
    elif select == 4:
        # or create a corpus and then load afters
        load_and_preprocess_files(directories, corpus_save, freq_save, save_freq=False)
        word_list = load_corpus(corpus_save)
    elif select == 5:
        # or create a corpus AND freq and then load afters
        load_and_preprocess_files(directories, corpus_save, freq_save, save_freq=True)
        word_list = load_corpus(corpus_save)
        word_freq = load_freq(freq_save)

    select2 = 2
    if select2 == 1:
        spellcheck(word_list, txt_folder, txt_folder_save, option="list")
    elif select2 == 2:
        spellcheck(word_freq, txt_folder, txt_folder_save, option="freq")


if __name__ == "__main__":
    main()