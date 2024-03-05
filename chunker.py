import spacy

# Load the SpaCy language model
nlp = spacy.load("en_core_web_sm")

def spacy_chunking_with_overlap(text, max_tokens=4000, overlap=200):
    # Use SpaCy to tokenize the document into sentences
    doc = nlp(text)
    sentences = list(doc.sents)

    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for sentence in sentences:
        sentence_tokens = len(sentence.text.split())
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

# Example usage
#text = """Your large text document goes here. This could be the content of a legal document, a long article, or any other large text body that you need to chunk into smaller parts for processing with NLP tools or APIs."""

# chunks = spacy_chunking_with_overlap(text, max_tokens=1000, overlap=50)  # Example token limits
# for i, chunk in enumerate(chunks, 1):
#     print(f"Chunk {i}: {chunk[:100]}...")  # Print the first 100 characters of each chunk for demonstration
