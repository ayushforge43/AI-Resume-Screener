import os

from PyPDF2 import PdfReader

try:
    import docx  # python-docx
except ImportError:  # pragma: no cover
    docx = None


class ResumeParseError(Exception):
    """Raised when a resume file can't be read or has no extractable text."""
    pass


def _extract_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def _extract_docx(path):
    if docx is None:
        raise ResumeParseError(
            "DOCX support isn't installed on the server. Please upload a PDF instead."
        )
    document = docx.Document(path)
    return "\n".join(p.text for p in document.paragraphs if p.text)


def extract_text(path):
    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == ".pdf":
            text = _extract_pdf(path)
        elif ext in (".docx", ".doc"):
            text = _extract_docx(path)
        else:
            raise ResumeParseError(
                "Unsupported file type. Please upload a PDF or DOCX resume."
            )
    except ResumeParseError:
        raise
    except Exception:
        raise ResumeParseError(
            "Unable to extract text from this file. Please try another resume."
        )

    if not text or not text.strip():
        raise ResumeParseError(
            "Unable to extract text from this file. It may be a scanned image "
            "with no selectable text. Please try another resume."
        )

    return text
