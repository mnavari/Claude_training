from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_content",
    description="Read the content of a document given its ID.",
    )
def read_document(
    doc_id: str = Field(description="ID of the document to read")):
    if doc_id not in docs:
        return f"Document with ID '{doc_id}' not found."
    return docs[doc_id]


@mcp.tool(
    name="edit_doc_content",
    description="Edit the content of a document given its ID and new content.",
    )
def edit_document(
    doc_id: str = Field(description="ID of the document to edit"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace and punctuation."),
    new_str: str = Field(description="The new text to replace the old text with.")):
    if doc_id not in docs:
        return f"Document with ID '{doc_id}' not found."
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Document '{doc_id}' updated successfully."


# TODO: Write a resource to return all doc id's
@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource("docs://documents/{doc_id}",mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrite a document in markdown format.",
)
def format_document(
    doc_id: str=Field(description="ID of the document to format")
    ) -> list[base.Message]:
    prompt = f"""
    Your goal is to rewrite the content of the document with ID '{doc_id}' in markdown syntax.  

    Add in headers, bullet points, tables, numbered lists, or any other markdown formatting that 
    would make the document easier to read and understand. Feel free to reorganize and edit
    (using the 'edit_document' tool) the content as needed to improve clarity and flow."""
    return [base.UserMessage(prompt)]  

    # TODO: Implement markdown formatting logic
    pass

if __name__ == "__main__":
    mcp.run(transport="stdio")