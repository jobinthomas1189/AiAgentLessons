"""
Create Mermaid diagram images for each LangGraph lesson file.
Generates and stores .png images in the utils directory.
Run: python create_mermaid.py (from agentic_files or utils directory)

Note: PNG generation uses Mermaid.INK API and requires network access.
"""

import sys
from pathlib import Path

# Add parent to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
AGENTIC_DIR = SCRIPT_DIR.parent
LESSONS_DIR = AGENTIC_DIR.parent
MERMAID_DIR = LESSONS_DIR / "mermaids"
sys.path.insert(0, str(AGENTIC_DIR))

OUTPUT_DIR = SCRIPT_DIR  # Store .png files in utils/


def get_mermaid_for_graph(graph) -> str:
    """Extract mermaid string from a compiled LangGraph."""
    try:
        g = graph.get_graph()
        return g.draw_mermaid()
    except Exception as e:
        return f"%% Error generating mermaid: {e}\nflowchart TB\n  error[{str(e)}]"


def save_mermaid_png(graph, output_path: Path) -> bool:
    """Save graph as PNG image. Returns True on success. Requires network (Mermaid.INK API)."""
    try:
        g = graph.get_graph()
        png_bytes = g.draw_mermaid_png(max_retries=3, retry_delay=2)
        output_path.write_bytes(png_bytes)
        return True
    except Exception as e:
        print(f"    PNG error: {e}")
        return False


def build_and_save_mermaid(
    name: str, graph, output_dir: Path, print_mermaid: bool = False, save_png: bool = True
) -> tuple[str, bool]:
    """Save graph as .png image, return (mermaid_str, success)."""
    mermaid = get_mermaid_for_graph(graph)
    png_path = output_dir / f"{name}.png"
    png_ok = save_mermaid_png(graph, png_path) if save_png else False
    if print_mermaid:
        print(f"\n--- {name} ---\n{mermaid}\n")
    return mermaid, png_ok


def main():
    from typing import Annotated, Literal, Optional, NotRequired
    from typing_extensions import TypedDict
    from operator import add

    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.graph import StateGraph, START, END

    output_dir = Path(MERMAID_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_results = []



if __name__ == "__main__":
    main()
