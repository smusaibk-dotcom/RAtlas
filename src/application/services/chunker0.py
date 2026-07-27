import hashlib
import re

from application.dto.canonical_document import CanonicalDocument
from application.dto.chunk import Chunk


class Chunker:
    """
    Deterministic document chunker.
    """

    def chunk(
        self,
        document: CanonicalDocument,
    ) -> list[Chunk]:
        content = document.content

        text = content.get(
            "text",
            "",
        )

        pages = document.metadata.get(
            "pages",
            [],
        )

        sections = self._extract_sections(
            text,
        )

        chunks = []

        previous_chunk_id = None

        for section_title, section_text in sections:
            heading_path = [
                part.strip()
                for part in re.split(
                    r"\s*>\s*|\s*/\s*",
                    section_title,
                )
                if part.strip()
            ]

            heading_level = len(
                heading_path,
            )

            paragraphs = self._split_paragraphs(
                section_text,
            )

            paragraphs = self._merge_small_paragraphs(
                paragraphs,
            )

            paragraphs = self._split_large_paragraphs(
                paragraphs,
            )

            offsets = self._compute_character_offsets(
                section_text,
                paragraphs,
            )

            for paragraph, (
                char_start,
                char_end,
            ) in zip(
                paragraphs,
                offsets,
            ):
                chunk_id = hashlib.sha256(
                    (section_title + str(char_start) + str(char_end) + paragraph).encode(
                        "utf-8",
                    )
                ).hexdigest()

                page_start, page_end = self._map_pages(
                    pages,
                    char_start,
                    char_end,
                )

                chunk = Chunk(
                    chunk_id=chunk_id,
                    section_title=heading_path[-1],
                    section_level=heading_level,
                    parent_section=(heading_path[-2] if len(heading_path) > 1 else None),
                    heading_level=heading_level,
                    heading_path=heading_path,
                    subsection_title=(heading_path[-1] if len(heading_path) > 1 else None),
                    previous_chunk_id=previous_chunk_id,
                    page_start=page_start,
                    page_end=page_end,
                    char_start=char_start,
                    char_end=char_end,
                    text=paragraph,
                    tables=self._attach_nearby_artifacts(
                        document.content.get("tables", []),
                        char_start,
                        char_end,
                    ),
                    figures=self._attach_nearby_artifacts(
                        document.content.get("figures", []),
                        char_start,
                        char_end,
                    ),
                    equations=self._attach_nearby_artifacts(
                        document.content.get("equations", []),
                        char_start,
                        char_end,
                    ),
                    code_blocks=self._attach_nearby_artifacts(
                        document.content.get("code_blocks", []),
                        char_start,
                        char_end,
                    ),
                    images=self._attach_nearby_artifacts(
                        document.content.get("images", []),
                        char_start,
                        char_end,
                    ),
                    references=self._attach_nearby_artifacts(
                        document.content.get("references", []),
                        char_start,
                        char_end,
                    ),
                )
                if chunks:
                    chunks[-1].next_chunk_id = chunk_id

                chunks.append(
                    chunk,
                )

                previous_chunk_id = chunk_id

        chunks.sort(
            key=lambda chunk: (
                chunk.page_start if chunk.page_start is not None else float("inf"),
                chunk.char_start,
            )
        )

        for chunk in chunks:
            if chunk.parent_section and chunk.parent_section not in chunk.heading_path:
                chunk.parent_section = None

            if chunk.subsection_title == chunk.section_title and len(chunk.heading_path) == 1:
                chunk.subsection_title = None

        return self._validate_chunks(
            chunks,
        )

    def _extract_sections(
        self,
        text: str,
    ) -> list[tuple[str, str]]:
        """
        Detect document sections deterministically.
        """

        patterns = [
            # Markdown
            r"^(#{1,6}\s+.+)$",
            # HTML
            r"<h[1-6][^>]*>(.*?)</h[1-6]>",
            # Numbered headings
            r"^(\d+(?:\.\d+)*\.?\s+.+)$",
            # ALL CAPS headings
            r"^([A-Z][A-Z0-9\s\-\(\):]{3,})$",
        ]

        for pattern in patterns:
            matches = list(
                re.finditer(
                    pattern,
                    text,
                    flags=re.MULTILINE | re.IGNORECASE,
                )
            )

            if not matches:
                continue

            sections = []

            for index, match in enumerate(
                matches,
            ):
                title = re.sub(
                    r"<[^>]+>",
                    "",
                    match.group(1) if match.lastindex else match.group(),
                ).strip()

                if title.startswith("#"):
                    title = title.lstrip("#").strip()

                start = match.end()

                end = matches[index + 1].start() if index + 1 < len(matches) else len(text)

                sections.append(
                    (
                        title,
                        text[start:end].strip(),
                    )
                )

            if sections:
                return sections

        return [
            (
                "Document",
                text.strip(),
            )
        ]

    def _split_paragraphs(
        self,
        text: str,
    ) -> list[str]:
        return [
            paragraph.strip()
            for paragraph in text.split(
                "\n\n",
            )
            if paragraph.strip()
        ]

    def _merge_small_paragraphs(
        self,
        paragraphs: list[str],
        minimum_characters: int = 300,
    ) -> list[str]:
        merged = []

        buffer = ""

        for paragraph in paragraphs:
            if len(buffer) < minimum_characters:
                if buffer:
                    buffer += "\n\n"

                buffer += paragraph

            else:
                merged.append(
                    buffer.strip(),
                )

                buffer = paragraph

        if buffer:
            merged.append(
                buffer.strip(),
            )

        return merged

    def _split_large_paragraphs(
        self,
        paragraphs: list[str],
        maximum_characters: int = 1500,
    ) -> list[str]:
        """
        Split oversized paragraphs while preserving sentence boundaries.
        """

        result = []

        for paragraph in paragraphs:
            if len(paragraph) <= maximum_characters:
                result.append(
                    paragraph,
                )

                continue

            sentences = re.split(
                r"(?<=[.!?])\s+",
                paragraph,
            )

            buffer = ""

            for sentence in sentences:
                if len(buffer) + len(sentence) + 1 <= maximum_characters:
                    if buffer:
                        buffer += " "

                    buffer += sentence

                else:
                    if buffer:
                        result.append(
                            buffer.strip(),
                        )

                    buffer = sentence

            if buffer:
                result.append(
                    buffer.strip(),
                )

        return result

    def _compute_character_offsets(
        self,
        text: str,
        paragraphs: list[str],
    ) -> list[tuple[int, int]]:
        """
        Compute deterministic character offsets
        for each chunk.
        """

        offsets = []

        cursor = 0

        for paragraph in paragraphs:
            start = text.find(
                paragraph,
                cursor,
            )

            if start == -1:
                start = cursor

            end = start + len(
                paragraph,
            )

            offsets.append(
                (
                    start,
                    end,
                )
            )

            cursor = end

        return offsets

    def _map_pages(
        self,
        pages: list[dict],
        char_start: int,
        char_end: int,
    ) -> tuple[int | None, int | None]:
        """
        Map character offsets to page numbers.
        """

        page_start = None
        page_end = None

        for page in pages:
            if page_start is None and page["start_offset"] <= char_start <= page["end_offset"]:
                page_start = page["page"]

            if page_end is None and page["start_offset"] <= char_end <= page["end_offset"]:
                page_end = page["page"]

        return (
            page_start,
            page_end,
        )

    def _attach_nearby_artifacts(
        self,
        artifacts: list,
        char_start: int,
        char_end: int,
    ) -> list:
        """
        Return artifacts that overlap the chunk.

        For now, this is a placeholder until every tool
        provides deterministic offsets.
        """

        attached = []

        for artifact in artifacts:
            start = artifact.get(
                "start_offset",
            )

            end = artifact.get(
                "end_offset",
            )

            if start is None or end is None:
                continue

            if start <= char_end and end >= char_start:
                attached.append(
                    artifact,
                )

        return attached

    def _validate_chunks(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Final validation before handing chunks to the
        Knowledge DTO generator.
        """

        validated = []

        seen = set()

        for chunk in chunks:
            if not chunk.text.strip():
                continue

            if chunk.chunk_id in seen:
                continue

            seen.add(
                chunk.chunk_id,
            )

            validated.append(
                chunk,
            )

        return validated
