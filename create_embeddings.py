import os
import torch
from sentence_transformers import SentenceTransformer
from embed import load_and_chunk_multiple_pdfs_faster
import fitz  # PyMuPDF

from tfidf_embed import embed_using_tfidf  # Uncomment if you want to use the TF-IDF embedding function
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

#for context aware embeddings
def create_embeddings_context_aware(pdf_paths, embed_model='sentence-transformers/static-similarity-mrl-multilingual-v1'):
    model = SentenceTransformer(embed_model)
    device = torch.device("cpu")
    model.to(device)
    embeddings = {}

    for pdf in pdf_paths:
        try:
            team_name = os.path.basename(pdf).split(".pdf")[0].split(" ")[1]
        except:
            team_name = os.path.basename(pdf).split(".pdf")[0]
            
        embeddings[team_name] = load_and_chunk_multiple_pdfs_faster(pdf, model=model)

    return embeddings

#for para-phrase embeddings

def create_embeddings_paraphrase_aware(pdf_paths, embed_model='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
    model = SentenceTransformer(embed_model)
    device = torch.device("cpu")
    model.to(device)
    embeddings = {}

    for pdf in pdf_paths:
        
        try:
            team_name = os.path.basename(pdf).split(".pdf")[0].split(" ")[1]
        except:
            team_name = os.path.basename(pdf).split(".pdf")[0]
        embeddings[team_name] = load_and_chunk_multiple_pdfs_faster(pdf, model=model)

    return embeddings

def create_tfidf_embeddings(pdf_paths):

    def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    embeddings = {}

    for pdf in pdf_paths:
        try:
            team_name = os.path.basename(pdf).split(".pdf")[0].split(" ")[1]
        except:
            team_name = os.path.basename(pdf).split(".pdf")[0]
        text = extract_text_from_pdf(pdf)
        embeddings[team_name] = embed_using_tfidf(text)

    return embeddings
