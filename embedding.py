from sentence_transformers import SentenceTransformer

def embed(chunk):
    """
    Embed the sections using a pre-trained model.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(chunk)  # Returns a 384-dimensional vector

    return embedding