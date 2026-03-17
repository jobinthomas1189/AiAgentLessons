# 03_interrupts.py

## Overview

LangGraph Interrupts — Human-in-the-loop workflows. Pause execution, wait for external input, then resume with `Command(resume=...)`.

**Source:** [LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

## Purpose

- Use `interrupt()` to pause and wait for human input
- Use `Command(resume=...)` to resume with the human's response
- Demonstrate approval workflows, review-and-edit, and multiple parallel interrupts

## Key Concepts

### `interrupt(payload)`

Pauses the graph and returns control. The graph returns `{"__interrupt__": [...]}`. Resume with `graph.invoke(Command(resume=value), config)`.

### `Command(goto=...)` or `Command(resume=...)`

- `goto` — Route to a specific node
- `resume` — Value passed back to the node that called `interrupt()`

## Demos

### 1. Approval Workflow

- **State:** `action_details`, `status`
- **Flow:** `approval` → (interrupt) → `proceed` or `cancel`
- **Interrupt payload:** `{"question": "Approve this action?", "details": ...}`
- **Resume:** `True` → proceed, `False` → cancel

### 2. Review and Edit

- **State:** `generated_text`
- **Flow:** `review` (interrupt) → human edits content → resume with updated text
- **Interrupt payload:** `{"instruction": "Review and edit", "content": ...}`

### 3. Multiple Interrupts (Parallel Branches)

- **State:** `vals` (list, reducer)
- **Flow:** Parallel nodes `a` and `b` both call `interrupt()` with different questions
- **Resume:** Map by interrupt ID when multiple interrupts exist

## Helper: `run_with_human_input()`

Runs the graph in a loop: on `__interrupt__`, prompts the user for input, then invokes `Command(resume=...)` until the graph completes.

## Requirements

- `InMemorySaver` (checkpointer) — required for interrupts
- `thread_id` in config — persistent pointer for checkpointing

## Usage

```bash
python 03_interrupts.py
```

Prompts for human input when interrupts fire.
