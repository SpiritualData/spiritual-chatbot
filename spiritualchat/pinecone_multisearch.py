"""Search in Pinecone using namespaces and metadata filters, and support multiple queries by namespace as part of a single retrieval call."""
import hashlib
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.embeddings.base import Embeddings
from langchain.schema import BaseRetriever, Document


class PineconeMultiSearchRetriever(BaseRetriever, BaseModel):
    embeddings: Embeddings
    sparse_encoder: Any
    index: Any
    top_k: int = 4
    alpha: float = 0.5

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def get_relevant_documents(self, namespace_queries: dict, metadata_filter: dict=None) -> List[Document]:
        """
        Args:
            namespace_queries (dict): Key is namespace in the Pinecone index. Value is a list of strings (queries to embed).
            metadata_filter (dict): Key is the metadata field associated with each Pinecone vector, and value is the filter applied on that field (see https://docs.pinecone.io/docs/metadata-filtering).

        Returns:
            namespace_results (dict): Key is namespace in the Pinecone index. Value is a list of Document objects.
        """
        namespace_results = defaultdict(list)
        for namespace, queries in namespace_queries.items():
            for query in queries:
                dense_vec = self.embeddings.embed_query(query)
                # query pinecone with the query parameters
                result = self.index.query(
                    vector=dense_vec,
                    top_k=self.top_k,
                    include_metadata=True,
                    namespace=namespace,
                    filter=metadata_filter
                )
                final_results = []
                for res in result["matches"]:
                    context = res["metadata"].pop("context")
                    final_results.append(
                        Document(page_content=context, metadata=res["metadata"])
                    )
                # return search results as json
                namespace_results[namespace].append(final_results)
        return namespace_results

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        raise NotImplementedError