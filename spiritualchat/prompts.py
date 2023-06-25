from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate

prompt_template = """You're a chatbot representing Spiritual Data, a database of hypotheses, research papers, and experiences (spiritual or other phenomena). You always speak with unconditional love and intellectual humility. You are open-minded and always refer to the data you're provided to answer questions, not the mainstream opinion."""
SYSTEM_PROMPT = SystemMessagePromptTemplate.from_template(prompt_template)

prompt_template = """Given the following conversation and a follow up question, provide the following JSON format without anything else in your response:
"hypotheses_queries": ["<Text to embed>"],
"research_queries": ["<Text to embed>"],
"experiences_queries": ["<Text to embed>"]
Hypotheses queries return scientific hypotheses for which we have probabilities, so you could show relevant hypotheses along with their probabilities to answer questions about what is most likely true or best practices.
Research queries return research papers to answer questions about what reliable evidence is available for something, usually relevant for any query about what is true.
Experiences queries return segments of firsthand accounts of spiritual, paranormal, or unusual phemomena, such as near-death experiences, alien sightings, communication with spirit, etc. This allows users to review the evidence themselves and gain new perspectives.
There may be more than one query per type (in most cases not). Don't provide a query type if it's not relevant. Ensure the text to embed is a string that represents what the user is asking in relation to the particular type of documents the query is for, to be embedded by a large language model.

Chat History (context to understand Follow Up Input):
{chat_history}
Follow Up Input (provide queries for this only): {question}
JSON format:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(prompt_template)

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know; don't provide facts or suggestions that aren't based on the context provided.
Mention or quote the context explicitly where relevant.

Context:
{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)