# llm-play


### filler text

Steps

1. take a local pdf, and tokenize it using openai embeddings.
2. construct prompt to run queries on pdf
3. ???
4. profit.

Query Embedding: Convert your query into an embedding.
Semantic Search: Compare the query embedding against embeddings of document sections to find the closest matches, indicating the most relevant sections.
Extract Text: Extract the text of the top matching sections from the original document.
Generate Prompt: Use the extracted text as context in a prompt to the Chat Completions API, asking for the information you need or for a summary, etc.
Receive Response: The Chat Completions API generates a response based on the context provided, effectively using the content of the most relevant sections identified via embeddings.
Evaluation:


Flow:

1. check if PDF is OCR, and read text accordingly.
2. parse full pdf.
3. create chunks for data with overlap (clarify?)
4. create mapping for sentence, paragraph, and page number (if applicable)



 - Raw PDFs
    - OCR Check
    - "Naturalize" to regular text based PDF
 - Chunking
    - 4000 token limit (OpenAI embeddings API limit)
    - 200 token overlap (for better context, this is variable and arg in spacy)
    - Spacy
        - Sentence tokenization
        - Dynamic chunking based on sentence length (does it help to see the text characteristics first?)
 - Metadata Mapping
    - add paragraph / page / file metadata mapping to each token?? (wont this be a big big table?)
    - how and where to store it?
    - JSONB in Supabase (JSONB is faster although writes are slower)
 - Vector Indexing (later for multiple pdfs)
    - how? where? what?
 - Integration
    - Query from user convert to embedding
    - semantic search compare the query embedding against embeddings of document sections to find the closest matches, indicating the most relevant sections.
        - may need further steps here that includes ranking of results like top k
        - add max. amount of relevant information upto Chat completions API context limit.
        - other things????
    - use metadata to map the origin text and extract and it feed it back into a system prompt + original prompt
    - Receive chat completions response
 - Evaluation
    - How? 


V1
 - ignore indexing for vectors and evals.
 - ignore ranking of semantic search
 - ??