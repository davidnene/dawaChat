from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
import pdfplumber

def read_pdf(file_path: str) -> str:
    pdf_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                pdf_text += page.extract_text()
        return pdf_text
    except Exception as e:
        print("Error reading PDF:", e)
        return ""

def process_and_store_pdf_content(file_path: str):
    # Read PDF content
    pdf_content = read_pdf(file_path)
    if not pdf_content:
        print("No text extracted from the PDF.")
    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(pdf_content)
    
    # Create embeddings for each chunk and store them
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Save the vector store to disk for later retrieval
    vector_store.save_local("faiss_dosage_index")

