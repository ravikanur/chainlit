from llama_index.core.retrievers import BaseRetriever, VectorIndexRetriever, KeywordTableSimpleRetriever
from llama_index.core import QueryBundle

class Custom_Retriever(BaseRetriever):
  def __init__(self, vector_retriever: VectorIndexRetriever,
               keyword_retriever: KeywordTableSimpleRetriever, mode: str = "AND"):
    self.vector_retriever = vector_retriever
    self.keyword_retriever = keyword_retriever
    self.mode = mode
    super().__init__()

  def _retrieve(self, query_bundle: QueryBundle):
    vector_nodes = self.vector_retriever.retrieve(query_bundle)
    keyword_nodes = self.keyword_retriever.retrieve(query_bundle)

    vector_ids = {n.node.node_id for n in vector_nodes}
    keyword_ids = {n.node.node_id for n in keyword_nodes}

    combine_dict = {n.node.node_id: n for n in vector_nodes}
    combine_dict.update({n.node.node_id: n for n in keyword_nodes})

    if self.mode == "AND":
      retrieve_ids = vector_ids.intersection(keyword_ids)
    else:
      retrieve_ids = vector_ids.union(keyword_ids)

    retrieve_nodes = [combine_dict[rid] for rid in retrieve_ids]
    return retrieve_nodes