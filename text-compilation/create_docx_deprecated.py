from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import qn
from docx.shared import Pt

def extract_first_50_pages(input_file, output_file):
    # Load the original document
    doc = Document(input_file)
    
    # Create a new document
    new_doc = Document()

    # Track the page count
    page_count = 0
    paragraph_count = 0
    for element in doc.element.body:
        # Copy paragraph elements directly
        if element.tag == qn('w:p'):
            # Calculate page breaks
            page_breaks = element.xpath('.//w:br[@w:type="page"]')

            # Add paragraph to the new document
            new_doc.element.body.append(element)

            # Increment page count if the paragraph contains page breaks
            paragraph_count += 1
            page_count += len(page_breaks)

            # Stop after 100 pages
            if page_count >= 40:
                break

        # Copy table elements directly
        elif element.tag == qn('w:tbl'):
            new_doc.element.body.append(element)

    # Save the new document
    new_doc.save(output_file)

# Usage
input_file = '/Users/samxp/Library/Mobile Documents/com~apple~Pages/Documents/compiled-doc-noimages.docx'
output_file = '/Users/samxp/Library/Mobile Documents/com~apple~Pages/Documents/first_50_pages.docx'
extract_first_50_pages(input_file, output_file)
