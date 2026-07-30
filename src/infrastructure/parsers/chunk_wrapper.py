import hashlib

from application.dto.chunk import Chunk
from infrastructure.parsers.document_chunker import DocumentChunker
from infrastructure.parsers.text_cleaner import TextCleaner
from application.chunk_validation.chunk_validator import ChunkValidator


class ChunkWrapper:
    def __init__(self):
        self._chunker = DocumentChunker()
        self._cleaner = TextCleaner()
        self._validator = ChunkValidator()

    def wrap(
        self,
        document=None,
        resource=None,
        resource_type=None,
        semantic_chunks=None,
    ) -> list[Chunk]:
        if semantic_chunks is not None:
            chunks = []

            for chunk_index, content in enumerate(semantic_chunks):
                if content.get("heading") in self._cleaner.NOISE_HEADINGS:
                    continue
                text = self._cleaner.clean(
                    content["text"],
                )

                content["text"] = text

                chunks.append(
                    Chunk(
                        chunk_id=hashlib.sha256(
                            (resource.url + str(chunk_index) + text).encode("utf-8")
                        ).hexdigest(),
                        resource_type=resource_type,
                        resource_id=resource.id
                        or hashlib.sha256(resource.url.encode("utf-8")).hexdigest(),
                        chunk_index=chunk_index,
                        content=content,
                        metadata={},
                    )
                )

            return chunks

        semantic_chunks = self._chunker.chunk(
            document,
        )

        chunks = []

        for chunk_index, semantic_chunk in enumerate(semantic_chunks):
            content = None
            if semantic_chunk.get("type") == "picture":
                text = semantic_chunk.get(
                    "caption",
                    "",
                )

                content = {
                    "heading": semantic_chunk.get(
                        "heading",
                        "",
                    ),
                    "text": text,
                    "picture": semantic_chunk.get(
                        "picture",
                    ),
                }

            elif semantic_chunk.get("type") == "table":
                table = semantic_chunk["table"]

                if hasattr(
                    table,
                    "export_to_markdown",
                ):
                    text = table.export_to_markdown(
                        document,
                    )

                    content = {
                        "heading": semantic_chunk.get(
                            "heading",
                            "",
                        ),
                        "text": text,
                        "table": table,
                    }

                else:
                    text = str(table)

                    content = {
                        "heading": semantic_chunk.get(
                            "heading",
                            "",
                        ),
                        "text": text,
                        "table": table,
                    }

            else:
                text = semantic_chunk["text"]

                content = {
                    "heading": semantic_chunk.get(
                        "heading",
                        "",
                    ),
                    "text": text,
                }
            if content.get("heading") in self._cleaner.NOISE_HEADINGS:
                continue
            text = self._cleaner.clean(
                text,
            )

            result = self._validator.validate(text)

            if not result.valid:
                continue

            content["text"] = text

            chunks.append(
                Chunk(
                    chunk_id=hashlib.sha256(
                        (resource.url + str(chunk_index) + text).encode("utf-8")
                    ).hexdigest(),
                    resource_type=resource_type,
                    resource_id=resource.id,
                    chunk_index=chunk_index,
                    content=content,
                    metadata={},
                )
            )

        return chunks
