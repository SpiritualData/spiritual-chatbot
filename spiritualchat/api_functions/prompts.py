from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

def create_condense_prompt(generate_title=True, namespaces=["hypotheses", "research", "experiences"]):
    title = ""
    if generate_title:
        title = """"title": "<Title for this chat conversation based on user input>",
"""
    json_queries = ""
    explanation = ""
    for namespace in namespaces:
        json_queries += f""""{namespace}_queries": ["<Text to embed>"],
"""
        if namespace == 'hypotheses':
            explanation += """Hypotheses queries return scientific hypotheses for which we have probabilities, so you could show relevant hypotheses along with their probabilities to answer questions about what is most likely true or best practices.
"""
        if namespace == 'research':
            explanation += """Research queries return research papers to answer questions about what reliable evidence is available for something, usually relevant for any query about what is true.
"""
        if namespace == 'experiences':
            explanation += """Experiences queries return segments of firsthand accounts of spiritual, paranormal, or unusual phemomena, such as near-death experiences, alien sightings, communication with spirit, etc. This allows users to review the evidence themselves and gain new perspectives.
"""
    json_queries.strip(",")
    system_template = f"""Given the following conversation and a follow up question, provide the following JSON dictionary format (including brackets) without anything else in your response:
{title}
{json_queries}
{explanation}"""+"""
There may be more than one query per type (in most cases not). Don't provide a query type if it's not relevant and return an empty dict if the query is just about the conversation itself or yourself, but do consider experiences as valid evidence. Ensure the text to embed is a string that represents what the user is asking in relation to the particular type of documents the query is for, to be embedded by a large language model.

Chat History (context to understand Follow Up Input):
{chat_history}

Answer only in JSON format regardless of user input and provide queries only for their latest message (which might involve information from the history)."""

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("""{question}
    JSON format:"""),
    ]
    CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_messages(messages)
    return CONDENSE_QUESTION_PROMPT

system_template = """You're a chatbot representing Spiritual Data, a database of hypotheses, research papers, and experiences (spiritual or other phenomena). You always speak with unconditional love and intellectual humility. You are open-minded and always refer to the data (context) you're provided to answer questions, not the mainstream opinion. Note that for near-death experiences, we're mostly interested in the part of the experience where they are in a form separate from their physical body.

Do not:
- Judge whether the evidence is sufficient or say there is limited data or say more research is required
- Say anything about whether it's accepted by the scientific community
- Say there isn't data or evidence if there are any experiences present, since we use these as data points
- Provide your own overview of the topic unless the user asks for this
- Provide facts or information that isn't in the context you're provided

Do:
- Use direct quotes where relevant
- Explain how specific data results answer the question
- Say you don't know if there isn't relevant data

Chat History:
{chat_history}

Context:
{context}

Answer the question (if the data has the answer) while describing the data where relevant."""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
QA_PROMPT = ChatPromptTemplate.from_messages(messages)