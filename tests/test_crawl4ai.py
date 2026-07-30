import asyncio

from crawl4ai import AsyncWebCrawler


async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.britannica.com/science/artificial-intelligence",
        )

        print("=" * 100)

        print("HTML available:", hasattr(result, "html"))
        print("Cleaned HTML:", hasattr(result, "cleaned_html"))
        print("Fit HTML:", hasattr(result, "fit_html"))

        print("=" * 100)

        if hasattr(result, "html"):
            print(result.html[:500])

        print("=" * 100)

        if hasattr(result, "cleaned_html"):
            print(result.cleaned_html[:500])

        print("=" * 100)

        if hasattr(result, "fit_html"):
            print(result.fit_html[:500])
        print(result.__dict__.keys())


asyncio.run(main())
