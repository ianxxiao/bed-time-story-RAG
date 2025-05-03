import json
from pathlib import Path

def get_user_inputs():
    """
    Get user inputs for searching chunks.
    """
    
    # Get search phrase
    search_phrase = input("Enter a short phrase to search for in the chunks: ")

    # Get chunk parameters
    chunk_size = input("Enter chunk size (default 1000): ") or 1000
    chunk_overlap = input("Enter chunk overlap (default 200): ") or 200


    return {
        "search_phrase": search_phrase,
        "chunk_size": int(chunk_size),
        "chunk_overlap": int(chunk_overlap),
    }

def load_chunks():
    """
    Load chunks from the JSON file.
    """
    with open(Path(__file__).parent / "data" / "chunks" / "chunks_TheBlueFairyBook_embed_metadata.json", 'r') as f:
        return json.load(f)
    
def search_chunks(chunks, search_phrase):
    """
    Search for the phrase in the chunks.
    """
    results = []
    for chunk in chunks:
        if search_phrase.lower() in chunk['metadata'].lower():
            results.append(chunk)
    return results

# Example usage
if __name__ == "__main__":

    user_inputs = get_user_inputs()

    if user_inputs:

        chunks = load_chunks()

        results = search_chunks(chunks, user_inputs['search_phrase'])

        print(f"Found {len(results)} chunks containing the phrase '{user_inputs['search_phrase']}'")

        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print("\nMetadata: " + result['metadata'])
            print("\nText: " + result['text'][:200] + "...")  # Print first 200 characters of each result

