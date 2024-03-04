import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2
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
    
    # Basic check to determine if OCR is needed
    if len(word_tokenize(text)) < 50:  # Assuming less than 50 tokens means little to no text was extracted
        print(f"Attempting OCR for {pdf_path}")
        text = extract_text_tesseract(pdf_path)
    
    tokens = word_tokenize(text)
    return len(tokens), "Tokenized" if tokens else "Error"

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
