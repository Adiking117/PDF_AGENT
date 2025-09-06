# 📄 PDF Workflow Agent

A **FastAPI-based PDF Workflow Agent** that allows you to query PDFs for answers, summaries, or quizzes using AI models.  
Built with **LangChain, ChromaDB, and LLaMA3/Groq models** for local AI inference and embeddings.

---

## 📚 Table of Contents
- [Project Overview](#-project-overview)
- [Features](#-features)
- [Workflow Overview](#-workflow-overview)
- [Architecture](#-architecture)
- [Installation](#️-installation)
- [Usage](#-usage)
- [Code Explanation](#-code-explanation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📝 Project Overview
This project processes PDFs and responds intelligently to user queries.  
Depending on the query type, it can:

- **Answer questions** from the PDF content.  
- **Summarize** the entire PDF or specific topics.  
- **Generate quizzes** based on the PDF content or topics.  

The workflow uses AI models for:
- Text classification  
- Summarization  
- Question answering  
- Quiz generation  

It stores PDF embeddings locally in **ChromaDB** for efficient retrieval.

---

## ✨ Features
- 📂 **PDF Loading** — Automatically loads and reads PDF files.  
- 🧠 **Query Classification** — Classifies user queries into five categories:
  - `qa` → Question answering  
  - `summpdf` → Summarize full PDF  
  - `quizpdf` → Generate a quiz for the full PDF  
  - `summtopic` → Summarize a specific topic  
  - `quiztopic` → Generate a quiz for a specific topic  
- ✂️ **Text Extraction & Splitting** — Extracts full text and splits into chunks for efficient retrieval.  
- 💾 **Embedding Storage** — Uses HuggingFace embeddings + ChromaDB for vectorized storage of PDF chunks.  
- 🎯 **Intelligent Retrieval** — Retrieves most relevant chunks using MMR (Maximal Marginal Relevance).  
- 🤖 **AI-powered Responses** — Generates answers, summaries, or quizzes using **LLaMA3-8B**.  

---

## 🔄 Workflow Overview
The workflow follows a graph-based node pipeline implemented using **langgraph**.

### Step 1: Load PDF
- **Node**: `load_pdf_node`  
- Loads the PDF file using PyPDFLoader.  
- Classifies the user query into one of the five categories using a ChatGroq model.  

### Step 2: Branching
Depending on the query type, the workflow takes one of two paths:

#### PDF-level queries
- Queries: `summpdf`, `quizpdf`  
- Steps:  
  1. `extract_text_node` → Extract full text from PDF  
  2. `summarize_text_node` / `generate_quiz_node` → Summarize or generate quiz for the entire PDF  

#### Retrieval-based queries
- Queries: `qa`, `summtopic`, `quiztopic`  
- Steps:  
  1. `split_pdf_node` → Split PDF into smaller chunks  
  2. `embed_pdf_node` → Create or load embeddings in ChromaDB  
  3. `get_similar_pages_node` → Retrieve most relevant chunks based on the query  
  4. Final nodes:  
     - `answer_question_on_query_node` → Answer question  
     - `summarize_on_topic_node` → Summarize topic  
     - `generate_quiz_on_topic_node` → Generate quiz  

### Step 3: Generate Output
- Final answer, summary, or quiz is stored in `state["answer"]`.  
- Users can also stream intermediate steps using `app.stream(initial_state)`.  

---

## 🏗 Architecture
```
User Query
   │
   ▼
Load PDF & Classify Query
   │
   ├─ PDF-level ──► Extract Text ──► Summarize / Quiz
   │
   └─ Retrieval-level ──► Split PDF ──► Embed in ChromaDB ──► Retrieve Relevant Pages
                              │
                              ├─► QA
                              ├─► Summarize Topic
                              └─► Quiz on Topic
```

### Key Components
- **LangChain Groq Model (ChatGroq)** — Handles query classification & text generation.  
- **Vector Store (ChromaDB)** — Stores PDF chunks as embeddings for semantic search.  
- **Text Splitter (RecursiveCharacterTextSplitter)** — Splits long PDF content into manageable chunks with overlap.  
- **Workflow Graph (StateGraph)** — Defines nodes & routing logic for PDF processing.  

---

## ⚙️ Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-workflow-agent.git
cd pdf-workflow-agent

# Install dependencies
pip install -r requirements.txt

# Configure your LLaMA3/Groq model
export HF_HOME="/path/to/your/local/models"

# Place your PDF file(s) in the project directory
```

---

## 🚀 Usage
### Basic Example
```python
from workflow import PDFChatState, app

initial_state = PDFChatState(
    pdfpath="container.pdf",
    userQuery="Explain Dependency Injection in Spring Boot",
)

final_state = app.invoke(initial_state)
print("Answer:", final_state["answer"])
```

---

## 🛠 Code Explanation

### PDF Loading
- Uses **PyPDFLoader** to read PDFs.  
- The state dictionary (`PDFChatState`) stores loaded content.  

### Query Classification
- **ChatGroq model** classifies the user query into one of five categories.  
- **Parser** ensures strict JSON output.  

### Text Extraction & Splitting
- `extract_text_node` → Extracts full PDF text.  
- `split_pdf_node` → Splits text into chunks for embedding.  

### Embedding & Retrieval
- `embed_pdf_node` → Uses HuggingFace embeddings + ChromaDB for storing chunk embeddings.  
- `get_similar_pages_node` → Retrieves most relevant chunks using MMR.  

### Answer / Summary / Quiz Generation
- Workflow routes to the appropriate node based on query type.  
- AI model generates the final answer using retrieved chunks or full PDF content.  

### Workflow Graph
- Nodes connected using **langgraph** with conditional edges based on query type.  
- `first_router` and `second_router` decide the path.  

---

## 🤝 Contributing
Contributions are welcome! To contribute:

1. Fork the repository.  
2. Create a new branch.  
3. Make your changes.  
4. Submit a pull request.  

---

## 📜 License
This project is licensed under the MIT License.  
