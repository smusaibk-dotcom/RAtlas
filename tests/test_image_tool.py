from infrastructure.tools.tools import ImageTool


tool = ImageTool()

result = tool.fetch_image(
    "https://media.gettyimages.com/id/2283195035/photo/mumbai-india-rakul-preet-singh-attends-the-bollywood-hangama-style-icon-awards-2026-on-june.jpg?s=612x612&w=gi&k=20&c=MzAg472Kt215_bUucBbLQtflpiTcP9xl3-NnhggyIII="
)

print(result)

if result["success"]:
    image = result["content"]

    text = tool.extract_text(image)

    metadata = tool.extract_metadata(image)

    figures = tool.extract_figures(image)

    tables = tool.extract_tables(image)

    print("\n===== OCR =====")
    print(text)

    print(image)

tool.cleanup()
