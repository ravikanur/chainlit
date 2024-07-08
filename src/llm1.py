from llama_index.core import (VectorStoreIndex, SimpleDirectoryReader, SimpleKeywordTableIndex, Settings,
                              StorageContext, get_response_synthesizer)
from llama_index.core.retrievers import KeywordTableSimpleRetriever, VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.callbacks.base import CallbackManager
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from src.customRetriever import Custom_Retriever

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

class llm_model:
    def __init__(self):
        Settings.chunk_size = 200
        Settings.chunk_overlap = 50
        Settings.llm = OpenAI(model = "gpt-3.5-turbo")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
 
    def read_data_and_build_context(self, path="./Data1") -> StorageContext:
        loader = SimpleDirectoryReader(path)
        documents = loader.load_data()
        nodes = Settings.node_parser.get_nodes_from_documents(documents)
        storage_context = StorageContext.from_defaults()
        storage_context.docstore.add_documents(nodes)
        return storage_context, nodes
    
    def build_index_and_retriever(self,storage_context, nodes) -> Custom_Retriever:
        vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
        keyword_index = SimpleKeywordTableIndex(nodes, storage_context=storage_context)
        vector_retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3)
        keyword_retriever = KeywordTableSimpleRetriever(index=keyword_index)
        custom_retriever = Custom_Retriever(vector_retriever, keyword_retriever)
        return custom_retriever
    
    def build_queryengine(self, custom_retriever) -> RetrieverQueryEngine:
        response_synthesizer = get_response_synthesizer(streaming=True)
        query_engine = RetrieverQueryEngine.from_args(retriever=custom_retriever, streaming=True, 
                                                      response_synthesizer=response_synthesizer)
        return query_engine
    
    def set_callback_handler(self, callback_handler) -> None:
        Settings.callback_manager = CallbackManager([callback_handler])
    
