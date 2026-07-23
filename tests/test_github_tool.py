from infrastructure.tools.tools import GitHubTool


tool = GitHubTool()

result = tool.clone_repository("https://github.com/pallets/flask.git")

if result["success"]:
    repository = result["content"]

    readme = tool.extract_readme(repository)

    files = tool.fetch_directory(
        repository,
        "",
    )

    app = tool.fetch_file(
        repository,
        "src/flask/app.py",
    )

    print(readme["content"][:500])

    print(len(files["content"]))

    print(app["content"][:500])

else:
    print(result)

tool.cleanup()
