import streamlit as st
import zipfile
import io
import os
from sentence_transformers import SentenceTransformer
from embed import load_and_chunk_multiple_pdfs_faster
from tfidf_embed import embed_using_tfidf  # Uncomment if you want to use the TF-IDF embedding function
from create_embeddings import create_embeddings_context_aware, create_tfidf_embeddings
from calculate_similarity import calculate_similarity, calculate_tfidf_similarity, calculate_composite_similarity
from create_report import save_similarity_report
#os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

embed_model = 'sentence-transformers/static-similarity-mrl-multilingual-v1'



def main():
    st.logo("IIT_Madras_Logo.svg.png",  size="large")
    st.set_page_config(page_title="Software Engineering Project Similarity Analysis", page_icon=":mag_right:", layout="wide")


    st.title("Software Engineering Project Similarity Analysis")
    st.subheader("B.S. in Data Science & Applications, IIT Madras")

    st.markdown(
    "<div style='font-size: 14px; color: grey;'>Developed by Indranil Bhattacharyya · Course Plagiarism Auditing Tool</div>",
    unsafe_allow_html=True
)
    st.caption("Powered by semantic (Transformer-based) and lexical (TF-IDF) similarity measures to identify potential overlap in team submissions.")

    label = "Upload your zip file here"
    uploaded_file = st.file_uploader("Upload your zip file here", type="zip")
    
    if st.button("Analyze"):
        if uploaded_file is not None:
            
                

            st.success("ZIP file uploaded successfully!")

            # Read the uploaded file as a zip file in memory
            #Extract the zip file
            extract_folder = "extracted_files"
            os.makedirs(extract_folder, exist_ok=True)
            zip_save_path = "uploaded.zip"
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall(extract_folder)
            #st.success(f"ZIP file extracted to folder: {extract_folder}")


            pdf_list = [i for i in os.listdir("extracted_files/data") if i.endswith('.pdf')]
            sorted_pdf_list = sorted(pdf_list)


            # using high-level embedding function
            with st.spinner(text="In progress...", show_time=True):


                team_embed_dict_context = create_embeddings_context_aware([os.path.join("extracted_files/data", pdf) for pdf in sorted_pdf_list], embed_model=embed_model)
                team_embed_dict_tfidf = create_tfidf_embeddings([os.path.join("extracted_files/data", pdf) for pdf in sorted_pdf_list])
                #st.success("Embeddings created successfully!") 

                
                
                context_aware_similarity_dict = calculate_similarity(team_embed_dict_context, embed_model=embed_model)
                tfidf_similarity_dict = calculate_tfidf_similarity(team_embed_dict_tfidf)
                composite_similarity_dict = calculate_composite_similarity(context_aware_similarity_dict, tfidf_similarity_dict)
                #st.success("Similarity calculations completed successfully!")
                
                
                

                
                # Create and save the similarity report
                report_path = "similarity_report.pdf"
                save_similarity_report(composite_similarity_dict, report_path,
                                    )
                
                st.success("Similarity report created successfully!")
                st.download_button(
                    label="Download Similarity Report",
                    data=open(report_path, "rb").read(),
                    file_name="similarity_report.pdf",
                    mime="application/pdf"
                )




if __name__ == "__main__":
    main()
    # Uncomment the line below to run the app
    