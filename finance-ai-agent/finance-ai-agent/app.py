import streamlit as st
import os
from dotenv import load_dotenv

# --------------------------------------------------
# 🔐 LOAD SECRETS FROM ENVIRONMENT VARIABLES
# --------------------------------------------------

# --------------------------------------------------
# 🚨 SAFETY CHECK: stop app if keys are missing
# --------------------------------------------------
required_vars = [
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_SEARCH_KEY,
    AZURE_SEARCH_ENDPOINT
]

if not all(required_vars):
    st.error("❌ Missing environment variables. Please set them in a .env file.")
    st.stop()

# --------------------------------------------------
# 📦 LANGCHAIN IMPORTS
# --------------------------------------------------
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --------------------------------------------------
# 🎨 STREAMLIT UI CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AI Finance Analyst", layout="wide")
st.title("📈 Agentic Finance Analyst")
st.markdown("### Grounded Financial Intelligence via Azure RAG")

# --------------------------------------------------
# 🏗️ RAG ENGINE SETUP
# --------------------------------------------------
@st.cache_resource
def get_rag_chain():
    """Initializes Azure services and builds the RAG chain."""

    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-3-small",
        api_version="2024-06-01"
    )

    llm = AzureChatOpenAI(
        azure_deployment="gpt-4o-mini",
        api_version="2024-06-01",
        temperature=0
    )

    vector_store = AzureSearch(
        azure_search_endpoint=AZURE_SEARCH_ENDPOINT,
        azure_search_key=AZURE_SEARCH_KEY,
        index_name="finance-index",
        embedding_function=embeddings.embed_query
    )

    system_prompt = (
        "You are a professional financial analyst. Use the provided context "
        "to answer the question. If the answer isn't in the context, "
        "say you don't know based on the documents. Always cite sources.\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(
        vector_store.as_retriever(),
        combine_docs_chain
    )

# --------------------------------------------------
# 🚦 INITIALIZATION
# --------------------------------------------------
rag_chain = None

try:
    with st.sidebar:
        st.header("Connection Status")
        rag_chain = get_rag_chain()
        st.success("✅ Connected to Azure AI Services")
except Exception as e:
    st.sidebar.error("❌ Connection Failed")
    st.sidebar.exception(e)
    st.stop()

# --------------------------------------------------
# 💬 CHAT STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --------------------------------------------------
# 🧠 USER INPUT
# --------------------------------------------------
if prompt := st.chat_input("Ask about the 10-K financial performance..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing financial documents..."):
            if rag_chain:
                response = rag_chain.invoke({"input": prompt})
                answer = response["answer"]
                st.write(answer)

                with st.expander("📚 View Document Citations"):
                    for doc in response["context"]:
                        source_name = doc.metadata.get("source", "Unknown Doc")
                        page_num = doc.metadata.get("page", "N/A")
                        st.write(f"**Source:** {source_name} | **Page:** {page_num}")

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            else:
                st.error("RAG engine is not initialized.")
