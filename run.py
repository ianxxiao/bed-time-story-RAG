#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from OCR import perform_ocr_file
from chunking import fixed_chunk_size, fixed_chunk_overlap
from metadata import generate_metadata_from_chunk
from embedding import embed
import time
from pprint import pprint
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

def main():
    """
    Main function to run RAG pipelien.
    """
    raw_file_path = Path(__file__).parent / "rawData" / "TheBlueFairyBook.pdf"

    #1. Convert the document to markdown
    success, error, combined_markdown, raw_markdown = perform_ocr_file(raw_file_path)

    if success:
        #2. Chunk the markdown into sections
        chunks = fixed_chunk_overlap(raw_markdown)

        #3. Embed the chunks
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(chunks)

        #3. Generate metadata and embeddings for each chunk
        chunks_with_embeddings_metadata = []
        for i, chunk in enumerate(tqdm(chunks[10:15], desc="Generating metadata", unit="chunk")):
            
            time.sleep(5)  # 5 second pause

            chunks_with_embeddings_metadata.append({
                "text": chunk,
                "metadata": generate_metadata_from_chunk(chunk),
                "embedding": embeddings[i]
            })

        pprint(chunks_with_embeddings_metadata[0:2])

if __name__ == "__main__":
    main()