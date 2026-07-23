from uuid import UUID, uuid4

from application.dto.conversation_state import ConversationState
from domain.ports.conversation_state_port import ConversationStatePort


class ConversationStateAdapter(ConversationStatePort):
    _storage: dict[UUID, ConversationState] = {}

    def create(self) -> ConversationState:
        state = ConversationState(
            conversation_id=uuid4(),
        )

        self._storage[state.conversation_id] = state

        return state

    def load(
        self,
        conversation_id: UUID,
    ) -> ConversationState:
        return self._storage[conversation_id]

    def save(
        self,
        state: ConversationState,
    ) -> None:
        self._storage[state.conversation_id] = state
