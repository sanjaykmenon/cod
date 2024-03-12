import spacy
import argparse
import os
import sys
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2
import lancedb
import getpass
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector

if "OPENAI_API_KEY" not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass.getpass("Enter your OpenAI API key: ")

registry = EmbeddingFunctionRegistry().get_instance()
openai = registry.get("openai").create() # uses multi-lingual model by default (768 dim)

# Load the SpaCy language model
nlp = spacy.load("en_core_web_sm")

def spacy_chunking_with_overlap(text, max_tokens=4000, overlap=200):
    
    if not isinstance(text, str):
        raise ValueError("Input text must be a string")

    if not isinstance(max_tokens, int) or not isinstance(overlap, int):
        raise ValueError("max_tokens and overlap must be integers")


    try: 
        # Use SpaCy to tokenize the document into sentences
        doc = nlp(text)
        sentences = list(doc.sents)
    except Exception as e:
        print(f"Error tokenizing text: {e}")


    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for sentence in sentences:
        filtered_sentence = [token.text for token in sentence if not token.is_stop]
        sentence_tokens = len(filtered_sentence)
        # If adding this sentence would exceed the max token limit, finalize the current chunk
        if current_tokens + sentence_tokens > max_tokens:
            chunks.append(' '.join(current_chunk))
            # Start the new chunk with the overlap, if there's enough content for it
            current_chunk = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
            current_tokens = sum(len(sent.split()) for sent in current_chunk)
        
        current_chunk.append(sentence.text)
        current_tokens += sentence_tokens
    
    # Add the last chunk if it has content
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


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
    tokens = text.split()  # split via spacing
    token_type = type(tokens)
    # Sample tokens for demonstration, adjust the number as needed
    sample_tokens = tokens[:10] if len(tokens) > 10 else tokens
    
    #tokens = spacy_chunking_with_overlap(text, max_tokens=4000, overlap=200)
    return text, "Tokenized" , token_type # Return tokens, status, and a sample of tokens



db = lancedb.connect("/tmp/db3")
registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get("openai").create()


class Words(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()
    pdf_file_name: str = None # New field for PDF file name
    pdf_location: str = None # New field for PDF location

# Create the table with the updated schema
table = db.create_table("words", schema=Words, mode="overwrite")

def insert_pdf_data(pdf_path):
    try: 
        text, status, token_type = process_pdf(pdf_path)
        print(f"type of text: {token_type}")

        if not isinstance(text, list):
            print(f"Error: Expected tokens to be a list but got {type(text)}")
            return

        pdf_file_name = pdf_path.split('/')[-1]
        pdf_location = pdf_path


        token_chunks = spacy_chunking_with_overlap(text, max_tokens=4000, overlap=200)

        for chunk in token_chunks:
            data = [
                {
                    "text": token,
                    "pdf_file_name":pdf_file_name,
                    "pdf_location": pdf_location
                }
                for token in chunk.split()
            ]

            #inert data with metadata into table
            try:
                table.add(data)
            except Exception as e:
                print(f"Error inserting data for {pdf_path}: {e}")

    except Exception as e:
        print(f"Error in insert_pdf_data for {pdf_path}: {e}")


def main():
    try: 
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
                insert_pdf_data(pdf_file)
                print(f"Successfully processed {pdf_file}")
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
