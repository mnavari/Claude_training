import os
import tempfile

import pytest

from tools.document import document_path_to_markdown


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")


class TestHappyPath:
    def test_converts_pdf_to_markdown(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_converts_docx_to_markdown(self):
        result = document_path_to_markdown(DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_pdf_contains_expected_content(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        assert "MCP" in result or "mcp" in result.lower()

    def test_docx_contains_expected_content(self):
        result = document_path_to_markdown(DOCX_FIXTURE)
        assert "MCP" in result or "mcp" in result.lower()

    def test_pdf_preserves_markdown_structure(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        has_structure = "#" in result or "-" in result or "*" in result
        assert has_structure

    def test_docx_preserves_markdown_structure(self):
        result = document_path_to_markdown(DOCX_FIXTURE)
        has_structure = "#" in result or "-" in result or "*" in result
        assert has_structure


class TestFileReadingErrors:
    def test_file_not_found_raises_error(self):
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown("/nonexistent/path/file.pdf")

    def test_directory_path_raises_error(self):
        with pytest.raises(IsADirectoryError):
            document_path_to_markdown(FIXTURES_DIR)

    def test_empty_file_handles_gracefully(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"")
            tmp_path = f.name
        try:
            with pytest.raises(Exception):
                document_path_to_markdown(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_no_read_permission_raises_error(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-1.4 fake content")
            tmp_path = f.name
        try:
            os.chmod(tmp_path, 0o000)
            with pytest.raises(PermissionError):
                document_path_to_markdown(tmp_path)
        finally:
            os.chmod(tmp_path, 0o644)
            os.unlink(tmp_path)


class TestFileTypeValidation:
    def test_unsupported_extension_raises_error(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"plain text")
            tmp_path = f.name
        try:
            with pytest.raises(ValueError, match="Unsupported file type"):
                document_path_to_markdown(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_image_extension_raises_error(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\xff\xd8\xff\xe0")
            tmp_path = f.name
        try:
            with pytest.raises(ValueError, match="Unsupported file type"):
                document_path_to_markdown(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_no_extension_raises_error(self):
        with tempfile.NamedTemporaryFile(suffix="", delete=False) as f:
            f.write(b"some content")
            tmp_path = f.name
        try:
            with pytest.raises(ValueError, match="no extension"):
                document_path_to_markdown(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_wrong_content_for_extension_returns_empty_or_garbage(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"this is not a real PDF")
            tmp_path = f.name
        try:
            result = document_path_to_markdown(tmp_path)
            assert isinstance(result, str)
            assert "MCP" not in result
        finally:
            os.unlink(tmp_path)


class TestReturnValue:
    def test_returns_string_for_pdf(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        assert type(result) is str

    def test_returns_string_for_docx(self):
        result = document_path_to_markdown(DOCX_FIXTURE)
        assert type(result) is str

    def test_result_is_not_binary(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        assert isinstance(result, str)
        result.encode("utf-8")
