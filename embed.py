
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import numpy as np
from sentence_transformers import SentenceTransformer
embed_model = 'sentence-transformers/static-similarity-mrl-multilingual-v1'
model = SentenceTransformer(embed_model)

def load_and_chunk_multiple_pdfs_faster(pdf_paths, chunk_size=256, chunk_overlap=64, model=model):
    


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,

        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
        keep_separator=True
    )

    loader = PyMuPDFLoader(pdf_paths)
    docs = loader.load()

    # Process each page individually
    all_chunks = []
    for doc in docs:
        chunks = text_splitter.split_text(doc.page_content)
        all_chunks.extend(chunks)

    embeddings = model.encode(all_chunks, normalize_embeddings=True)
    document_embedding = np.mean(embeddings, axis=0)  # Simple average
    document_embedding = document_embedding / np.linalg.norm(document_embedding)  # Normalize


    return document_embedding.reshape(1,-1)





