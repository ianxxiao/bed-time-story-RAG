import os
import requests
from typing import Dict, List
from cerebras.cloud.sdk import Cerebras

def generate_metadata_from_chunk(chunk: str) -> Dict[str, str]:
    """
    Generate metadata for a chunk of text using the Cerebras-GPT model.
    Returns a dictionary containing metadata like summary, topics, and key entities.
    
    Args:
        chunk (str): Text chunk to analyze
        
    Returns:
        Dict[str, str]: Dictionary containing metadata fields
    """
    API_KEY = os.getenv("CEREBRAS_API_KEY")
    
    client = Cerebras(api_key=API_KEY)

    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content": "You are a tool that extracts keywords from text. Respond only with a plain list of keywords, seperated by commas."
            },

            {
                "role": "user",
                "content": f"Extract keywords from the following text:\n{chunk}"
            }
        ], 
        model= "llama-3.3-70b"
    )

    return chat_completion.choices[0].message.content