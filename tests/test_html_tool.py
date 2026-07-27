import asyncio

from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.parse_chunk_tool import ParseChunkTool

# ===========================
# CHANGE ONLY THIS RESOURCE
# ===========================

# resource = ResourceReference(
# "Israel Conflict Timeline",
# url="https://www.ajc.org/IsraelConflictTimeline",
# provider="test",
# )

# PDF
# resource = ResourceReference(
#   title="Attention Is All You Need",
#   url="https://arxiv.org/pdf/1706.03762.pdf",
#   provider="test",)

# IMAGE
# resource = ResourceReference(
#  title="Dog",
#  url="https://images.unsplash.com/photo-1517841905240-472988babdf9",
#  provider="test",
# )

# YOUTUBE
# resource = ResourceReference(
#     title="Attention Is All You Need",
#     url="https://www.youtube.com/watch?v=iDulhoQ2pro",
#     provider="test",
# )

resource = ResourceReference(
    title="Britannica",
    url="https://www.britannica.com/topic/Palestinian-statehood",
    provider="test",
)


async def main():
    parser = ParseChunkTool()

    resource1 = ResourceReference(
        title="Wikipedia",
        url="https://en.wikipedia.org/wiki/History_of_Palestinian_statehood",
        provider="test",
    )

    resource2 = ResourceReference(
        title="CFR",
        url="https://education.cfr.org/learn/timeline/israeli-palestinian-conflict-timeline",
        provider="test",
    )

    chunks1 = await parser.run(resource1)
    chunks2 = await parser.run(resource2)

    print(f"Wikipedia: {len(chunks1)} chunks")
    print(f"CFR      : {len(chunks2)} chunks")

    all_chunks = []

    all_chunks.extend(chunks1)
    print("After Wikipedia:", len(all_chunks))

    all_chunks.extend(chunks2)
    print("After CFR:", len(all_chunks))


asyncio.run(main())
