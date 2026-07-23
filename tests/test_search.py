from application.dto.search_query import SearchQuery
from infrastructure.adapters.search_adapter import SearchAdapter


def main():
    adapter = SearchAdapter()

    query = SearchQuery(
        query="Evolution of Transformer models",
        priority=1,
        max_results=5,
    )

    result = adapter.search(query)

    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
