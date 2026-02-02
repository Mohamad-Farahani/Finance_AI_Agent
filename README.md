# 📈 Agentic Finance Analyst (RAG with Azure AI)

![Demo of the application](assets/demo.gif)

A Streamlit-based AI finance assistant that uses **Retrieval-Augmented Generation (RAG)** with **Azure OpenAI** and **Azure AI Search** to answer questions grounded in financial documents (e.g., 10-K reports).

The system retrieves relevant document chunks from an indexed vector store and generates reliable, source-cited answers using an LLM.

---

## 🚀 Features

- 🔎 Document retrieval using Azure AI Search
- 🧠 LLM-powered answers via Azure OpenAI (GPT-4o-mini)
- 📚 Source citation for transparency
- 💬 Interactive chat UI (Streamlit)
- 🔐 Secure API key handling via environment variables
- ⚡ Cached RAG pipeline for performance

---

## 🏗️ Architecture

1. User asks a financial question
2. Query is embedded using Azure OpenAI embeddings
3. Relevant chunks are retrieved from Azure AI Search
4. LLM generates an answer using retrieved context
5. Sources are displayed to the user

---

## 🧪 Tech Stack

- Python
- Streamlit
- Azure OpenAI
- Azure AI Search
- LangChain
- dotenv

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Mohamad-Farahani/Finance_AI_Agent.git
cd Finance_AI_Agent
