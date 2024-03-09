import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry, InstuctorEmbeddingFunction
import argparse
import os
import sys
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2
import chunker 


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

    #print all tokens
    #print(f"All tokens in {pdf_path}: {tokens}")

    # Sample tokens for demonstration, adjust the number as needed
    sample_tokens = tokens[:10] if len(tokens) > 10 else tokens
    
    # Basic check to determine if OCR is needed
    # if len(tokens) < 50:  # Assuming less than 50 tokens means little to no text was extracted
    #     print(f"Attempting OCR for {pdf_path}")
    #     text = extract_text_tesseract(pdf_path)
    #     tokens = text.split()  # Re-tokenize after OCR


    tokens = chunker.spacy_chunking_with_overlap(text, max_tokens=4000, overlap=200)
    return len(tokens), "Tokenized" if tokens else "Error", sample_tokens



instructor = get_registry().get("instructor").create(
                            source_instruction="represent the docuement for retreival",
                            query_instruction="represent the document for retreiving the most similar documents"
                            )

class Schema(LanceModel):
    vector: Vector(instructor.ndims()) = instructor.VectorField()
    text: str = instructor.SourceField()

db = lancedb.connect("~/.lancedb")
tbl = db.create_table("test", schema=Schema, mode="overwrite")

texts = [{"text": "Capitalism has been dominant in the Western world since the end of feudalism, but most feel[who?] that..."},
        {"text": "The disparate impact theory is especially controversial under the Fair Housing Act because the Act..."},
        {"text": "Disparate impact in United States labor law refers to practices in employment, housing, and other areas that.."}]

tbl.add(texts)