#!/usr/bin/env python3

from pathlib import Path
from OCR import perform_ocr_file
from chunking import fixed_chunk_size, fixed_chunk_overlap
from metadata import generate_metadata_from_chunk
from embedding import embed
import time
from pprint import pprint
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import firebase_admin
from firebase_admin import credentials, firestore
import json

def main():
    """
    Main function to run RAG pipelien.
    """
    book = "TheGreenFairyBook"
    raw_file_path = Path(__file__).parent / "data" / "rawData" / f"{book}.pdf"    
    cred = credentials.Certificate("bed-time-story-23cd6-firebase-adminsdk-fbsvc-d1d12b089d.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    #1. Convert the document to markdown
    markdown_data_dir = Path(__file__).parent / "data" / "markdownData"
    combined_path = markdown_data_dir / f"{raw_file_path.stem}_combined.md"
    raw_path = markdown_data_dir / f"{raw_file_path.stem}_raw.md"
    
    if not combined_path.exists() or not raw_path.exists():
        success, error, combined_markdown, raw_markdown = perform_ocr_file(raw_file_path)
    else:
        print(f" >>> Using existing markdown files for {raw_file_path.stem}")
        success = True
        combined_markdown = combined_path.read_text()
        raw_markdown = raw_path.read_text()

    if success:
        #2. Chunk the markdown into sections
        chunks = fixed_chunk_overlap(raw_markdown)

        #3. Embed the chunks
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(chunks)

        #3. Generate metadata and embeddings for each chunk
        chunks_with_embeddings_metadata = []
        for i, chunk in enumerate(tqdm(chunks, desc="Generating metadata", unit="chunk")):
            
            time.sleep(4.5)

            chunks_with_embeddings_metadata.append({
                "chunk_idx": str(i),
                "text": chunk,
                "metadata": generate_metadata_from_chunk(chunk),
                "embedding": embeddings[i].tolist(),
                "book": book
            })

            db.collection(book).document(chunks_with_embeddings_metadata[i]["chunk_idx"]).set(chunks_with_embeddings_metadata[i])

        #4. Save chunks to a file
        chunks_dir = Path(__file__).parent / "data" / "chunks"
        chunks_dir.mkdir(parents=True, exist_ok=True)
        with open(chunks_dir / f"chunks_{book}_embed_metadata.json", "w") as f:
            json.dump(chunks_with_embeddings_metadata, f)

if __name__ == "__main__":
    main()