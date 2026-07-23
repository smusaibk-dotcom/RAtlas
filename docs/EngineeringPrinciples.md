# Ratlas Engineering Principles

1. Business Logic never depends on external Providers

2. Evolution Graph is deterministic.

3. Ratlas is coverage-driven, not retrieval-driven.

4. All asynchronous workflows must return a standardized response containing:
- task_id
- status
- message
- Optionally, the response may include the identifier of the created resource (e.g., source_id, graph_id, learning_graph_id) if available.
5. All long-running AI workflows must follow a standardized asynchronous execution model.
Workflow:
1. Client submits a request.
2. Backend immediately returns:
   - task_id
   - status
   - message
3. Client monitors execution through the Task API.
4. Upon completion, the client retrieves the generated resource using the appropriate resource API.
This execution model applies to all AI generation workflows, including:
- Research
- Chat
- Knowledge Source Ingestion
- Evolution Graph Generation
- Learning Graph Generation

6. REST APIs must expose backend business capabilities rather than frontend interactions.Frontend behaviors such as zooming, panning, expanding visual elements, highlighting paths, dragging nodes, or other UI interactions must not result in dedicated backend APIs unless backend computation or data retrieval is required.

7. - resource_type ( can be evolution_graph, learning_graph, chat_response, generated_artifact)
   - resource_id   (to be used in resource_endpoint so that no hardcoded routing logic is used for result_type )

8. Every resource must belong to an authenticated user.The backend must verify ownership before performing any operation on a resource.Requests for resources owned by another user must be rejected.

9. When a requested resource exists but is not owned by the authenticated user, the API should return 404 Not Found instead of 403 Forbidden to avoid leaking the existence of resources.

10. All API errors must follow a standardized response structure.
Fields:
- code
- message
- details (optional)
- timestamp
- request_id

11. A multimodal document streaming and chunking framework that preserves document reading order and atomic visual elements while respecting LLM token budgets.