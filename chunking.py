def fixed_chunk_size(markdown_text, chunk_size=1000):
    """
    Chunk the markdown text into sections of a fixed size.
    """
    return [markdown_text[i:i+chunk_size] for i in range(0, len(markdown_text), chunk_size)]

def fixed_chunk_overlap(markdown_text, chunk_size=1000, overlap=200):
    """
    Chunk the markdown text into sections of a fixed size with a fixed overlap.
    """
    chunks = []
    for i in range(0, len(markdown_text), chunk_size-overlap):
        chunks.append(markdown_text[i:i+chunk_size])
    return chunks

