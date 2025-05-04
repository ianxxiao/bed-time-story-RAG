import json
from pathlib import Path
from cerebras.cloud.sdk import Cerebras
from pprint import pprint
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
# Load environment variables from .env file
load_dotenv()

def create_story_from_chunks(chunks):
    """
    Create a new story from multiple chunks using Llama model.
    
    Args:
        chunks (list): List of chunk dictionaries containing text and metadata
        
    Returns:
        str: Generated story based on the input chunks
    """
    API_KEY = os.getenv("CEREBRAS_API_KEY")
    if not API_KEY:
        raise ValueError("CEREBRAS_API_KEY not found. Please set it in your .env file or environment variables.")
    
    client = Cerebras(api_key=API_KEY)

    try:
        # Combine text from all chunks
        combined_text = "\n".join([f"\nSummary: {chunk['metadata']} \nFull Text: {chunk['text']}" for chunk in chunks])
        
        # Create prompt for story generation    
        prompt = f"""Here are some story excerpts:\n {combined_text} \n You must use characters from the excerpts while adding new plots. The story should be about 300 words long."""

        # Generate new story using Llama
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a creative storyteller who writes fairy tales in a classic style for children."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b",
            temperature=0.9
        )
    except Exception as e:
        if hasattr(e, 'status_code') and e.status_code == 400:
            # Randomly select 3 chunks if we get a 400 error
            import random
            selected_chunks = random.sample(chunks, min(3, len(chunks)))
            combined_text = "\n".join([f"\nSummary: {chunk['metadata']} \nFull Text: {chunk['text']}" for chunk in selected_chunks])
            
            prompt = f"""Here are some story excerpts:\n {combined_text} \n You must use characters from the excerpts while adding new plots. The story should be about 300 words long."""

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a creative storyteller who writes fairy tales in a classic style for children."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b",
                temperature=0.9
            )
        else:
            raise e

    return chat_completion.choices[0].message.content

def get_user_inputs():
    """
    Get user inputs for searching chunks.
    """
    
    # Get search phrase
    search_phrase = input("Enter a short phrase to search for in the chunks: ")

    return {
        "search_phrase": search_phrase
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

    if len(search_phrase.split()) == 1:
        # For single word searches, use simple string matching
        for chunk in chunks:
            if search_phrase.lower() in chunk['metadata'].lower():
                results.append(chunk)
            
        return results
    
    else:
        # For multi-word searches, use ranking
        model = SentenceTransformer("all-MiniLM-L6-v2")
        search_embedding = model.encode(search_phrase)
        similarities = []
        for chunk in chunks:
            metadata_embedding = model.encode(chunk['metadata'])
            similarity = cosine_similarity([search_embedding], [metadata_embedding])[0][0]
            similarities.append((chunk, similarity))
        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 5 results
        return [chunk for chunk, score in similarities[:5]]

# Example usage
if __name__ == "__main__":
    try:
        user_inputs = get_user_inputs()

        if user_inputs:

            chunks = load_chunks()
            results = search_chunks(chunks, user_inputs['search_phrase'])

            print(f"Found {len(results)} chunks containing the phrase '{user_inputs['search_phrase']}'")

            for i, result in enumerate(results, 1):
                print(f"\nResult {i}:")
                print("\nMetadata: " + result['metadata'])

            story = create_story_from_chunks(results)
            print("\nStory:")
            pprint(story)
            
    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")