from infrastructure.tools.tools import YouTubeTool


tool = YouTubeTool()

result = tool.fetch_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

print(result)

if result["success"]:
    video = result["content"]

    metadata = tool.extract_metadata(video)

    transcript = tool.extract_transcript(video)

    chapters = tool.extract_chapters(video)

    print("\n===== METADATA =====")
    print(metadata)

    print("\n===== TRANSCRIPT =====")
    print(transcript["content"][:1000])

    print("\n===== CHAPTERS =====")
    print(chapters)

tool.cleanup()
