from application.agents.kee.states import KEEState


def build_kee_canonical_document_user_prompt(
    state: KEEState,
    raw_content,
    raw_metadata,
) -> str:
    return f"""
Current Resource
----------------
{state["current_resource"]}

Raw Extracted Content
---------------------
{raw_content}

Raw Metadata
------------
{raw_metadata}

Normalize the extracted knowledge into a CanonicalDocument.

Return ONLY a valid JSON object in the following format:

{{
    "title": "",
    "content": {{
        "text": "",
        "tables": [],
        "figures": [],
        "equations": [],
        "images": [],
        "code_blocks": [],
        "references": [],
        "links": []
    }},
    "metadata": {{}}
}}

Do NOT generate:
- resource_id
- source_url
- source_type
Rules:
- Preserve every extracted artifact.
- Do not discard tables, figures, equations, images, code blocks, references or links.
- If an artifact exists in the extracted content, copy it into the corresponding field.
- Do not summarize, merge, or remove any extracted artifact.
- Normalize only the document structure, title and metadata.
- Preserve all available fields inside each artifact object (id, page, caption, bbox, xref, start_offset, end_offset, etc.).
"""
