from urllib.parse import urlparse

from application.dto.resource_reference import ResourceReference


class ResourceRouter:
    """
    Deterministically classifies resources.

    No downloading.
    No parsing.
    No chunking.
    """

    def route(
        self,
        resource: ResourceReference,
    ) -> str:
        url = resource.url.lower()

        hostname = urlparse(url).netloc.lower()

        path = urlparse(url).path.lower()

        if "youtube.com" in hostname or "youtu.be" in hostname:
            return "youtube"

        if "github.com" in hostname:
            return "github"

        if path.endswith(".pdf"):
            return "pdf"

        if path.endswith(
            (
                ".doc",
                ".docx",
                ".ppt",
                ".pptx",
                ".md",
                ".txt",
            )
        ):
            return "document"

        if path.endswith(
            (
                ".png",
                ".jpg",
                ".jpeg",
                ".webp",
                ".bmp",
                ".gif",
                ".tiff",
            )
        ):
            return "image"

        return "html"
