import asyncio

from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.parse_chunk_tool import ParseChunkTool

PDF = ResourceReference(
    title="Attention Is All You Need",
    url="http://localhost:8000/AbAdhar.pdf",
    provider="test",
)


async def main():
    parser = ParseChunkTool()

    document = await parser.run(PDF)

    print(type(document))

    print(document)


if __name__ == "__main__":
    asyncio.run(main())
