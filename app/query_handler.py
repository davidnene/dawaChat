from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def get_dosage_info(query: str):
    # Load the FAISS vector store from disk
    vector_store = FAISS.load_local("faiss_dosage_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # Retrieve relevant documents based on the query
    retrieved_docs = vector_store.as_retriever().invoke(query)
    context = "\n".join([doc.page_content for doc in retrieved_docs]) 

    # Create a prompt that includes the query and the context
    prompt = f"Based on the following information, answer the question:\n\n{context}\n\nQuestion: {query}"
    response = llm.invoke(prompt)

    return response
