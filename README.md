# Software Engineering Project Similarity Analyzer - PlagTrace

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated tool designed to analyze and identify similarities in academic documents, specifically tailored for software engineering project reports. This application leverages a hybrid approach, combining semantic and lexical analysis with paraphrasing detection to provide a robust similarity score, helping educators and auditors detect potential plagiarism or unauthorized collaboration.

The tool is presented through an interactive Streamlit web interface, allowing users to upload a single ZIP file containing multiple team reports (in PDF format) and receive a detailed, color-coded similarity report.

## ✨ Key Features

- **Hybrid Similarity Engine**: Utilizes context-aware transformer models, traditional TF-IDF vectorization, and a paraphrasing-aware component to capture a comprehensive spectrum of similarities.
- **Semantic Analysis**: Employs `sentence-transformers` models (specifically `static-similarity-mrl-multilingual-v1` and `paraphrase-multilingual-MiniLM-L12-v2`) to understand the conceptual meaning and context of the text, identifying similarities even when phrasing is different.
- **Lexical Analysis**: Uses TF-IDF to detect direct copy-pasting of text and identical phrasing.
- **Paraphrasing Detection**: Integrates a dedicated model to identify reworded yet semantically equivalent content.
- **Composite Scoring**: Combines the semantic, lexical, and paraphrasing scores into a single, weighted composite score for a more accurate and reliable assessment.
- **Batch Processing**: Accepts a `.zip` archive containing multiple PDF documents, automatically extracting and processing each one.
- **Interactive Web UI**: A user-friendly interface built with Streamlit for easy file uploads and analysis.
- **Automated PDF Reporting**: Generates a professional, multi-page PDF report summarizing the findings, with color-coded risk levels for quick interpretation.

## ⚙️ How It Works (Methodology)

The system calculates similarity through a robust, multi-stage process:

1.  **PDF Parsing & Chunking**: Each PDF document is parsed to extract raw text. The text is then broken down into smaller, manageable chunks using `langchain`'s text splitters.

2.  **Multi-Modal Embedding Strategy**:

    * **Context-Aware Embeddings**: Using the `sentence-transformers/static-similarity-mrl-multilingual-v1` model, the system generates dense vector representations (embeddings) for each document. This model is adept at capturing the semantic essence of the text.
    * **TF-IDF Embeddings**: A Term Frequency-Inverse Document Frequency (TF-IDF) matrix is constructed from the entire corpus of documents. This method excels at identifying key terms and lexical overlap.
    * **Paraphrase Embeddings**: The `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` model is used to generate embeddings specifically tuned for detecting paraphrased content.

3.  **Similarity Calculation**:

    * Cosine similarity is calculated between the context-aware and paraphrase embeddings of each pair of documents.
    * A dot product is used to find the similarity between the TF-IDF vectors.

4.  **Composite Score Generation**: The final similarity score is a weighted average of the context-aware, TF-IDF, and paraphrasing similarities, providing a balanced view of conceptual overlap, literal duplication, and rephrased content. The current weighting is:

    $$
    \text{Composite Score} = (0.4 \times \text{Contextual Similarity}) + (0.4 \times \text{Paraphrasing Similarity}) + (0.2 \times \text{TF-IDF Similarity})
    $$

5.  **Report Generation**: The results are compiled into a PDF report using `reportlab`, highlighting pairs of teams with similarity scores and providing a clear methodology explanation.

## 🛠️ Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **Machine Learning / NLP**: [Sentence-Transformers](https://www.sbert.net/), [Scikit-learn](https://scikit-learn.org/), [LangChain](https://www.langchain.com/), [PyTorch](https://pytorch.org/)
-   **PDF Processing**: [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
-   **Report Generation**: [ReportLab](https://www.reportlab.com/)
-   **Core Libraries**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)

## 🚀 Setup and Installation

Follow these steps to run the project locally.

**1. Clone the Repository**

```bash
git clone <your-repository-url>
cd <repository-directory>
```

**2. Create and Activate a Virtual Environment**

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Install Dependencies**

All required packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 🏃‍♀️ Usage

**1. Run the Streamlit Application**

Execute the `main.py` script from your terminal:

```bash
streamlit run main.py
```

**2. Use the Web Interface**

-   Your web browser should automatically open to the application's URL (usually `http://localhost:8501`).
-   Prepare a single `.zip` file containing all the team project reports in PDF format.
-   Use the file uploader on the web page to select and upload your `.zip` file.
-   Click the **"Analyze"** button to start the similarity analysis.
-   The process may take a few moments depending on the number and size of the documents.
-   Once complete, a "Download Similarity Report" button will appear. Click it to download the generated PDF report.

## 📁 Repository Structure

```
.
├── .gitignore               # Specifies files for Git to ignore
├── main.py                  # Main Streamlit application file
├── embed.py                 # Functions for creating context-aware embeddings
├── tfidf_embed.py           # Functions for creating TF-IDF embeddings
├── create_embeddings.py     # Module to generate all types of embeddings
├── calculate_similarity.py  # Logic for similarity score computation
├── create_report.py         # Generates the final PDF report
├── create_report_normal.py  # An alternative report generation script (can be removed if not needed)
├── requirements.txt         # Project dependencies
├── Dockerfile               # Docker configuration for containerization
└── README.md                # This README file
```

## ✍️ Author

This project was developed by **Indranil Bhattacharyya** as a course plagiarism auditing tool for the B.S. in Data Science & Applications program at IIT Madras.
```