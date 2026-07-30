import logging
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import fitz
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)

from application.dto.resource_reference import ResourceReference
from infrastructure.browser.browser_tool import BrowserAgent
from infrastructure.parsers.chunk_wrapper import ChunkWrapper
from infrastructure.parsers.resource_router import ResourceRouter
from infrastructure.parsers.youtube_chunker import YoutubeChunker
from infrastructure.parsers.page_validator import PageValidator



logging.getLogger("docling").setLevel(logging.ERROR)


class ParseChunkTool:
    """
    Responsible for:

    1. Routing resources.
    2. Calling BrowserAgent if required.
    3. Dispatching to Docling/LlamaIndex.
    4. Returning RatlasChunks.
    """

    def __init__(self):
        self._router = ResourceRouter()

        self._browser = BrowserAgent()

        self._wrapper = ChunkWrapper()

        self._youtube_chunker = YoutubeChunker()

        pdf_pipeline_no_ocr = PdfPipelineOptions()
        pdf_pipeline_no_ocr.do_ocr = False
        self._converter_no_ocr = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pdf_pipeline_no_ocr,
                ),
            },
        )
        pdf_pipeline_with_ocr = PdfPipelineOptions()
        pdf_pipeline_with_ocr.do_ocr = True
        self._converter_with_ocr = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pdf_pipeline_with_ocr,
                ),
            },
        )
        self._ocr_pipeline_options = PdfPipelineOptions()
        self._ocr_pipeline_options.do_ocr = True
        self._converter_ocr = DocumentConverter(
            format_options={
                InputFormat.IMAGE: PdfFormatOption(
                    pipeline_options=self._ocr_pipeline_options,
                ),
            },
        )

    async def run(
        self,
        resource: ResourceReference,
    ):
        resource_type = self._router.route(
            resource,
        )

        match resource_type:
            case "pdf":
                return await self._parse_pdf(
                    resource,
                )

            case "html":
                return await self._parse_html(
                    resource,
                )

            case "document":
                return await self._parse_document(
                    resource,
                )

            case "image":
                return await self._parse_image(
                    resource,
                )

            case "github":
                return await self._parse_github(
                    resource,
                )

            case "youtube":
                return await self._parse_youtube(
                    resource,
                )

            case _:
                raise ValueError(f"Unsupported resource type: {resource_type}")

    async def _parse_pdf(
        self,
        resource: ResourceReference,
    ):
        pdf_path = await self._browser.download_pdf(
            resource.url,
        )

        with fitz.open(pdf_path) as pdf:
            has_text_layer = any(page.get_text("text").strip() for page in pdf)

        converter = self._converter_no_ocr if has_text_layer else self._converter_with_ocr

        result = converter.convert(
            source=pdf_path,
        )

        return self._wrapper.wrap(
            result.document,
            resource,
            "pdf",
        )

    async def _parse_html(
        self,
        resource: ResourceReference,
    ):
        html = await self._browser.download_html(resource.url)

        PageValidator.validate(html)

        with tempfile.NamedTemporaryFile(
            suffix=".html",
            delete=False,
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(html)
            temp_path = Path(f.name)

        try:
            result = self._converter_no_ocr.convert(
                source=temp_path,
            )

            return self._wrapper.wrap(
                result.document,
                resource,
                "html",
            )

        finally:
            temp_path.unlink(
                missing_ok=True,
            )

    async def _parse_document(
        self,
        resource: ResourceReference,
    ):
        file_path = await self._browser.download_file(
            resource.url,
        )

        result = self._converter_no_ocr.convert(
            source=file_path,
        )

        return self._wrapper.wrap(
            result.document,
            resource,
            "document",
        )

    async def _parse_image(
        self,
        resource: ResourceReference,
    ):
        try:
            result = self._converter_ocr.convert(
                source=resource.url,
            )

            return self._wrapper.wrap(
                result.document,
                resource,
                "image",
            )

        except Exception:
            image_path = await self._browser.download_file(
                resource.url,
            )

            result = self._converter_ocr.convert(
                source=image_path,
            )

            return self._wrapper.wrap(
                result.document,
                resource,
                "image",
            )

    async def _parse_github(
        self,
        resource: ResourceReference,
    ):
        path = urlparse(resource.url).path.strip("/").split("/")

        owner = path[0]
        repo = path[1]

        documents = await self._browser.fetch_github_documents(
            owner=owner,
            repo=repo,
        )

        return documents

    async def _parse_youtube(
        self,
        resource: ResourceReference,
    ):
        transcript = await self._browser.fetch_youtube_documents(
            resource.url,
        )

        semantic_chunks = self._youtube_chunker.wrap(
            transcript,
            resource,
        )

        return self._wrapper.wrap(
            resource=resource,
            resource_type="youtube",
            semantic_chunks=semantic_chunks,
        )
