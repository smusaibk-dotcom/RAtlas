# ==========================================================
# HTML TOOL
# ==========================================================
from io import StringIO

import httpx
import pandas as pd
import trafilatura
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class HTMLTool:
    """
    Tool for interacting with HTML webpages.

    Performs deterministic operations only.
    All reasoning, planning and fallback decisions
    are handled by the KEE.
    """

    def __init__(self):
        self._playwright = sync_playwright

    def extract(
        self,
        url: str,
    ):
        """
        Extract the complete webpage.
        """

        downloaded = trafilatura.fetch_url(
            url,
        )

        if downloaded is not None:
            return trafilatura.extract(
                downloaded,
                output_format="xml",
                include_comments=True,
                include_tables=True,
                include_images=True,
                include_links=True,
            )

        with self._playwright() as p:
            browser = p.chromium.launch(
                headless=True,
            )

            try:
                page = browser.new_page()

                page.goto(
                    url,
                    wait_until="networkidle",
                )

                html = page.content()

                return trafilatura.extract(
                    html,
                    output_format="xml",
                    include_comments=True,
                    include_tables=True,
                    include_images=True,
                    include_links=True,
                )

            finally:
                browser.close()

    def fetch_page(
        self,
        url: str,
    ) -> dict:
        """
        Download the HTML of a webpage.
        """

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

            return {
                "success": True,
                "content": response.text,
                "status_code": response.status_code,
                "error": None,
            }

        except Exception as e:
            if e.response.status_code == 403:
                return self.render_page(url)

            return {
                "success": False,
                "content": None,
                "status_code": getattr(
                    getattr(e, "response", None),
                    "status_code",
                    None,
                ),
                "error": str(e),
            }

    def render_page(
        self,
        url: str,
    ) -> dict:
        """Render a JavaScript-heavy webpage."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(
                    url,
                    wait_until="networkidle",
                )
                html = page.content()
                return {
                    "success": True,
                    "content": html,
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
            finally:
                browser.close()

    def parse_html(
        self,
        page: str,
    ) -> BeautifulSoup:
        """
        Parse HTML into a BeautifulSoup document.
        """

        return BeautifulSoup(
            page,
            "html.parser",
        )

    def extract_main_content(
        self,
        page: str,
    ) -> str:
        content = trafilatura.extract(
            page,
        )

        return content or ""

    def extract_links(
        self,
        document,
    ) -> list[str]:
        return [link.get("href") for link in document.find_all("a", href=True)]

    def extract_images(
        self,
        document,
    ) -> list[str]:
        images = []

        for index, image in enumerate(
            document.find_all("img", src=True),
            start=1,
        ):
            images.append(
                {
                    "id": f"image_{index}",
                    "src": image.get("src"),
                    "alt": image.get("alt"),
                    "caption": None,
                    "start_offset": None,
                    "end_offset": None,
                }
            )

        return images

    def extract_tables(
        self,
        page: str,
    ):
        try:
            return pd.read_html(StringIO(page))

        except ValueError:
            return []

        except Exception:
            return []

    def extract_metadata(
        self,
        document,
    ) -> dict:
        metadata = {
            "title": None,
            "description": None,
        }

        title = document.find("title")

        if title:
            metadata["title"] = title.get_text(strip=True)

        description = document.find(
            "meta",
            attrs={"name": "description"},
        )

        if description:
            metadata["description"] = description.get("content")

        return metadata

    def extract_headings(
        self,
        document,
    ) -> list[dict]:
        headings = []

        for level in range(1, 7):
            for index, heading in enumerate(
                document.find_all(f"h{level}"),
                start=1,
            ):
                headings.append(
                    {
                        "id": f"h{level}_{index}",
                        "level": level,
                        "text": heading.get_text(
                            " ",
                            strip=True,
                        ),
                        "position": index,
                    }
                )

        return headings

    def extract_code_blocks(
        self,
        document,
    ) -> list[dict]:
        blocks = []

        for index, block in enumerate(
            document.find_all(
                [
                    "pre",
                    "code",
                ]
            ),
            start=1,
        ):
            blocks.append(
                {
                    "id": f"code_{index}",
                    "language": (
                        block.get(
                            "class",
                            [None],
                        )[0]
                        if block.get("class")
                        else None
                    ),
                    "content": block.get_text(
                        "\n",
                        strip=True,
                    ),
                    "start_offset": None,
                    "end_offset": None,
                }
            )

        return blocks

    def extract_figures(
        self,
        document,
    ) -> list[dict]:
        figures = []

        for index, figure in enumerate(
            document.find_all("figure"),
            start=1,
        ):
            image = figure.find("img")

            caption = figure.find("figcaption")

            figures.append(
                {
                    "id": f"figure_{index}",
                    "image": (image.get("src") if image else None),
                    "caption": (
                        caption.get_text(
                            " ",
                            strip=True,
                        )
                        if caption
                        else None
                    ),
                    "start_offset": None,
                    "end_offset": None,
                }
            )

        return figures

    def extract_references(
        self,
        document,
    ) -> list[dict]:
        references = []

        selectors = [
            "references",
            "reference",
            "bibliography",
            "bib",
            "citation",
        ]

        for selector in selectors:
            section = document.find(
                id=re.compile(
                    selector,
                    re.IGNORECASE,
                )
            )

            if section:
                items = section.find_all(
                    [
                        "li",
                        "p",
                    ]
                )

                for index, item in enumerate(
                    items,
                    start=1,
                ):
                    references.append(
                        {
                            "id": f"reference_{index}",
                            "text": item.get_text(
                                " ",
                                strip=True,
                            ),
                            "start_offset": None,
                            "end_offset": None,
                        }
                    )

                break

        return references

    def extract_section_hierarchy(
        self,
        document,
    ) -> list[dict]:
        hierarchy = []

        stack = []

        for heading in document.find_all(
            [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
            ]
        ):
            level = int(
                heading.name[1],
            )

            while stack and stack[-1]["level"] >= level:
                stack.pop()

            parent = stack[-1]["id"] if stack else None

            node = {
                "id": f"{heading.name}_{len(hierarchy) + 1}",
                "title": heading.get_text(
                    " ",
                    strip=True,
                ),
                "level": level,
                "parent": parent,
            }

            hierarchy.append(
                node,
            )

            stack.append(
                node,
            )

        return hierarchy

    def extract_dom_positions(
        self,
        document,
    ) -> list[dict]:
        """
        Record the DOM position of important elements.
        """

        positions = []

        selectors = [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "table",
            "figure",
            "img",
            "pre",
            "code",
        ]

        index = 1

        for selector in selectors:
            for element in document.find_all(selector):
                positions.append(
                    {
                        "id": f"{selector}_{index}",
                        "tag": selector,
                        "position": index,
                        "text": element.get_text(
                            " ",
                            strip=True,
                        )[:200],
                    }
                )

                index += 1

        return positions

    def cleanup(
        self,
    ) -> None:
        return
