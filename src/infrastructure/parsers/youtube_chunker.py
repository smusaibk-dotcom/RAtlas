from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.text_cleaner import TextCleaner


class YoutubeChunker:
    def __init__(
        self,
    ):
        self._cleaner = TextCleaner()

    def wrap(
        self,
        transcript,
        resource: ResourceReference,
    ) -> list[dict]:
        semantic_chunks = []

        current_text = []
        current_start = None
        current_end = None
        word_count = 0

        MAX_DURATION = 120
        MAX_WORDS = 350

        for snippet in transcript:
            snippet_text = snippet.text.strip()

            snippet_start = snippet.start

            snippet_end = snippet.start + snippet.duration

            snippet_words = len(snippet_text.split())

            if current_start is None:
                current_start = snippet_start

            if current_text and (
                (snippet_end - current_start) > MAX_DURATION
                or (word_count + snippet_words) > MAX_WORDS
            ):
                paragraph = self._cleaner.clean(" ".join(current_text))

                semantic_chunks.append(
                    {
                        "heading": resource.title,
                        "text": paragraph,
                        "start_time": current_start,
                        "end_time": current_end,
                        "duration": current_end - current_start,
                    }
                )

                current_text = []
                word_count = 0

                current_start = snippet_start
                current_end = None

            current_text.append(
                snippet_text,
            )

            word_count += snippet_words

            current_end = snippet_end

        if current_text:
            paragraph = self._cleaner.clean(" ".join(current_text))

            semantic_chunks.append(
                {
                    "heading": resource.title,
                    "text": paragraph,
                    "start_time": current_start,
                    "end_time": current_end,
                    "duration": current_end - current_start,
                }
            )

        return semantic_chunks
