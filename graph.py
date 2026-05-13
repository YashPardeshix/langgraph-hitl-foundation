from typing import TypedDict
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

class MathState(TypedDict):
    input_number: float
    human_decision: str


def Multiply_node(state: MathState):
    old_number = state["input_number"]
    new_number = old_number * 2

    return {"input_number": new_number}

def Divide_node(state: MathState):
    old_number = state["input_number"]
    new_number = old_number / 2
    
    decision = interrupt(f"Is {new_number} correct?")

    return {
        "input_number": new_number,
        "human_decision": decision
    }


def Add_node(state: MathState):
    new_number = state["input_number"] + 10
    return {"input_number": new_number}

def should_continue(state: MathState):
    if state["human_decision"] == "yes":
        return "add"
    else:
        return END


conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

builder = StateGraph(MathState)
builder.add_node("multiply", Multiply_node)
builder.add_node("divide", Divide_node)
builder.add_node("add", Add_node)
builder.add_edge(START, "multiply")
builder.add_edge("multiply", "divide")
builder.add_conditional_edges("divide", should_continue)
builder.add_edge("add", END)
graph = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}
# print("--- Starting Graph ---")
# initial_input = {"input_number": 10}
# result = graph.invoke(initial_input, config)
# print(result)


print("--- Resuming Graph ---")
try:
    result = graph.invoke(Command(resume="yes"), config)
    print(result)
except Exception as e:
    print(f"Error: {e}")