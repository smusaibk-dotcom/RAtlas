# API Contracts

## Public API Resources

- Research
- Session
- Knowledge Source
- Chat
- Graph
- Task

----

## Research Request API

### Business Actions

- Start New Research

### API 1 — Start New Research

Purpose: Starts a new research workflow for a user query.

Method: POST

Endpoint: /research/query

Request:
- query (required)
- session_id (optional)
- research_mode (optional)

Response:
- task_id
- session_id
- status
- message

HTTP Status Codes:
- 202 Accepted — Research started successfully.
- 400 Bad Request — Invalid request.
- 404 Not Found — Session not found.
- 422 Unprocessable Entity — Validation failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

---

## Session API

### Business Actions

- Create Session
- List Sessions
- Rename Session
- Delete Session

### API 1 — Create Session

Purpose: Creates a new research session.

Method: POST

Endpoint: /sessions

Request:
- title (optional)

Response:
- session_id
- title
- created_at
- status

HTTP Status Codes:
- 201 Created — Session created successfully.
- 400 Bad Request — Invalid request.
- 401 Unauthorized — Authentication failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

### API 2 — List Sessions

Purpose: Returns all research sessions for the authenticated user.

Method: GET

Endpoint: /sessions

Query Parameters:
- page (optional)
- page_size (optional)
- sort_by (optional)
- sort_order (optional)
- search (optional)

Response:
- sessions
- total_count
- page
- page_size

HTTP Status Codes:
- 200 OK — Sessions retrieved successfully.
- 401 Unauthorized — Authentication failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

### API 3 — Rename Session

Purpose: Renames an existing research session.

Method: PATCH

Endpoint: /sessions/{session_id}

Path Parameters:
- session_id (required)

Request:
- title (required)

Validation Rules:
- Title cannot be empty.
- Title cannot contain only whitespace.
- Maximum length: 200 characters.

Response:
- session_id
- title
- updated_at

HTTP Status Codes:
- 200 OK — Session renamed successfully.
- 400 Bad Request — Invalid request.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Session not found.
- 422 Unprocessable Entity — Validation failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

### API 4 — Open Session

Purpose: Loads a research session and its associated workspace.

Method: GET

Endpoint: /sessions/{session_id}

Path Parameters:
- session_id (required)

Query_Parameters:
- preview_limit (optional)
- include (optional)

Response:
- session
- chat_preview
- knowledge_sources_preview
- evolution_graphs_preview
- learning_graphs_preview
- generated_artifacts_preview

HTTP Status Codes:
- 200 OK — Session loaded successfully.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Session not found.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

### API 5 — Delete Session

Purpose: Deletes a research session.

Method: DELETE

Endpoint: /sessions/{session_id}

Path Parameters:
- session_id (required)

Behavior:
- Marks the session as DELETED.
- Hides the session from the user interface.
- Schedules a background cleanup task for permanent deletion.

Response:
- session_id
- status
- message

HTTP Status Codes:
- 200 OK — Session deleted successfully.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Session not found.
- 409 Conflict — Session is already deleted.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token


## Knowledge Source API

### Business Actions

- Ingest Knowledge Source

### API 1 — Ingest Knowledge Source

Purpose: Ingests a knowledge source into a research session.

Method: POST

Endpoint: /sources

Request:
- session_id (required)
- source_type (required)
- source (required)

Response:
- task_id
- source_id
- status
- message

HTTP Status Codes:
- 202 Accepted — Knowledge source ingestion started successfully.
- 400 Bad Request — Invalid request.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Session not found.
- 422 Unprocessable Entity — Validation failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

----

## Chat API

### Business Actions

- Send Message
- Give Feedback

### API 1 — Send Message

Purpose: Sends a chat message within a research session.

Method: POST

Endpoint: /messages

Request:
- session_id (required)
- message (required)

Response:
- task_id
- status
- message

HTTP Status Codes:
- 202 Accepted — Message accepted for processing.
- 400 Bad Request — Invalid request.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Session not found.
- 422 Unprocessable Entity — Validation failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token


### API 2 — Give Feedback

Purpose: Records user feedback for an assistant response.

Method: POST

Endpoint: /messages/{message_id}/feedback

Path Parameters:
- message_id (required)

Request:
- feedback_type (required)
  values:
  - positive
  - negative
- feedback_comment (optional)

Response:
- success
- message

HTTP Status Codes:
- 201 Created — Feedback recorded successfully.
- 400 Bad Request — Invalid request.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Message not found.
- 422 Unprocessable Entity — Validation failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

--- 

## Graph API

### Business Actions
- Get Graph Node

### API 1 — Get Graph Node

Purpose: Returns complete information for a graph node.

Method: GET

Endpoint: /graphs/{graph_type}/nodes/{node_id}

Path Parameters:
- graph_type (required)
- node_id (required)

Response:
- node

HTTP Status Codes:
- 200 OK — Graph node retrieved successfully.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Node not found.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

Validation Rules:
graph_type must be one of:
- evolution
- learning

---

## Task API

### Business Actions
- Get Task Status
- Cancel Task

### API 1 — Get Task Status

Purpose: Returns the current status of a task.

Method: GET

Endpoint: /tasks/{task_id}

Path Parameters:
- task_id (required)

Response:
- task
  - task_id
  - status
  - progress
  - current_stage
  - resource_type 
  - resource_id   
  - resource_endpoint
  - started_at
  - completed_at
  - error_message

HTTP Status Codes:
- 200 OK — Task retrieved successfully.
- 401 Unauthorized — Authentication failed.
- 404 Not Found — Task not found.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token

### API 2 — Cancel Task

Purpose: Cancels an ongoing Task.

Method: POST

Endpoint: /tasks/{task_id}/cancel

Path Parameters:
- task_id (required)

Response:
- task_id
- status
- message

HTTP Status Codes:
- 200 OK — Research cancelled successfully.
- 404 Not Found — Task not found.
- 409 Conflict — Research has already completed and cannot be cancelled.
- 401 Unauthorized — Authentication failed.
- 500 Internal Server Error — Unexpected server error.

Authentication:
- Required
- JWT Bearer Token


----


## Global Error Model
All API errors follow the standardized response structure below.
### Error Response
```json
{
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "The requested session does not exist.",
    "details": null,
    "timestamp": "2026-07-17T15:32:18Z",
    "request_id": "8b7e0a45-7b5d-4a5c-b5de-f8f9d2d7d8b1"
  }
}
```
Fields:
- code
- message
- details (optional)
- timestamp
- request_id