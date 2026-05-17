# LangGraph HITL — Phase 1

## What this is
A simple LangGraph StateGraph demonstrating interrupt and checkpoint mechanics.

## What it demonstrates
- interrupt() pausing a graph mid-execution
- SqliteSaver persisting state to disk
- Graph resuming from checkpoint after process kill

## How to run
pip3 install langgraph langgraph-checkpoint-sqlite
python3 graph.py.