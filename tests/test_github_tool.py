import asyncio

from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.parse_chunk_tool import ParseChunkTool


async def main():
    parser = ParseChunkTool()

    resource = ResourceReference(
        id="github-test",
        title="FastAPI",
        url="https://github.com/fastapi/fastapi",
        provider="test",
    )

    documents = await parser.run(resource)

    print(type(documents))
    print(len(documents))

    doc = documents[0]

    print("=" * 100)
    print(type(doc))
    print("=" * 100)

    print(dir(doc))

    print("=" * 100)
    print(doc)

    print("=" * 100)
    print(doc.text[:2000])

    print("=" * 100)
    print(doc.metadata)


asyncio.run(main())
