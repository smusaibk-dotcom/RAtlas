from application.dto.resource_reference import ResourceReference
from infrastructure.parsers.resource_router import ResourceRouter

router = ResourceRouter()

resources = [
    ResourceReference(
        title="PDF",
        url="https://arxiv.org/pdf/1706.03762.pdf",
        provider="test",
    ),
    ResourceReference(
        title="GitHub",
        url="https://github.com/langchain-ai/langchain",
        provider="test",
    ),
    ResourceReference(
        title="YouTube",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        provider="test",
    ),
    ResourceReference(
        title="HTML",
        url="https://openai.com/blog/",
        provider="test",
    ),
    ResourceReference(
        title="Image",
        url="https://example.com/image.png",
        provider="test",
    ),
]

for resource in resources:
    print(
        resource.url,
        " ---> ",
        router.route(resource),
    )
