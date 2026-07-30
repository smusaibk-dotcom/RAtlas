from dataclasses import dataclass
from enum import Enum


class ChunkRejectReason(str, Enum):
    EMPTY = "EMPTY"


@dataclass(slots=True)
class ChunkValidationResult:
    valid: bool
    reason: ChunkRejectReason | None = None


class ChunkValidator:
    def validate(
        self,
        text: str,
    ) -> ChunkValidationResult:

        text = text.strip()

        if self._is_empty(text):
            return ChunkValidationResult(
                valid=False,
                reason=ChunkRejectReason.EMPTY,
            )

        return ChunkValidationResult(
            valid=True,
        )

    def _is_empty(
        self,
        text: str,
    ) -> bool:
        return len(text) == 0