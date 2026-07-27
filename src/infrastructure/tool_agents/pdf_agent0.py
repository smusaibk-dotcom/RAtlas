import io
import os

import fitz
import httpx
import pdfplumber
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from transformers import AutoTokenizer


class PDFAgent:
    """
    Tool for interacting with PDF documents.

    Performs deterministic operations only.
    All reasoning, planning and fallback decisions
    are handled by the KEE.
    """


class PDFAgent:
    def __init__(self):
        self._converter = DocumentConverter()

        self._tokenizer = AutoTokenizer.from_pretrained(
            os.getenv("EMBEDDING_MODEL"),
        )

        self._chunker = HybridChunker(
            tokenizer=self._tokenizer,
            merge_peers=False,
        )

    def run(
        self,
        pdf_path: str | Path,
    ):
        """
        Extract a PDF using Docling and return
        framework-generated chunks.
        """

        result = self._converter.convert(
            source=pdf_path,
        )

        document = result.document

        chunks = list(
            self._chunker.chunk(
                document,
            )
        )

        return chunks

    def _fetch_pdf(
        self,
        url: str,
    ) -> dict:
        try:
            response = httpx.get(
                url,
                headers={
                    "User-Agent": "Ratlas/1.0",
                },
                follow_redirects=True,
                timeout=30.0,
            )

            response.raise_for_status()

            return {
                "success": True,
                "content": response.content,
                "status_code": response.status_code,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": getattr(
                    getattr(e, "response", None),
                    "status_code",
                    None,
                ),
                "error": str(e),
            }

    def _extract_text(
        self,
        pdf: bytes,
    ) -> dict:
        try:
            document = fitz.open(
                stream=pdf,
                filetype="pdf",
            )

            pages = []

            full_text = ""

            character_offset = 0

            for page_number, page in enumerate(
                document,
                start=1,
            ):
                blocks = page.get_text(
                    "blocks",
                )

                page_blocks = []

                for block in blocks:
                    page_blocks.append(
                        {
                            "bbox": block[:4],
                            "text": block[4],
                        }
                    )

                text = ""

                for block in blocks:
                    text += block[4]

                pages.append(
                    {
                        "page": page_number,
                        "start_offset": character_offset,
                        "end_offset": character_offset + len(text),
                        "text": text,
                        "blocks": page_blocks,
                    }
                )

                full_text += text

                character_offset += len(text)

            document.close()

            return {
                "success": True,
                "content": {
                    "text": full_text,
                    "pages": pages,
                },
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": {
                    "text": "",
                    "pages": [],
                },
                "status_code": None,
                "error": str(e),
            }

    def _extract_tables(
        self,
        pdf: bytes,
    ) -> dict:
        try:
            tables = []

            with pdfplumber.open(
                io.BytesIO(pdf),
            ) as document:
                for page_number, page in enumerate(
                    document.pages,
                    start=1,
                ):
                    page_text = page.extract_text() or ""

                    extracted = page.extract_tables() or []

                    for table_index, table in enumerate(
                        extracted,
                        start=1,
                    ):
                        tables.append(
                            {
                                "id": f"table_{page_number}_{table_index}",
                                "page": page_number,
                                "bbox": None,
                                "caption": None,
                                "content": table,
                                "start_offset": 0,
                                "end_offset": len(page_text),
                            }
                        )

            return {
                "success": True,
                "content": tables,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": [],
                "status_code": None,
                "error": str(e),
            }

    def _extract_images(
        self,
        pdf: bytes,
    ) -> dict:
        try:
            document = fitz.open(
                stream=pdf,
                filetype="pdf",
            )

            images = []

            for page_number, page in enumerate(
                document,
                start=1,
            ):
                for image_index, image in enumerate(
                    page.get_images(full=True),
                    start=1,
                ):
                    xref = image[0]

                    images.append(
                        {
                            "id": f"image_{page_number}_{image_index}",
                            "page": page_number,
                            "xref": xref,
                            "bbox": None,
                            "caption": None,
                            "start_offset": 0,
                            "end_offset": len(page.get_text()),
                        }
                    )

            document.close()

            return {
                "success": True,
                "content": images,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": [],
                "status_code": None,
                "error": str(e),
            }

    def _extract_metadata(
        self,
        pdf: bytes,
    ) -> dict:
        try:
            document = fitz.open(
                stream=pdf,
                filetype="pdf",
            )

            metadata = document.metadata

            metadata["page_count"] = len(
                document,
            )

            document.close()

            return {
                "success": True,
                "content": metadata,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": {},
                "status_code": None,
                "error": str(e),
            }

    def cleanup(
        self,
    ) -> None:
        return
