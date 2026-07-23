def router(
    self,
    state: KEEState,
) -> str:
    """
    Decide the next node based on the
    agent's latest reasoning.
    """

    observation = state["current_observation"]

    if observation is None:
        raise ValueError("The reason node did not produce an observation.")

    action = observation.get(
        "action",
    )

    if action == "tool":
        return "tool"

    if action == "chunk":
        return "chunk"

    if action == "knowledge_package":
        return "knowledge_package"

    if action == "evolution_feed":
        return "evolution_feed"

    if action == "finish":
        return "evolution_feed"

    raise ValueError(f"Unknown action received from the agent: {action}")
