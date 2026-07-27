import os
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx
from llama_index.readers.github import GithubClient, GithubRepositoryReader
from playwright.async_api import (
    Browser,
    Page,
    async_playwright,
)
from youtube_transcript_api import YouTubeTranscriptApi


class BrowserAgent:
    """
    Tool for browser automation.

    Performs deterministic browser operations only.
    All reasoning, planning and fallback decisions
    are handled by the KEE.
    """

    def __init__(self) -> None:
        self._playwright = None
        self._browser: Browser | None = None
        self._page: Page | None = None

    async def launch(
        self,
        headless: bool = True,
    ) -> dict:
        try:
            self._playwright = await async_playwright().start()

            self._browser = await self._playwright.chromium.launch(
                headless=headless,
            )

            self._page = await self._browser.new_page()

            return {
                "success": True,
                "content": None,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def goto(
        self,
        url: str,
    ) -> dict:
        try:
            response = await self._page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            return {
                "success": True,
                "content": self._page.url,
                "status_code": (response.status if response else None),
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def click(
        self,
        selector: str,
    ) -> dict:
        try:
            await self._page.click(
                selector,
            )

            return {
                "success": True,
                "content": None,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def type(
        self,
        selector: str,
        text: str,
    ) -> dict:
        try:
            await self._page.fill(
                selector,
                text,
            )

            return {
                "success": True,
                "content": None,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def press(
        self,
        selector: str,
        key: str,
    ) -> dict:
        try:
            await self._page.press(
                selector,
                key,
            )

            return {
                "success": True,
                "content": None,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def wait(
        self,
        milliseconds: int,
    ) -> dict:
        try:
            await self._page.wait_for_timeout(
                milliseconds,
            )

            return {
                "success": True,
                "content": None,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def scroll(
        self,
        pixels: int,
    ) -> dict:
        try:
            await self._page.mouse.wheel(
                0,
                pixels,
            )

            return {
                "success": True,
                "content": None,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def current_html(
        self,
    ) -> dict:
        try:
            return {
                "success": True,
                "content": await self._page.content(),
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": "",
                "status_code": None,
                "error": str(e),
            }

    async def current_url(
        self,
    ) -> dict:
        try:
            return {
                "success": True,
                "content": self._page.url,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": "",
                "status_code": None,
                "error": str(e),
            }

    async def find_elements(
        self,
        selector: str,
    ) -> dict:
        try:
            elements = []

            locator = self._page.locator(selector)

            count = await locator.count()

            for i in range(count):
                element = locator.nth(i)

                visible = await element.is_visible()

                elements.append(
                    {
                        "text": (await element.inner_text() if visible else ""),
                        "html": await element.evaluate("(e) => e.outerHTML"),
                    }
                )

            return {
                "success": True,
                "content": elements,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": [],
                "status_code": None,
                "error": str(e),
            }

    async def screenshot(
        self,
        path: str,
    ) -> dict:
        try:
            await self._page.screenshot(
                path=path,
                full_page=True,
            )

            return {
                "success": True,
                "content": Path(path),
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def download(
        self,
        selector: str,
        path: str,
    ) -> dict:
        try:
            async with self._page.expect_download() as download_info:
                await self._page.click(selector)

            download = await download_info.value

            await download.save_as(path)

            return {
                "success": True,
                "content": Path(path),
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    async def download_pdf(
        self,
        url: str,
    ) -> Path:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=60.0,
            headers={
                "User-Agent": "Ratlas/1.0",
            },
        ) as client:
            response = await client.get(url)
        response.raise_for_status()

        temp_dir = Path(
            tempfile.mkdtemp(
                prefix="ratlas_pdf_",
            )
        )

        pdf_path = temp_dir / "document.pdf"

        pdf_path.write_bytes(
            response.content,
        )

        return pdf_path

    async def download_file(
        self,
        url: str,
    ) -> Path:
        launch_result = await self.launch()

        if not launch_result["success"]:
            raise RuntimeError(launch_result["error"])

        try:
            goto_result = await self.goto(url)

            if not goto_result["success"]:
                raise RuntimeError(goto_result["error"])

            await self.wait(3000)

            temp_dir = Path(
                tempfile.mkdtemp(
                    prefix="ratlas_file_",
                )
            )

            file_path = temp_dir / "resource.png"

            await self._page.screenshot(
                path=str(file_path),
                full_page=True,
            )

            return file_path

        finally:
            await self.cleanup()

    async def download_html(
        self,
        url: str,
    ) -> str:
        launch_result = await self.launch()

        if not launch_result["success"]:
            raise RuntimeError(launch_result["error"])

        try:
            goto_result = await self.goto(url)

            if not goto_result["success"]:
                raise RuntimeError(goto_result["error"])

            await self.wait(3000)

            html = (await self.current_html())["content"]

            return html

        finally:
            await self.cleanup()

    async def fetch_github_documents(
        self,
        owner: str,
        repo: str,
    ):
        client = GithubClient(
            github_token=os.getenv("GITHUB_TOKEN"),
        )

        reader = GithubRepositoryReader(
            github_client=client,
            owner=owner,
            repo=repo,
            use_parser=False,
        )

        return reader.load_data(
            branch="main",
        )

    async def fetch_youtube_documents(
        self,
        video_url: str,
    ):
        parsed = urlparse(video_url)

        video_id = parse_qs(
            parsed.query,
        )["v"][0]

        transcript = YouTubeTranscriptApi().fetch(
            video_id,
        )

        return transcript

    async def cleanup(
        self,
    ) -> None:
        if self._page:
            await self._page.close()

        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()
