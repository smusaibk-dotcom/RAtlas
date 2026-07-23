from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.conversation_state import ConversationState


class ConversationStatePort(ABC):
    @abstractmethod
    def create(self) -> ConversationState:
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        conversation_id: UUID,
    ) -> ConversationState:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        state: ConversationState,
    ) -> None:
        raise NotImplementedError
