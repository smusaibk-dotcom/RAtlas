import asyncio

from infrastructure.browser.browser_tool import BrowserAgent


async def main():
    browser = BrowserAgent()

    text = await browser.download_html(
        "https://www.drishtiias.com/daily-updates/daily-news-analysis/external-benchmarks-lending-rate"
    )

    print(text)


if __name__ == "__main__":
    asyncio.run(main())