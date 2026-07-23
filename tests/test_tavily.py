from infrastructure.clients.tavily_client import TavilyClient


def main():
    client = TavilyClient()

    response = client.search(
        query="Evolution of Transformer models",
        max_results=3,
    )

    print(response)


if __name__ == "__main__":
    main()
