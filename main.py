import chunker
import openai_embeddings_doc_parser
import argparse
import os
#import embeddings



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
            num_tokens, status, sample_tokens = openai_embeddings_doc_parser.process_pdf(pdf_file)
            print(f"{pdf_file}: {status} with {num_tokens} tokens. Sample tokens: {sample_tokens}")
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

if __name__ == "__main__":
    main()