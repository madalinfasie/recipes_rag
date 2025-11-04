import typing as t

from langchain_core.documents import Document
from langchain.chat_models import init_chat_model
from langgraph.graph import START, StateGraph

import db.qdrant as qdrant
from settings import Settings


llm = init_chat_model(Settings.MODEL_NAME, model_provider=Settings.MODEL_PROVIDER)

prompt = """You're a good chef and a great cook, use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Give details about what ingredients need to be used and what steps should be taken to create a recipe.

{context}
Question: {question}
Helpful Answer:

"""


class State(t.TypedDict):
    question: str
    context: list[Document]
    answer: str


def retrieve(state: State) -> State:
    retrieved_docs = qdrant.vector_store.similarity_search(state["question"])
    state["context"] = retrieved_docs
    return state


def generate(state: State) -> State:
    docs_content = "\n\n".join([doc.page_content for doc in state["context"]])
    messages = prompt.format(context=docs_content, question=state["question"])
    response = llm.invoke(messages)
    state["answer"] = str(response.content)
    return state


def build_graph():
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    return graph


def ask(question: str) -> str:
    new_state = graph.invoke({"question": question, "context": [], "answer": ""})
    return new_state["answer"]


graph = build_graph()
