# 03_interrupts.py

## Overview

Human-in-the-loop approval workflow using `interrupt()` and `Command(resume=...)`.
This script contains a single concrete pattern: pause for approval, then route to proceed/cancel.

## State

```python
class ApprovalState(TypedDict):
    action_details: str
    status: Optional[Literal["pending", "approved", "rejected"]]
```

## Flow

```text
START -> approval -> (proceed or cancel) -> END
```

- `approval_node` calls `interrupt(...)` with question + details payload
- Human answer is resumed as boolean
- `route_after_approval` chooses:
  - `proceed` when approved
  - `cancel` when rejected

## Interrupt/Resume Pattern In This File

1. Invoke graph with an initial state and thread config
2. Read interrupt payload from `result["__interrupt__"][0].value`
3. Collect console input (`yes/no`)
4. Resume using `graph.invoke(Command(resume=approved), config)`
5. Print final status

## Key Functions

- `_build_approval_graph()`: compiles graph with `InMemorySaver`
- `demo_approval_workflow()`: runs an interactive terminal demo

## Usage

```bash
python 03_interrupts.py
```

The script prompts for approval and then prints the final routed status.
