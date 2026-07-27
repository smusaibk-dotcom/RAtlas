import asyncio

from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.parse_chunk_tool import ParseChunkTool


async def main():
    parser = ParseChunkTool()

    resource = ResourceReference(
        id="pdf-test",
        title="Dummy PDF",
        url="http://localhost:8000/dummy_tables_test.pdf",
        provider="test",
    )

    result = await parser.run(resource)

    print(f"\nTotal Chunks : {len(result)}")

    print("\n" + "=" * 100)
    print("TABLE CHUNKS")
    print("=" * 100)

    table_count = 0

    for chunk in result:
        if "table" in chunk.content:
            table_count += 1

            print("\n" + "=" * 80)
            print(f"TABLE #{table_count}")
            print("=" * 80)

            print("Heading:")
            print(chunk.content["heading"])

            print("\nContent Keys:")
            print(chunk.content.keys())

            print("\nTable Type:")
            print(type(chunk.content["table"]))

            print("\nPreview:")
            print(str(chunk.content["table"])[:500])

    print("\n" + "=" * 100)
    print(f"TOTAL TABLES FOUND : {table_count}")
    print("=" * 100)


asyncio.run(main())
