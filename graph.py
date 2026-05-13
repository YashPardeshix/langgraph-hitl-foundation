from typing import TypedDict
from langgraph.types import interrupt

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