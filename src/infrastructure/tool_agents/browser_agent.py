from pathlib import Path

from playwright.sync_api import (
    Browser,
    Page,
    sync_playwright,
)

import httpx

import tempfile


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

    def launch(
        self,
        headless: bool = True,
    ) -> dict:
        try:
            self._playwright = sync_playwright().start()

            self._browser = self._playwright.chromium.launch(
                headless=headless,
            )

            self._page = self._browser.new_page()

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

    def goto(
        self,
        url: str,
    ) -> dict:
        try:
            response = self._page.goto(
                url,
                wait_until="networkidle",
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

    def click(
        self,
        selector: str,
    ) -> dict:
        try:
            self._page.click(
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

    def type(
        self,
        selector: str,
        text: str,
    ) -> dict:
        try:
            self._page.fill(
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

    def press(
        self,
        selector: str,
        key: str,
    ) -> dict:
        try:
            self._page.press(
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

    def wait(
        self,
        milliseconds: int,
    ) -> dict:
        try:
            self._page.wait_for_timeout(
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

    def scroll(
        self,
        pixels: int,
    ) -> dict:
        try:
            self._page.mouse.wheel(
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

    def current_html(
        self,
    ) -> dict:
        try:
            return {
                "success": True,
                "content": self._page.content(),
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

    def current_url(
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

    def find_elements(
        self,
        selector: str,
    ) -> dict:
        try:
            elements = []

            for element in self._page.locator(selector).all():
                elements.append(
                    {
                        "text": (element.inner_text() if element.is_visible() else ""),
                        "html": element.evaluate("(e) => e.outerHTML"),
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

    def screenshot(
        self,
        path: str,
    ) -> dict:
        try:
            self._page.screenshot(
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

    def download(
        self,
        selector: str,
        path: str,
    ) -> dict:
        try:
            with self._page.expect_download() as download:
                self._page.click(
                    selector,
                )

            download.value.save_as(
                path,
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

    def download_pdf(
        self,
        url: str,
    ) -> Path:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=60.0,
            headers={
                "User-Agent": "Ratlas/1.0",
            },
        )

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

    def download_html(
        self,
        url: str,
    ) -> str:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=60.0,
            headers={
                "User-Agent": "Ratlas/1.0",
            },
        )

        response.raise_for_status()

        return response.text

    def cleanup(
        self,
    ) -> None:
        if self._page:
            self._page.close()

        if self._browser:
            self._browser.close()

        if self._playwright:
            self._playwright.stop()
