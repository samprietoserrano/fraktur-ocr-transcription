import glob 
import os
import PyPDF2
import readline
from itertools import chain

def extract_pages(input_pdf, output_pdf, page_indices, make_list):
    # Make the list if only inputted a range
    if make_list:
        full_indices = []
        for i in range(page_indices[0], page_indices[1]+1):
            full_indices.append(i)
        page_indices = full_indices

    # Open the input PDF file
    with open(input_pdf, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)
        
        # Create a PDF writer object
        writer = PyPDF2.PdfWriter()

        for index in page_indices:
            ix = index - 1
            page = reader.pages[ix]
            writer.add_page(page)

        # Write the output PDF to the specified file
        with open(output_pdf, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

        print(f"Output PDF created: {output_pdf}")
        print("------------------------")


def exclude_pages(input_pdf, output_pdf, page_indices, make_list):
    # Make the list if only inputted a range
    if make_list:
        full_indices = []
        for i in range(page_indices[0], page_indices[1]+1):
            full_indices.append(i)
        page_indices = full_indices

    # Open the input PDF file
    with open(input_pdf, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)
        
        # Create a PDF writer object
        writer = PyPDF2.PdfWriter()

        # Make the list of all page numbers
        all_page = [i for i in range(len(reader.pages))]

        # Loop over the page indices and add the corresponding pages to the writer
        for index in all_page:
            ix = index + 1
            if ix in page_indices:
                continue
            page = reader.pages[index]
            writer.add_page(page)

        # Write the output PDF to the specified file
        with open(output_pdf, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

        print(f"Output PDF created: {output_pdf}")
        print("------------------------")


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


# Indices of the pages to extract (1-based)
group_lists = {
    "pg_begin": [i for i in range(9, 23)],
    "pg_toc": [23, 24, 25, 26, 27],
    "pg_starts": [29, 31, 32, 36, 46, 55, 56, 68, 86, 105, 121, 136, 151, 165, 212, 231, 256, 270, 281, 304, 317, 330, 341, 347, 364, 391, 409, 420, 444, 450, 482, 488, 500, 509, 516, 528, 543, 554, 562, 579, 586, 606, 621, 629, 634, 644, 653, 666, 683, 727, 728, 729, 735, 744, 760, 798, 807, 817, 830, 840, 849, 855, 863, 873, 881, 887, 904],
    "pg_tables": [404, 405, 406, 407, 408],
    "pg_index": [i for i in range(905, 985)],
    "pg_other": [706, 874],
    "pg_dict": [985, 986],
    "pg_skip": [58],
    "pg_img": [8, 76, 140, 170, 177, 192, 201, 210, 218, 236, 240, 456, 473, 491, 519, 523, 529, 557, 569, 576, 590, 600, 626, 647, 718],
    "pg_img-new": [1, 2, 5, 8, 76, 140, 170, 177, 192, 201, 210, 218, 236, 240, 456, 473, 491, 519, 523, 529, 557, 569, 576, 590, 600, 626, 647, 718],
    "pg_blank1": [i for i in range(1, 8)],
    "pg_blank2": [10, 18, 28, 77, 141, 171, 176, 193, 200, 211, 219, 237, 241, 474, 492, 520, 524, 530, 558, 570, 575, 589, 599, 625, 648, 719, 987, 988, 989, 990, 991, 992]
}

def print_options():
    option_dict = dict()

    option = 1
    for group in group_lists:
        print("\t" + f"for {group}, enter {option} ")
        option_dict[option] = group
        option += 1

    print("\t" + f"to enter a custom list, hit return" + "\n")
    return option_dict
    

def main():
    print("------------------------")
    print("Initializing program...")
    input_pdf = '/Users/USER/Documents/CESTA-Summer/source-internetarchive/bub_gb_MbxYAAAAcAAJ.pdf'  # Path to the input PDF file

    options = print_options()
    search = input("Enter option from above: ")

    indices = []
    if not search:
        custom = input("Enter list with comma separators (e.g., 45, 50, etc): ")
        indices += [int(i) for i in custom.split(',')]
    else:
        choice = options[int(search)]
        indices += group_lists[choice]
    
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    output_path = input("Enter the full saving path using tab autocomplete \n (e.g., /Users/USER/.../myfile.pdf): ")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if 'main' not in search:
        extract_pages(input_pdf, output_path, indices, make_list=False)
    else:
        running_list = list(chain.from_iterable(group_lists.values()))
        exclude_pages(input_pdf, output_path, sorted(list(set(running_list))), make_list=False)

if __name__ == "__main__":
    main()