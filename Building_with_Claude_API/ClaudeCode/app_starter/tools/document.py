import os

from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: str = Field(description="Path to a PDF or DOCX file to convert to markdown"),
) -> str:
    """Read a PDF or DOCX file from disk and convert its contents to markdown.

    Takes a file path, validates the extension, reads the binary content,
    and returns the document converted to markdown text.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if os.path.isdir(path):
        raise IsADirectoryError(f"Path is a directory, not a file: {path}")

    ext = os.path.splitext(path)[1].lower()
    if not ext:
        raise ValueError(f"File has no extension: {path}")
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported types: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    with open(path, "rb") as f:
        binary_data = f.read()

    file_type = ext.lstrip(".")
    return binary_document_to_markdown(binary_data, file_type)
