# ==========================================================
# IMAGE TOOL
# ==========================================================

import io
import httpx
from PIL import Image
import pytesseract
from PIL.ExifTags import TAGS
from playwright.sync_api import sync_playwright


class ImageTool:
    """
    Tool for interacting with images.

    Performs deterministic operations only.
    All reasoning, planning and fallback decisions
    are handled by the KEE.
    """

    def extract(
        self,
        url: str,
    ):
        """
        Extract the complete image using Surya.
        """

        image = self.fetch_image(
            url,
        )

        if not image["success"]:
            raise RuntimeError(
                image["error"],
            )

        # Temporary until Surya is integrated.
        return image["content"]

    def fetch_image(
        self,
        url: str,
    ) -> dict:
        try:
            response = httpx.get(
                url,
                headers={
                    "User-Agent": "Ratlas/1.0",
                },
                follow_redirects=True,
                timeout=30.0,
            )

            response.raise_for_status()

            image = Image.open(
                io.BytesIO(
                    response.content,
                )
            )

            return {
                "success": True,
                "content": image,
                "status_code": response.status_code,
                "error": None,
            }

        except Exception as e:
            response = getattr(
                e,
                "response",
                None,
            )

            if response is not None and response.status_code == 403:
                return self.render_image(url)

            return {
                "success": False,
                "content": None,
                "status_code": getattr(
                    response,
                    "status_code",
                    None,
                ),
                "error": str(e),
            }

    def render_image(
        self,
        url: str,
    ) -> dict:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                )

                page = browser.new_page()

                page.goto(
                    url,
                    wait_until="networkidle",
                )

                image_bytes = page.locator("img").screenshot()

                browser.close()

                image = Image.open(
                    io.BytesIO(
                        image_bytes,
                    )
                )

                return {
                    "success": True,
                    "content": image,
                    "status_code": 200,
                    "error": None,
                }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    def extract_text(
        self,
        image: Image.Image,
    ) -> dict:
        try:
            text = pytesseract.image_to_string(
                image,
            )

            return {
                "success": True,
                "content": text,
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

    def extract_tables(
        self,
        image: Image.Image,
    ) -> dict:
        try:
            return {
                "success": True,
                "content": [],
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

    def extract_figures(
        self,
        image: Image.Image,
    ) -> dict:
        try:
            return {
                "success": True,
                "content": image,
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

    def extract_metadata(
        self,
        image: Image.Image,
    ) -> dict:
        try:
            metadata = {}

            exif = image.getexif()

            if exif:
                for tag, value in exif.items():
                    metadata[
                        TAGS.get(
                            tag,
                            tag,
                        )
                    ] = value

            return {
                "success": True,
                "content": metadata,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": {},
                "status_code": None,
                "error": str(e),
            }

    def cleanup(
        self,
    ) -> None:
        return
