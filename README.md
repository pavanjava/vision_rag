# SEC-10K Financial Document Analysis System

A RAG-based system for analyzing SEC-10K financial reports using vision models and vector databases.

## System Architecture

```
PDF → Images → Vision Model (vLLM) → Text Extraction → Vector Store (Qdrant) → RAG Agent
```

## Components

### 1. Document Processing Pipeline

**`knowledge_to_image_converter.py`**
- Converts PDF pages to images
- Supports single page or batch conversion
- Output: PNG images at configurable DPI

**`image_to_base64_converter.py`**
- Converts images to base64 data URIs
- Supports PNG, JPG, JPEG, GIF, WebP formats

### 2. Vision Model Integration

**`image_inferer.py`**
- Client for vLLM Vision API (Qwen3-VL-8B-Instruct)
- Extracts text from financial document images
- Supports both URL and local image input

**Endpoint:** `https://s7z2ms3wud6hm6-8000.proxy.runpod.net/v1/`

### 3. Knowledge Base Ingestion

**`ingestion_pipe.py`**
- Chunks extracted text using semantic chunking
- Stores embeddings in Qdrant vector database
- Uses BAAI/bge-base-en-v1.5 embeddings

### 4. RAG Agent

**`rag_agent.py`**
- Queries Qdrant knowledge base
- Uses Claude/vLLM for response generation
- Specialized for SEC-10K financial analysis

## Setup

### Requirements

```bash
pip install agno llama-index qdrant-client pdf2image pillow requests python-dotenv chonkie
```

### Environment Variables

```env
COLLECTION_NAME=your_collection_name
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=th3s3cr3tk3y
ANTHROPIC_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
```

### External Dependencies

- **Poppler**: Required for PDF to image conversion
    - Ubuntu: `sudo apt-get install poppler-utils`
    - macOS: `brew install poppler`
- **Qdrant**: Vector database (runs on port 6333)
- **vLLM Server**: Vision model inference endpoint

## Usage Workflow

### Step 1: Convert PDF to Images

```python
from core.knowledge_to_image_converter import pdf_to_images

pdf_to_images(
    "data/report.pdf", 
    output_folder="output_images",
    page_number=7  # Optional: specific page
)
```

### Step 2: Extract Text from Images

```python
from core.image_inferer import VLLMVisionClient

client = VLLMVisionClient()
response = client.chat_with_local_image(
    text_prompt="Extract all information in paragraph format.",
    image_path="output_images/report_page_7.png"
)
text = client.extract_response_text(response)
```

### Step 3: Ingest to Vector Database

```python
from core.ingestion_pipe import ingest_data_to_store

ingest_data_to_store(text)
```

### Step 4: Query with RAG Agent

```python
from core.rag_agent import agent

agent.print_response(
    input="What are Total current assets in September 30, 2025?"
)
```

## Key Features

- **Vision-based extraction**: Handles tables, charts, and formatted financial data
- **Semantic chunking**: Intelligent text segmentation preserving context
- **Vector similarity search**: Fast retrieval with top-k results (k=15)
- **Multi-model support**: Claude, Gemini, GPT-4, Ollama, vLLM
- **Structured outputs**: Bullet points and tabular responses

## GPU Configuration

The system runs on **4x NVIDIA GeForce RTX 5090** (32GB each) with tensor parallelism for distributed inference.

## Notes

- Vision model excels at extracting structured financial data from images
- Agent restricted to provided context only (no hallucination)
- Supports Google Search integration for external validation
- Default embedding dimension: 768 (FastEmbed)
- Retrieval: Top 15 most relevant chunks per query

## Credits

This project is built using the following excellent tools and frameworks:

- **[Agno](https://github.com/agno-agi/agno)** - AI agent framework for building intelligent applications
- **[LlamaIndex](https://www.llamaindex.ai/)** - Data framework for LLM applications with RAG capabilities
- **[Qdrant](https://qdrant.tech/)** - High-performance vector database for similarity search
- **[vLLM](https://github.com/vllm-project/vllm)** - Fast and efficient LLM inference engine
- **[RunPod](https://www.runpod.io/)** - GPU cloud infrastructure for AI workloads