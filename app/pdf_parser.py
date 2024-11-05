from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
import fitz  

def read_pdf(file_path: str) -> str:
    try:
        doc = fitz.Document(file_path)
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()
        return pdf_text
    except Exception as e:
        print("Error reading PDF:", e)
        return ""

def process_and_store_pdf_content(file_path: str):
    # Read PDF content
    pdf_content = read_pdf(file_path)
    
    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(pdf_content)
    
    # Create embeddings for each chunk and store them
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Save the vector store to disk for later retrieval
    vector_store.save_local("faiss_dosage_index")

