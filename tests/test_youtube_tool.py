import asyncio

from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.parse_chunk_tool import ParseChunkTool


async def main():
    parser = ParseChunkTool()

    resource = ResourceReference(
        id="yt-test",
        title="Attention Is All You Need",
        url="https://www.youtube.com/watch?v=iDulhoQ2pro",
        provider="youtube",
    )

    chunks = await parser.run(
        resource,
    )

    print(len(chunks))

    print("=" * 100)

    for i, chunk in enumerate(semantic_chunks):
        print("=" * 100)

        print(f"CHUNK #{i}")

        print("Heading :", chunk.content["heading"])

        print("Start   :", chunk.content["start_time"])

        print("End     :", chunk.content["end_time"])

        print(
            "Duration:",
            round(
                chunk.content["duration"],
                2,
            ),
        )

        print(
            "Words   :",
            len(
                chunk.content["text"].split(),
            ),
        )

        print()

        print(
            chunk.content["text"][:250],
        )

        print()


asyncio.run(main())
