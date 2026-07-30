from application.dto.chunk import Chunk


def build_candidate_discovery_user_prompt(
    chunk: Chunk,
) -> str:
    heading = ""

    if isinstance(chunk.content, dict):
        heading = chunk.content.get("heading", "")

    text = chunk.content.get("text", "") if isinstance(chunk.content, dict) else str(chunk.content)

    return f"""
Chunk ID
--------
{chunk.chunk_id}

Resource Type
-------------
{chunk.resource_type}

Chunk Index
-----------
{chunk.chunk_index}

Heading
-------
{heading}

Chunk
-----
{text}

------------------------------------------------------------
TASK
------------------------------------------------------------

Identify every possible candidate explicitly mentioned in the chunk.

Return ONLY valid JSON in the following format:

{{
    "candidates": [
        {{
            "text": "",
            "candidate_type": "",
            "evidence": ""
        }}
    ]
}}

Remember:

- Every candidate must be supported by the chunk.
- Preserve the original wording whenever possible.
- Evidence must be copied directly from the chunk.
- Do not explain your reasoning.
- Do not output markdown.
- Do not output code fences.
- Return ONLY the JSON object.
"""
