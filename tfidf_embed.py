import fitz  # PyMuPDF
import os
from sklearn.feature_extraction.text import TfidfVectorizer



def create_vocab():
    def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text

    pdf_folder = "extracted_files/data 2"
    all_texts = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_folder, filename)
            text = extract_text_from_pdf(file_path)
            all_texts.append(text)



    vectorizer = TfidfVectorizer(
                                stop_words='english',
                                ngram_range=(1,2))

    vectorizer.fit(all_texts)
    return vectorizer


def embed_using_tfidf(text):
  vectorizer = create_vocab()  # Assuming pdf_list is not needed here
  vectorized_text = vectorizer.transform([text])
  return vectorized_text.toarray()

 
