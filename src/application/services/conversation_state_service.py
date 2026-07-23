from uuid import UUID

from application.dto.conversation_state import ConversationState
from domain.ports.conversation_state_port import ConversationStatePort


class ConversationStateService:
    def __init__(
        self,
        port: ConversationStatePort,
    ) -> None:
        self._port = port

    def create(self) -> ConversationState:
        return self._port.create()

    def load(
        self,
        conversation_id: UUID,
    ) -> ConversationState:
        return self._port.load(conversation_id)

    def save(
        self,
        state: ConversationState,
    ) -> None:
        self._port.save(state)
