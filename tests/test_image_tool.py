import asyncio

from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.parse_chunk_tool import ParseChunkTool


async def main():
    parser = ParseChunkTool()

    resource = ResourceReference(
        title="Ratlas",
        url="https://www.python.org/static/community_logos/python-logo.png",
        provider="test",
    )

    result = await parser.run(resource)

    print(result.export_to_markdown())


asyncio.run(main())
