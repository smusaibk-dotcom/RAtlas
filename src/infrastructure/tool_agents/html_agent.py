from crawl4ai import AsyncWebCrawler


class HTMLAgent:
    """
    HTML Agent

    Responsibilities

    1. Crawl webpage.
    2. Extract rich content.
    3. Return Crawl4AI extraction.
    """

    async def run(
        self,
        url: str,
    ):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
            )

        return {
            "url": url,
            "success": result.success,
            "title": result.metadata.get("title"),
            "markdown": result.markdown,
            "html": result.cleaned_html,
            "links": result.links,
            "media": result.media,
            "metadata": result.metadata,
        }
