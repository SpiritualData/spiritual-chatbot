"""Search in Pinecone using namespaces and metadata filters, and support multiple queries by namespace as part of a single retrieval call."""
from __future__ import annotations
import hashlib
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.embeddings.base import Embeddings
from langchain.schema import BaseRetriever, Document
# from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.chains import ConversationalRetrievalChain

import warnings
from abc import abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pydantic import Extra, Field, root_validator

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
    Callbacks,
)
from langchain.chains.base import Chain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts.base import BasePromptTemplate
from langchain.schema import BaseMessage, BaseRetriever, Document
from langchain.vectorstores.base import VectorStore

class PineconeMultiSearchRetriever(BaseRetriever, BaseModel):
    embeddings: Embeddings
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


class MultiSearchConversationalRetrievalChain(ConversationalRetrievalChain):
    """Chain for chatting with an index."""

    combine_docs_chain: BaseCombineDocumentsChain
    question_generator: LLMChain
    output_key: str = "answer"
    return_source_documents: bool = True
    return_generated_question: bool = True
    get_chat_history: Optional[Callable[[CHAT_TURN_TYPE], str]] = None
    """Return the source documents."""

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        question = inputs["question"]
        get_chat_history = self.get_chat_history or _get_chat_history
        chat_history_str = get_chat_history(inputs["chat_history"])

        if chat_history_str:
            callbacks = _run_manager.get_child()
            new_question = self.question_generator.run(
                question=question, chat_history=chat_history_str, callbacks=callbacks
            )
        else:
            new_question = question
        docs = self._get_docs(new_question, inputs)
        new_inputs = inputs.copy()
        new_inputs["question"] = new_question
        new_inputs["chat_history"] = chat_history_str
        answer = self.combine_docs_chain.run(
            input_documents=docs, callbacks=_run_manager.get_child(), **new_inputs
        )
        output: Dict[str, Any] = {self.output_key: answer}
        if self.return_source_documents:
            output["source_documents"] = docs
        if self.return_generated_question:
            output["generated_question"] = new_question
        return output
