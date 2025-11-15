import os

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.llamaindex import LlamaIndexVectorDb
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, Settings
# from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
# from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from qdrant_client import QdrantClient
# from agno.utils.pprint import pprint_run_response
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.models.ollama import Ollama
from agno.models.vllm import VLLM
from agno.tools.googlesearch import GoogleSearchTools

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-001",
#                                             embedding_config=EmbedContentConfig(output_dimensionality=768))
Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

qdrant_connector = QdrantClient(url="http://localhost:6333", api_key="th3s3cr3tk3y")

def retrieve_iso_knowledge_base():
    if qdrant_connector.collection_exists(collection_name=os.environ.get("COLLECTION_NAME")):
        vector_store = QdrantVectorStore(client=qdrant_connector, collection_name=os.environ.get("COLLECTION_NAME")) # collection name should match the collection name while ingesting
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)
        retriever = index.as_retriever(top_k=15)
        knowledge = Knowledge(
            vector_db=LlamaIndexVectorDb(knowledge_retriever=retriever)
        )
        return knowledge
    else:
        # handle the fallback if not qdrant
        pass


kb = retrieve_iso_knowledge_base()

### Agent use OpenAI for Response

SYSTEM_PROMPT = (
    "You are an expert Financial Data Analysis "
    "specialized in SEC-10K reports. Your primary role is to provide accurate and detailed "
    "answers to questions *about* the SEC-10K standards and to summarize details "
    "or the overall content of the *provided SEC-10K context*."
    "IMPORTANT: Do not use external knowledge, previous knowledge or make up information. Only use the context provided to you. "
    "If you dont find the answer politely say you dont know the answer"
    "MOST IMPORTANT: Always provide the information in bullets"
)

#gemini_llm = Gemini(id="gemini-2.5-flash", temperature=0.7, api_key=os.environ.get("GEMINI_API_KEY"))
claude_llm = Claude(id="claude-sonnet-4-20250514", temperature=0.7, api_key=os.environ.get("ANTHROPIC_API_KEY"))
# gpt_llm = OpenAIChat(id="gpt-4o", temperature=0.7, api_key=os.environ.get("OPENAI_API_KEY"))
# llm = Ollama(id='gemma3:12b')
vllm = VLLM(id="Qwen/Qwen3-VL-8B-Instruct", base_url=f"{os.environ.get('VLLM_API_URL')}/v1/")

def create_claude_agent():
    # Instantiate the Agno Agent with the knowledge base
    _agent = Agent(
        model=vllm,
        # tools=[GoogleSearchTools(fixed_max_results=5)],
        # search_knowledge=True,
        debug_mode=True,
        system_message=SYSTEM_PROMPT,
        instructions="Always give the response in bullets or tabular format."
    )
    return _agent

agent = create_claude_agent()

query = "What are Total current assets in September 30, 2025?"
# query = "What are the total Asbestos-related liabilities?"

context = ''
documents = kb.search(query=query, max_results=10)
for document in documents:
    context += document.content

input_and_context = f'Query:{query}\n\nContext:{context}'

agent.print_response(input=input_and_context)
