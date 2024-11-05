from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def get_dosage_info(query: str):
    # Load the FAISS vector store from disk
    vector_store = FAISS.load_local("faiss_dosage_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # # Retrieve relevant documents based on the query
    # retrieved_docs = vector_store.as_retriever().invoke(query)
    # context = "\n".join([doc.page_content for doc in retrieved_docs]) 

    # # Create a prompt that includes the query and the context
    # prompt = f"Based on the following information, answer the question:\n\n{context}\n\nQuestion: {query}"
    # response = llm.invoke(prompt)
    
    # llm = ChatOpenAI(model="gpt-3.5-turbo")
    # # Set up RetrievalQA with the preloaded vector store
    # qa = RetrievalQA.from_llm(llm=llm, retriever=vector_store.as_retriever())
    
    # # Run the query
    # response = qa.run(query)
    
    
    retriever = vector_store.as_retriever()
    retriever.search_kwargs = {"k": 20}  # Limit retrieval to top 5 documents

    # Retrieve and summarize documents
    retrieved_docs = retriever.invoke(query)
    summaries = [doc.page_content[:300] for doc in retrieved_docs]  # Take the first 300 characters of each document

    # Prepare context from summarized documents
    context = "\n".join(summaries)

    # Create the prompt with context and query
    prompt = f"Based on the following information, answer the question:\n\n{context}\n\nQuestion: {query}"

    # Run the query with the LLM
    response = llm.invoke([{"role": "user", "content": prompt}])
    

    return response
