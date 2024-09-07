import PyPDF2

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
    "pg_img": [1, 2, 5, 8, 76, 140, 170, 177, 192, 201, 210, 218, 236, 240, 456, 473, 491, 519, 523, 529, 557, 569, 576, 590, 600, 626, 647, 718],
    "pg_blank1": [i for i in range(1, 8)],
    "pg_blank2": [10, 18, 28, 77, 141, 171, 176, 193, 200, 211, 219, 237, 241, 474, 492, 520, 524, 530, 558, 570, 575, 589, 599, 625, 648, 719, 987, 988, 989, 990, 991, 992]
}

# Paths for each page group map
group_paths = {
    "pg_begin": '/Users/samxp/Documents/CESTA-Summer/mappings/beg-text-map.txt',
    "pg_toc": '/Users/samxp/Documents/CESTA-Summer/mappings/toc-text-map.txt',
    "pg_starts": '/Users/samxp/Documents/CESTA-Summer/mappings/nonsimple-text-map.txt',
    "pg_main": '/Users/samxp/Documents/CESTA-Summer/mappings/main-text-map.txt',
    "pg_index": '/Users/samxp/Documents/CESTA-Summer/mappings/index-text-map.txt',
    "pg_tables": '/Users/samxp/Documents/CESTA-Summer/mappings/tables-text-map.txt',
    "pg_other": '/Users/samxp/Documents/CESTA-Summer/mappings/other-text-map.txt',
    "pg_dict": '/Users/samxp/Documents/CESTA-Summer/mappings/dict-text-map.txt',
    "pg_skip": '',
    "pg_img": '',
    "pg_blank1": '',
    "pg_blank2": ''
}

def map_main_only(page_list):
    """This function maps the main-group with the following assumptions:
        1) main-group was processed from the JPEG version, thus their names are not re-listed.
        2) main-group txt files simply need to be re-indexed by one since JPEGs are zero-indexed."""
    
    og_pdf = '/Users/samxp/Documents/CESTA-Summer/source-internetarchive/bub_gb_MbxYAAAAcAAJ.pdf'

    with open(og_pdf, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)

        # Make the list of all page numbers
        all_pages = [i for i in range(len(reader.pages))]

        # Loop over the page indices and add the corresponding pages to the writer
        count = 0
        lines = []
        for index in all_pages:
            page = index + 1
            if page in page_list:
                continue
            lines.append("real page: {} and file: {}".format(page, index))
            count += 1

        return lines, count

def map_pages(page_list, output_path):
    """This function maps the groups processed with Transkribus sine they got re-listed, thus need to be map."""
    
    map_list = []
    count = 0

    # Get the list of mapping entries
    if 'main' in output_path:
        map_list, count = map_main_only(page_list)
    else:
        for ix, page_ix in enumerate(page_list, start=1):
            map_list.append("real page: {} and file: {}".format(page_ix, ix))
            count = ix

    # Write the output to the specified file
    with open(output_path, 'w') as output_file:
        for line in map_list:
            output_file.write(line + '\n')

    print(f"Output file created: {output_path}")
    print(f"{count} pages mapped.")


def main():
    running_list = []
    # Save the map for all non-main groups
    for group in group_lists:
        map_path = group_paths[group]
        pg_list = group_lists[group]
        running_list += pg_list
        if not map_path:
            continue
        map_pages(sorted(list(set(pg_list))), map_path)

    # Finally, save the map for main-group
    map_pages(sorted(list(set(running_list))), group_paths["pg_main"])

if __name__ == "__main__":
    main()