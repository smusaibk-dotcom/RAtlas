from pathlib import Path

import fitz
from infrastructure.tool_agents.browser_agent import BrowserAgent


class PDFAgent:
    """
    PDF Agent

    Responsibilities

    1. Ask BrowserAgent to download the PDF.
    2. Split the PDF page-by-page.
    3. Return ordered page chunks.
    """

    def __init__(self):
        self._browser = BrowserAgent()

    def run(
        self,
        pdf_url: str,
    ) -> list[dict]:
        pdf_path: Path = self._browser.download_pdf(
            pdf_url,
        )

        document = fitz.open(
            pdf_path,
        )

        chunks = []

        for page_number in range(
            len(document),
        ):
            page = document.load_page(
                page_number,
            )

            chunks.append(
                {
                    "chunk_id": f"page_{page_number + 1}",
                    "page": page_number + 1,
                    "text": page.get_text(),
                }
            )

        document.close()

        return chunks
