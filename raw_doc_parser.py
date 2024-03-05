import argparse
import os
import sys
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2
import chunker 
# from nltk.tokenize import word_tokenize
# import nltk
# from prettytable import PrettyTable

# Download necessary NLTK datasets
# nltk.download('punkt')

def extract_text_pypdf2(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() if page.extract_text() else ''
    return text

def extract_text_tesseract(pdf_path):
    pages = convert_from_path(pdf_path, 300)
    text = ''
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

def process_pdf(pdf_path):
    print(f"Processing {pdf_path}")
    text = extract_text_pypdf2(pdf_path)

    if not text:
        print(f"Attempting OCR for {pdf_path}")
        text = extract_text_tesseract(pdf_path)

     # Initialize tokens variable by splitting the text
    tokens = text.split()  # Tokenize the initial extracted text

    # Sample tokens for demonstration, adjust the number as needed
    sample_tokens = tokens[:10] if len(tokens) > 10 else tokens
    
    # Basic check to determine if OCR is needed
    # if len(tokens) < 50:  # Assuming less than 50 tokens means little to no text was extracted
    #     print(f"Attempting OCR for {pdf_path}")
    #     text = extract_text_tesseract(pdf_path)
    #     tokens = text.split()  # Re-tokenize after OCR


    tokens = chunker.spacy_chunking_with_overlap(text, max_tokens=4000, overlap=200)
    return len(tokens), "Tokenized" if tokens else "Error", sample_tokens

def main():
    parser = argparse.ArgumentParser(description='Process PDFs to extract text and tokenize.')
    parser.add_argument('pdf_directory', type=str, help='Directory containing PDFs')
    args = parser.parse_args()

    pdf_directory = args.pdf_directory

    # Check if the directory exists
    if not os.path.isdir(pdf_directory):
        print(f"The directory {pdf_directory} does not exist.")
        sys.exit(1)

    # List PDF files in the directory
    pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    
    # Check if there are PDF files in the directory
    if not pdf_files:
        print(f"No PDF files found in the directory {pdf_directory}.")
        sys.exit(1)

    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            num_tokens, status, sample_tokens = process_pdf(pdf_file)
            print(f"{pdf_file}: {status} with {num_tokens} tokens. Sample tokens: {sample_tokens}")
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

if __name__ == "__main__":
    main()

# Prepare a table to display the results
# table = PrettyTable()
# table.field_names = ["PDF File", "Status", "Token Count/Error"]

# pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
# total_tokens = 0

# for pdf_file in pdf_files:
#     num_tokens, status = process_pdf(pdf_file)
#     total_tokens += num_tokens
#     table.add_row([pdf_file, status, num_tokens])

# # Display the table and total token count
# print(table)
# print(f"Total Tokens in all PDFs: {total_tokens}")
