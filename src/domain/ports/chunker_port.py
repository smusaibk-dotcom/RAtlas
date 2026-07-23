from abc import ABC, abstractmethod

from application.dto.chunk import Chunk


class ChunkerPort(ABC):
    """
    Splits a rich extraction into deterministic,
    self-contained chunks.
    """

    @abstractmethod
    def chunk(
        self,
        extraction,
    ) -> list[Chunk]:
        """
        Split one rich extraction into multiple chunks.

        The chunker must:

        - preserve reading order
        - preserve related artifacts
        - respect the configured token budget
        - produce deterministic chunks
        """
        raise NotImplementedError
