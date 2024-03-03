import os
import fitz  # PyMuPDF
import openai
from prettytable import PrettyTable
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def split_text_for_embeddings(text, chunk_size=4000, overlap=200):
    """
    Splits text into chunks, each with a maximum length of `chunk_size` characters,
    and ensures an overlap of approximately `overlap` tokens between consecutive chunks.
    """
    rough_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap * 10)]  # 10 is an approx. avg. character count per token

    chunks = []
    for rough_chunk in rough_chunks[:-1]:  # Process all but the last chunk for overlap
        boundary_index = rough_chunk.rfind(' ', 0, chunk_size)
        if boundary_index == -1:  # Fallback in case no space is found
            boundary_index = len(rough_chunk)
        chunks.append(rough_chunk[:boundary_index])

        # Prepare the next chunk starting with the overlap from the current chunk
        next_start = max(0, boundary_index - overlap * 10)
        if next_start < len(rough_chunk):
            rough_chunks[rough_chunks.index(rough_chunk) + 1] = rough_chunk[next_start:] + rough_chunks[rough_chunks.index(rough_chunk) + 1]

    # Add the last chunk without looking for a boundary since it doesn't need to overlap with a subsequent chunk
    chunks.append(rough_chunks[-1])

    return chunks

def get_embeddings_for_text(text, chunk_size=4096, overlap=200):
    """
    Splits the text into chunks with overlap and gets embeddings for each chunk.
    Returns a list of embeddings.
    """
    chunks = split_text_for_embeddings(text, chunk_size, overlap)
    embeddings = []
    
    for chunk in chunks:
        response = openai.Embedding.create(
            input=chunk,
            engine="text-similarity-babbage-001",
        )
        embeddings.append(response['data'][0]['embedding'])
    return embeddings

def process_pdf_and_get_embeddings(pdf_path):
    print(f"Processing {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    embeddings = get_embeddings_for_text(text)
    print(f"Retrieved embeddings for {len(embeddings)} chunks of text from {pdf_path}.")
    return embeddings

# Main execution
if __name__ == "__main__":
    # Prepare a table to display the results
    table = PrettyTable()
    table.field_names = ["PDF File", "Number of Chunks"]

    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        embeddings = process_pdf_and_get_embeddings(pdf_file)
        table.add_row([pdf_file, len(embeddings)])

    # Display the table
    print(table)
