import os
import re
import shutil

def duplicate_jpegs(page_list, source_folder, target_folder):
    # Create the target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    copies = 0
    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith('.jpg'):
            tmp = re.findall(r'\d+', file_name)
            n = list(map(int, tmp)) 
            file_n = n[0] + 1
            
            # if file_n not in page_list:
            if file_n in page_list:
                source_path = os.path.join(source_folder, file_name)
                target_path = os.path.join(target_folder, file_name)
                shutil.copy2(source_path, target_path)
                print(f"Copied '{file_name}'")
                copies +=1 

    print(str(copies) + " copies made.")

def main():
    source_folder = '/Users/USER/Documents/CESTA-Summer/all-pages-as-jpeg'  # Replace with the path to your source folder
    target_folder = '/Users/USER/Documents/CESTA-Summer/all-pages-as-jpeg/images-only'  # Replace with the path to your target folder
    
    # Indices of the pages to extract (1-based)
    pg_begin = [i for i in range(9, 23)]
    pg_toc = [23, 24, 25, 26, 27]
    pg_starts = [29, 31, 32, 36, 46, 55, 56, 68, 86, 105, 121, 136, 151, 165, 212, 231, 256, 270, 281, 304, 317, 330, 341, 347, 364, 391, 409, 420, 444, 450, 482, 488, 500, 509, 516, 528, 543, 554, 562, 579, 586, 606, 621, 629, 634, 644, 653, 666, 683, 727, 728, 729, 735, 744, 760, 798, 807, 817, 830, 840, 849, 855, 863, 873, 881, 887, 904]
    pg_index = [i for i in range(905, 985)]
    pg_img = [8, 17, 76, 140, 170, 177, 192, 201, 210, 218, 236, 240, 456, 473, 491, 519, 523, 529, 557, 569, 576, 590, 600, 626, 647, 718]
    pg_img_new = pg_img + [1, 2, 5]
    pg_tables = [404, 405, 406, 407, 408]
    pg_other = [706, 874]
    pg_dict = [985, 986]
    pg_skip = [58]
    pg_blank1 = [i for i in range(1, 8)]
    pg_blank2 = [10, 18, 28, 77, 141, 171, 176, 193, 200, 211, 219, 237, 241, 474, 492, 520, 524, 530, 558, 570, 575, 589, 599, 625, 648, 719, 987, 988, 989, 990, 991, 992]
    pg_total = pg_skip + pg_begin + pg_index + pg_blank1 + pg_blank2 + pg_dict + pg_img + pg_other + pg_starts + pg_toc + pg_tables

    # Run the move_jpeg function
    duplicate_jpegs(sorted(list(set(pg_img_new))), source_folder, target_folder)

if __name__ == "__main__":
    main()
