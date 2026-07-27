from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any


class RichExtractionPort(ABC):
    """
    Represents a source-specific rich extraction that can be
    streamed sequentially to the chunker.
    """

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """
        Iterate through the extraction in natural reading order.
        """
        raise NotImplementedError
