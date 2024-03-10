import os
import lancedb
import getpass
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector
from openai_embeddings_doc_parser import process_pdf # Import the function from @openai_embeddings_doc_parser.py

if "OPENAI_API_KEY" not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass.getpass("Enter your OpenAI API key: ")
    
registry = EmbeddingFunctionRegistry().get_instance()
openai = registry.get("openai").create() # uses multi-lingual model by default (768 dim)

class Words(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()
    pdf_file_name: str = None # New field for PDF file name
    pdf_location: str = None # New field for PDF location

# Create the table with the updated schema
table = db.create_table("words", schema=Words)

# Example PDF path
pdf_path = 'path/to/your/pdf.pdf'

# Generate tokens and metadata
tokens, status, sample_tokens = process_pdf(pdf_path)
pdf_file_name = pdf_path.split('/')[-1] # Extract file name from path
pdf_location = pdf_path # Use the full path as location

# Prepare data for insertion
data = [
    {
        "text": token,
        "pdf_file_name": pdf_file_name,
        "pdf_location": pdf_location
    }
    for token in tokens
]

# Insert the data with metadata into the table
table.add(data)