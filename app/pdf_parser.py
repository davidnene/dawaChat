from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

def process_and_store_pdf_content(pdf_content: str):
    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(pdf_content)
    
    # Create embeddings for each chunk and store them
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Save the vector store to disk for later retrieval
    vector_store.save_local("faiss_dosage_index")

