from application.agents.kee.states import KEEState


def build_kee_user_prompt(
    state: KEEState,
    tools: list[str],
) -> str:
    return f"""
Research Goal
-------------
{state["goal"]}

Available Resources
-------------------
{state["resources"]}

Working Memory
--------------
{state["memory"]}

Knowledge Packages
------------------
{state["knowledge_packages"]}

Current Resource
----------------
{state["current_resource"]}

Current Observation
-------------------
{state["current_observation"]}

Available Tools
---------------
{tools}

Determine the single best next action.

Return ONLY a valid JSON object in the following format:

{{
    "action": "",
    "tool": "",
    "capability": "",
    "arguments": {{}}
}}
"""
