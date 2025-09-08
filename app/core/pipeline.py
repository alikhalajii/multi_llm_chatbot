from app.core.adapters import get_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


#  Define the workflow
workflow = StateGraph(state_schema=MessagesState)


def call_model(state: MessagesState):
    """Call the model with the current state messages."""
    model = config["configurable"]["model"]
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Default model config
model_id = get_chat_model("together", "llama_3_8b")
config = {
    "configurable": {
        "thread_id": "thread_123",
        "model": model_id
    }
}

# Prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Du sprichst wie ein höflicher Assistent. Antworte immer klar und kurz in der Sprache des Benutzers."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


def build_config(provider: str, model_key: str, thread_id="thread_123"):
    """Return a pipeline configuration with selected provider/model."""
    model_id = get_chat_model(provider, model_key)
    return {
        "configurable": {
            "thread_id": thread_id,
            "model": model_id
        }
    }
