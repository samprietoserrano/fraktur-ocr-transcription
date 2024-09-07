import os

def remove_hyphenation(src, tgt):
    """This version of the function concatenates the entire lines if there is a hyphen in between.
    The newer version only concatenates the necessary word segment after the hyphen. """
    with open(src, 'r') as file:
        lines = file.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i].strip()
        if current_line.endswith('-') and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            # Remove the hyphen and concatenate the lines
            merged_line = current_line[:-1] + next_line
            new_lines.append(merged_line)
            i += 2  # Skip the next line since it's merged
        else:
            new_lines.append(current_line)
            i += 1

    with open(tgt, 'w') as file:
        for line in new_lines:
            file.write(line + '\n')

def process_directory(src, tgt):
    # Create the target folder if it doesn't exist
    os.makedirs(tgt, exist_ok=True)

    for filename in os.listdir(src):
        if filename.endswith('.txt'):
            path_in = os.path.join(src, filename)
            path_out = os.path.join(tgt, filename)
            remove_hyphenation(path_in, path_out)
            print(f"Processed {filename}")

# Example usage:
src = '/Users/samxp/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp2'
tgt = '/Users/samxp/Documents/CESTA-Summer/output-txt/from-script/gcp-script/pp4-unhyphen-old'
process_directory(src, tgt)
