from infrastructure.tool_agents.html_agent import HTMLTool

tool = HTMLTool()

doc = tool.extract("https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)")

print(type(doc))
print(doc[:500])
