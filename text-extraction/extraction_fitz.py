# import io
import re
import os
import fitz  # PyMuPDF library
import textwrap

# Function to detect paragraphs
def end_of_paragraph(block_rect, margin_1x=90, margin_2x=150):
    if block_rect[2] < margin_1x - 5:
        return True
    if block_rect[2] > margin_1x + 5 and block_rect[2] < margin_2x - 5:
        return True
    return False

# Function to detect headers
def end_of_header(block_rect, line, side, margin_hx=140):
    # if side:
    #     if block_rect[2] > margin_hx and (line[-3].isdigit() or line[0].isdigit()):
    #         return True
    #     return False
    # if block_rect[3] < 20:
    #     return True
    # return False
    if block_rect[3] < 20:
        return True
    return False

# Function to make all one line
def replace_newlines_with_space(text):
    return text.replace('\n', ' ')[:-1] + '\n'

# Iterate over text blocks and detect paragraphs
def interate_blocks(blocks, side):
    paragraphs = []
    current_paragraph = ""
    header_done = False
    for block in blocks:
        if (block[6]):
            continue

        line = block[4]
        nline = ""
        if line.count('\n') > 1:
            nline += replace_newlines_with_space(line)
        else:
            nline += block[4]
        
        block_rect = fitz.Rect(block[:4])  # Get the bounding box of the block
        # print(block_rect)
        # print(line)
        # break
        # if "hätte" in nline.lower():
        #     print(block[2])
        if not header_done:
            if end_of_header(block_rect, nline, side):
                current_paragraph += nline
                paragraphs.append(current_paragraph)
                current_paragraph = ""
                header_done = True
                continue
        if end_of_paragraph(block_rect):
            current_paragraph += nline
            paragraphs.append(current_paragraph)
            current_paragraph = ""
        else:
            current_paragraph += nline

    # Add the last paragraph
    if current_paragraph:
        paragraphs.append(current_paragraph)
    # for p in paragraphs:
    #     print(p)
    return paragraphs

# Write the paragraphs to file
def output_blocks(paragraphs, output_file):
    # Consolidate paragraphs
    for i, paragraph in enumerate(paragraphs):
        if i == 0:
            continue
        if paragraph[0].isalpha() or paragraph[0] == "®":
            continue
        else:
            if i != 1:
                paragraphs[i-1] = paragraphs[i-1] + " " + paragraph
                paragraphs.pop(i)

    # Write each paragraph to the output file
    for i, paragraph in enumerate(paragraphs, start=1):
        if i == 1:
            output_file.write(f"Header:\n")
        else:
            output_file.write(f"Paragraph {i-1}:\n")
        text = " ".join(paragraph.replace("\n", " ").split())
        text = textwrap.fill(text, width=80)
        paragraph = re.sub(r' ,', ',', text)

        output_file.write(paragraph + "\n\n")

# Write the paragraphs to file (print)
def output_blocks_p(paragraphs):
    # Consolidate paragraphs
    for i, paragraph in enumerate(paragraphs):
        if i == 0:
            # print(paragraph)
            continue
        if not paragraph[0].isupper():
            if i != 1:
                paragraphs[i-1] = paragraphs[i-1] + " " + paragraph
                paragraphs.pop(i)

    # Write each paragraph to the output file
    for i, paragraph in enumerate(paragraphs, start=1):
        if i == 1:
            print(f"Header:") 
        else:
            print(f"Paragraph {i-1}:")
        text = " ".join(paragraph.replace("\n", " ").split())
        text = textwrap.fill(text, width=80)
        paragraph = re.sub(r' ,', ',', text)
        print(paragraph)
        print()

# Function to detect margins
def end_of_margin(prev_rect, block_rect, margin_sz):
    if block_rect[3] > prev_rect[3] + 1.5*margin_sz:
        return True
    return False

# Iterate over text blocks and detect margins
def interate_margins(blocks):
    margins = []
    current_margin = ""
    prev_rect = fitz.Rect()
    for block in blocks:
        if (block[6]):
            continue

        line = block[4]
        nline = ""
        if line.count('\n') > 1:
            nline += replace_newlines_with_space(line)
        else:
            nline += block[4]
        
        block_rect = fitz.Rect(block[:4])  # Get the bounding box of the block
        if prev_rect.is_empty:
            prev_rect = block_rect
            current_margin += nline
            continue
        if end_of_margin(prev_rect, block_rect, margin):
            margins.append(current_margin)
            current_margin = nline
            prev_rect = block_rect
        else:
            current_margin += nline
            # prev_rect = block_rect

    # Add the last margin
    if current_margin:
        margins.append(current_margin)
    return margins

# Write the margins to file
def output_margins(margins, output_file, start):
    # Write each margin to the output file
    num = 0
    for i, margin in enumerate(margins, start=start):
        output_file.write(f"Margin {i}:\n")
        text = " ".join(margin.replace("\n", " ").split())
        text = textwrap.fill(text, width=80)
        margin = re.sub(r' ,', ',', text)

        output_file.write(margin + "\n\n")
        num += 1
    return num

# Write the margins to file (print)
def output_margins_p(margins):
    # Print each margin
    for i, margin in enumerate(margins, start=1):
        print(f"Margin {i}:")
        text = " ".join(margin.replace("\n", " ").split())
        text = textwrap.fill(text, width=80)
        margin = re.sub(r' ,', ',', text)

        print(margin)
        print()

# Open the PDF file
# pdf_file = fitz.open("/Users/samxp/Documents/CESTA-Summer/output-txt/script-with-new-pdf/sample-main-pages.pdf")
pdf_file = fitz.open("/Users/samxp/Documents/CESTA-Summer/pdf_by_types/only-script-eligible.pdf")
# page = pdf_file[905]

# Get the text flags for the clip box
flags = fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_PRESERVE_LIGATURES 

# Create the output directory if it doesn't exist
output_dir = "/Users/samxp/Documents/CESTA-Summer/output-txt/script-with-new-pdf/"
os.makedirs(output_dir, exist_ok=True)

# Extract text from all pages
for page_index in range(len(pdf_file)):
# for page_index in range(0, 3):
    page = pdf_file[page_index]
    # text = page.get_text("text", flags=flags)

    # print(page.rect)
    # break
    # Define the clip box, which is 21.16 points away from the left and right sides
    # Making clips for the main text, the left margin, and the right margin of page
    margin = 21.16
    clip_left_margin = fitz.Rect(0-margin, 0, 1.25 * margin, page.rect.height)
    clip_right_margin = fitz.Rect(page.rect.width - 1.25*margin, 0, page.rect.width, page.rect.height)
    clip_main = fitz.Rect(1.5 * margin, 0, page.rect.width - 1.3*margin, page.rect.height)


    # Run on the main page
    blocks = page.get_text("blocks", clip=clip_main, flags=flags)
    for b in blocks:
        print(b)
        break
    paragraphs = []
    # if page_index % 2 == 0:
    #     paragraphs = interate_blocks(blocks, 0)
    # else: 
    #     paragraphs = interate_blocks(blocks, 1)
    paragraphs = interate_blocks(blocks, 1) 
    
    # Run on the margins
    m1 = page.get_text("blocks", clip=clip_left_margin, flags=flags)
    m2 = page.get_text("blocks", clip=clip_right_margin, flags=flags)
    margins_l = interate_margins(m1)
    margins_r = interate_margins(m2)

    # Open the output file for writing
    output_file_path = os.path.join(output_dir, f'text_{page_index}.txt')
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_blocks(paragraphs, output_file)
        # output_blocks_p(paragraphs)
        num = output_margins(margins_l, output_file, 1)
        output_margins(margins_r, output_file, num+1)

# Close the PDF file
pdf_file.close()