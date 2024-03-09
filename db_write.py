import os
from lance import LanceModel, Vector, EmbeddingFunctionRegistry
from lance.db import LanceDB
from openai_embeddings_doc_parser import process_pdf # Import the function from @openai_embeddings_doc_parser.py

# Assuming lancedb and EmbeddingFunctionRegistry are correctly imported
db = LanceDB.connect("/tmp/db")
registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get("openai").create()

class Words(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()
    pdf_file_name: str = None # New field for PDF file name
    pdf_location: str = None # New field for PDF location

# Create the table with the updated schema
table = db.create_table("words", schema=Words)

def process_directory(directory_path):
    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory_path, pdf_file)
        
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

# Example usage
directory_path = 'path/to/your/pdf/directory'
process_directory(directory_path)