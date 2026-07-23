from infrastructure.tools.tools import BrowserTool


tool = BrowserTool()

print(tool.launch())

print(tool.goto("https://arxiv.org"))

print(tool.current_url())

inputs = tool.find_elements("input")

print(inputs)

if inputs["success"] and inputs["content"]:
    print(
        tool.type(
            "input",
            "transformer architecture",
        )
    )

    print(
        tool.press(
            "input",
            "Enter",
        )
    )

    print(
        tool.wait(
            3000,
        )
    )

    print(
        tool.current_url(),
    )

    html = tool.current_html()

    print(
        html["content"][:1000],
    )

    print(
        tool.screenshot(
            "browser_test.png",
        )
    )

tool.cleanup()
