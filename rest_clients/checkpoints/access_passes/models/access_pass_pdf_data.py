"""Generated model: AccessPassPDFData."""

from pydantic import BaseModel


class AccessPassPDFData(BaseModel):
    html_body: str
    agreed_document_id: int
    title: str
