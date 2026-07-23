# Ratlas User Flows

---

# UF-1 Create a Research Workspace

## Objective

Allow the user to create a dedicated workspace for a research project.

## Preconditions

- User is authenticated.

## User Steps

1. Click "New Workspace".
2. Enter workspace name.
3. Optionally enter a description.
4. Click "Create".

## System Actions

1. Validate input.
2. Create a new Workspace.
3. Store it in the database.
4. Redirect user to the empty workspace dashboard.

## Success Outcome

A new workspace is created and becomes the active workspace.

## Failure Cases

- Workspace name is empty.
- Workspace name already exists (optional rule).
- Database error.


---

# UF-2 Choose Knowledge Source

## Objective

Allow the user to decide how knowledge should enter Ratlas.

## Preconditions

- User is authenticated.
- Workspace exists.

## User Steps

1. Open a workspace.
2. Click one of the Three Icons Displayed .
3. Choose one of the following:
   - Explore a Research Topic
   - Upload Research Paper
   - Upload Multimedia (Image / Video / Audio)

## System Actions

1. Display the available knowledge source options.
2. Record the selected ingestion mode.
3. Redirect the user to the corresponding workflow.

## Success Outcome

The user clicks one of the three workflows.

## Failure Cases

- Invalid selection.
- Unsupported upload format.


---

# UF-3 Explore a Research Topic

## Objective

Allow the user to explore any research domain by automatically collecting knowledge from trusted external sources and constructing a Research Evolution Graph.

## Preconditions

- User is authenticated.
- Workspace exists.

## User Steps

1. Open a workspace.
2. Select "Explore Research Topic".
3. Enter a research topic.
4. Click "Generate".

## System Actions

1. Validate the topic.
2. Search trusted external knowledge sources.
3. Collect relevant resources.
4. Extract structured knowledge.
5. Identify concepts and relationships.
6. Construct the Research Evolution Graph.
7. Store the generated knowledge.
8. Display the interactive graph.

## Success Outcome

The user receives an interactive Research Evolution Graph for the selected topic.

## Failure Cases

- No relevant sources found.
- External source unavailable.
- Knowledge extraction fails.
- Graph generation fails.


---

# UF-4 Upload & Analyze a Research Paper

## Objective

Allow the user to upload one or more research papers and automatically integrate their knowledge into the workspace.

## Preconditions

- User is authenticated.
- Workspace exists.

## User Steps

1. Open a workspace.
2. Select "Upload Research Paper".
3. Upload one or more research papers.
4. Click "Analyze".

## System Actions

1. Validate uploaded files.
2. Extract text and metadata.
3. Extract structured knowledge.
4. Identify concepts and relationships.
5. Merge with existing workspace knowledge.
6. Update the Research Evolution Graph.
7. Store extracted knowledge.

## Success Outcome

The uploaded paper is incorporated into the workspace and reflected in the Evolution Graph.

## Failure Cases

- Unsupported file format.
- Corrupted document.
- Extraction failure.
- Graph update failure.


---

# UF-5 Upload & Analyze Multimedia

## Objective

Allow the user to upload multimedia content and integrate the extracted knowledge into the workspace.

## Preconditions

- User is authenticated.
- Workspace exists.

## User Steps

1. Open a workspace.
2. Select "Upload Multimedia".
3. Upload one or more supported files (Image, Video, Audio).
4. Click "Analyze".

## System Actions

1. Validate uploaded files.
2. Extract textual and visual information.
3. Extract structured knowledge.
4. Identify concepts and relationships.
5. Merge with existing workspace knowledge.
6. Update the Research Evolution Graph.
7. Store extracted knowledge.

## Success Outcome

Knowledge extracted from multimedia is integrated into the workspace and reflected in the Evolution Graph.

## Failure Cases

- Unsupported file format.
- Corrupted media.
- Extraction failure.
- Graph update failure.


---

# UF-6 Explore the Research Evolution Graph

## Objective

Allow the user to interactively explore the generated Research Evolution Graph to understand how knowledge has evolved.

## Preconditions

- A Research Evolution Graph exists in the workspace.

## User Steps

1. Open the Evolution Graph.
2. Pan and zoom across the graph.
3. Select a Research Node.
4. Explore connected nodes and relationships.

## System Actions

1. Load the Evolution Graph.
2. Render the graph interactively.
3. Display node details including:
   - Problem
   - Solution
   - Limitations
   - Impact
   - Research Gap
4. Highlight connected nodes and relationships.

## Interactive Actions

Any Action should allow the user to:

- View Node Details
- Jump to Any Research Node
- Show in Evolution Graph
- View Supporting Sources
- Explore Related Concepts
- View Open Research Questions
- Show Research Timeline
- View Learning Path

## Success Outcome

The user understands the evolution of the selected research area through interactive exploration.

## Failure Cases

- Graph unavailable.
- Node information missing.
- Rendering failure.

---

# UF-7 Graph-aware Research Chat

## Objective

Allow the user to ask research questions and receive explainable, evidence-backed answers grounded in the workspace's Knowledge Graph and Research Evolution Graph.

## Preconditions

- User is authenticated.
- Workspace exists.
- Research knowledge has been ingested.
- Research Evolution Graph has been generated.

## User Steps

1. Open the Research Chat.
2. Enter a research question.
3. Submit the query.
4. Review the generated response.
5. Explore the supporting knowledge using the interactive actions.

## System Actions

1. Interpret the user's research question.
2. Retrieve the most relevant knowledge from the workspace.
3. Generate a context-aware answer.
4. Identify supporting Research Nodes.
5. Identify supporting Sources.
6. Generate graph navigation actions.
7. Present an interactive, evidence-backed response.


## Success Outcome

The user receives an explainable, evidence-backed answer that is fully connected to the underlying knowledge graph and can seamlessly navigate through the research ecosystem.

## Failure Cases

- No relevant knowledge found.
- Knowledge retrieval failure.
- Response generation failure.
- Supporting evidence unavailable.
- Graph navigation unavailable.