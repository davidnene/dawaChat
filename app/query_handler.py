from langchain import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def get_dosage_info(query: str):
    # Load the FAISS vector store from disk
    vector_store = FAISS.load_local("faiss_dosage_index", OpenAIEmbeddings())
    
    # Set up RetrievalQA with the preloaded vector store
    qa = RetrievalQA.from_llm(retriever=vector_store.as_retriever())
    
    # Run the query
    response = qa.run(query)
    return response
