from application.dto.chunk import Chunk


class Chunker:
    """
    Splits a rich extraction into deterministic,
    self-contained chunks.
    """

    def __init__(
        self,
        target_tokens: int = 1500,
        hard_limit: int = 1800,
    ) -> None:
        self._target_tokens = target_tokens
        self._hard_limit = hard_limit

    def chunk(
        self,
        extraction,
    ) -> list[Chunk]:
        raise NotImplementedError
