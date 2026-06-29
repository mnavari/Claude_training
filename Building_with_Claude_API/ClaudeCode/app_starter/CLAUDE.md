# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
uv venv
source .venv/bin/activate
uv pip install -e .

# Run the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is an MCP (Model Context Protocol) server that exposes document-processing tools to AI assistants. It uses `FastMCP` from the `mcp` package.

- **`main.py`** — Creates the `FastMCP` server instance and registers tools via `mcp.tool()(function)`. All new tools must be imported here and registered this way.
- **`tools/`** — Each module defines tool functions as plain Python functions. Tools are not decorated in-place; they're registered in `main.py`.
- **`tools/document.py`** — Uses `markitdown` to convert binary documents (PDF, DOCX) to markdown text.
- **`tools/math.py`** — Example arithmetic tool showing the expected tool definition pattern.

## Defining MCP Tools

Tools are plain Python functions registered with `mcp.tool()(my_function)` in `main.py`.

**Parameter descriptions** use Pydantic `Field` as default values:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
```

**Docstrings** should follow this structure:
1. One-line summary
2. Detailed explanation of functionality
3. When to use (and not use) the tool
4. Usage examples with expected input/output

See `tools/math.py` for a complete example of this pattern.

## Code Style

- Always apply appropriate type annotations to function arguments and return types.
