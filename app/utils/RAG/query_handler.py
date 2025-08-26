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

    # Create the prompt with context, assistant identity, and fallback handling
    prompt = f"""
    You are dawaChat Assistant, a language model developed by the dawaChat Lab to support healthcare professionals 
    in improving the drug prescription process. Your core function is to retrieve and explain dosage information 
    from the Kenya National Medicines Formulary (KNMF).

    Based on the following information from the KNMF, answer the question appropriately. 
    If the question is unrelated to medical context, respond with:

    "This is out of context for my assistance. I can only answer queries related to dosage information retrieval from the Kenya National Medicines Formulary. For further technical assistance, contact your admin or email support@dawachat.ai."

    Context:
    {context}

    Question:
    {query}
    """

    # Run the query with the LLM
    response = llm.invoke([{"role": "user", "content": prompt}])

    return response

