from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def get_dosage_info(query: str):
    # Load the FAISS vector store from disk
    vector_store = FAISS.load_local("faiss_dosage_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    llm = ChatOpenAI(model="gpt-4o")

    
    retriever = vector_store.as_retriever()
    retriever.search_kwargs = {"k": 20}  

    # Retrieve and summarize documents
    retrieved_docs = retriever.invoke(query)
    summaries = [doc.page_content[:300] for doc in retrieved_docs]  
    # Prepare context from summarized documents
    context = "\n".join(summaries)

    # Create the prompt with context and query
    prompt = f"Based on the following information, answer the question:\n\n{context}\n\nQuestion: {query}"

    # Run the query with the LLM
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    return response
