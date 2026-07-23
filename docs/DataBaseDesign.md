# Database Design

## Database Ownership

### PostgreSQL
Stores the transactional and relational data of Ratlas.

#### Owns
- Research Sessions
- Research Topics
- Documents
- Structured Documents
- Generated Artifacts
- Tasks
- Chat History
- Workflow Metadata
- User Metadata (Future)

---

### Neo4j
Stores graph structures and relationships.

#### Owns
- Evolution Graphs
- Learning Graphs
- Graph Nodes
- Graph Edges
- Concept Relationships

---

### Qdrant
Stores vector embeddings used for semantic retrieval.

#### Owns
- Document Embeddings
- Chunk Embeddings
- Concept Embeddings
- Graph Node Embeddings

---

### Redis
Stores temporary and high-speed runtime data.

#### Owns
- Active Sessions
- Task Progress
- LLM Cache
- Workflow Cache
- Rate Limiting

---

# PostgreSQL

## Aggregate Root 1: Research Session

### Attributes

- session_id (PK)
- title (nullable)
- status
- created_at
- updated_at
- last_accessed_at

### Relationships

One Research Session can have:

- Many Documents
- Many Tasks
- Many Chat Messages
- Many Generated Artifacts
- Many Evolution Graphs
- Many Learning Graphs

#### Task

##### Attributes

- task_id (PK)
- session_id (FK)
- workflow_type
- status
- progress_percentage
- current_stage
- started_at
- completed_at
- error_message (nullable)

##### Relationships

Belongs to:

- One Research Session

#### Chat Message

##### Attributes

- message_id (PK)
- session_id (FK)
- role
- content
- user_intent
- referenced_source_ids
- referenced_graph_node_ids
- referenced_artifact_ids
- created_at

##### Relationships

Belongs to:

- One Research Session

#### Generated Artifact

##### Attributes

- artifact_id (PK)
- session_id (FK)
- artifact_type
- title
- storage_location
- created_at

##### Relationships

Belongs to:

- One Research Session

### Aggregate Root 2: Knowledge Source

#### Attributes

- Source_id (PK)
- session_id (FK)
- title
- source_type
- file_type
- original_url
- storage_path
- file_size
- source_status
- created_at
- updated_at

#### Owns

- Structured Document

#### Relationships

Belongs to:

- One Research Session

#### Structured Document

##### Attributes

- structured_document_id (PK)
- source_id (FK)
- pipeline_name
- pipeline_version
- is_active
- extraction_status
- created_at

##### Contains

- Metadata
- Sections
- Figures
- Tables
- Equations
- References
- Concepts
- Citations
- Chunks


### Aggregate Root 3: Evolution Graph

#### Attributes

- graph_id (PK)
- session_id (FK)
- title
- graph_status
- version
- created_at
- updated_at

#### Owns

- Graph Nodes
- Graph Edges

#### Relationships

Belongs to:

- One Research Session

#### Graph Node

- node_id (PK)
- graph_id (FK)
- title
- summary
- key_contributions
- limitations
- year
- node_type
- importance_score

#### Graph Edge

- edge_id (PK)
- graph_id (FK)
- source_node_id
- target_node_id
- relationship_type
- confidence_score

### Aggregate Root 4: Learning Graph

#### Attributes

- learning_graph_id (PK)
- session_id (FK)
- title
- graph_status
- version
- created_at
- updated_at

#### Owns

- Learning Nodes
- Learning Edges

#### Relationships

Belongs to:

- One Research Session

#### Learning Node

- node_id (PK)
- learning_graph_id (FK)
- linked_evolution_node_id (nullable)
- title
- summary
- difficulty_level
- estimated_duration
- prerequisites_count
- importance_score

#### Learning Edge

- edge_id (PK)
- learning_graph_id (FK)
- source_node_id
- target_node_id
- relationship_type




# Relationships & Cardinalities

## Research Session

- One Research Session → Many Knowledge Sources (1:N)
- One Research Session → Many Tasks (1:N)
- One Research Session → Many Chat Messages (1:N)
- One Research Session → Many Generated Artifacts (1:N)
- One Research Session → Many Evolution Graphs (1:N)
- One Research Session → Many Learning Graphs (1:N)

---

## Knowledge Source

- One Knowledge Source → Many Structured Documents (1:N)

---

## Evolution Graph

- One Evolution Graph → Many Graph Nodes (1:N)
- One Evolution Graph → Many Graph Edges (1:N)

---

## Learning Graph

- One Learning Graph → Many Learning Nodes (1:N)
- One Learning Graph → Many Learning Edges (1:N)

---

## Cross-Aggregate Relationships

- Many Knowledge Sources <-> Many Graph Nodes (M:N)
- Many Knowledge Sources <-> Many Learning Nodes (M:N)


----



# Neo4j Schema

## Purpose

Stores the evolution and learning knowledge graphs for efficient graph traversal.

---

## Node Labels

### EvolutionNode

Properties

- node_id
- title
- summary
- key_contributions
- limitations
- year
- node_type
- importance_score
- supporting_source_ids

---

### LearningNode

Properties

- node_id
- title
- summary
- difficulty_level
- estimated_duration
- importance_score
- linked_evolution_node_id
- supporting_source_ids

---

## Relationship Types

### Evolution Relationships

- INSPIRED_BY
- IMPROVES
- EXTENDS
- INTRODUCES
- REPLACES
- USES
- COMBINES
- COMPARES_WITH
- COMPETES_WITH
- ADDRESSES_LIMITATION_OF
- ENABLES
- RELATED_TO

---

### Learning Relationships

- PREREQUISITE_OF
- RECOMMENDED_NEXT
- ALTERNATIVE_TO
- DEPENDS_ON


# Qdrant Schema

## Purpose

Stores vector embeddings for semantic search and retrieval.

---

## Collections

### KnowledgeSourceEmbeddings

Stores embeddings for extracted content from every Knowledge Source.

Metadata

- source_id
- structured_document_id
- chunk_id
- chunk_text
- source_type
- title
- section
- embedding_model
- created_at

---

### EvolutionNodeEmbeddings

Stores embeddings for Evolution Nodes.

Metadata

- node_id
- title
- summary
- year
- node_type

---

### LearningNodeEmbeddings

Stores embeddings for Learning Nodes.

Metadata

- node_id
- title
- summary
- difficulty_level


# Redis Schema

## Purpose

Stores temporary, high-speed runtime data.

---

## Key Structures

### Active Sessions

Stores active user sessions.

---

### Task Progress

Stores real-time progress of long-running workflows.

---

### LLM Cache

Stores cached LLM responses to reduce latency and cost.

---

### Workflow Cache

Stores temporary workflow state during execution.

---

### Rate Limiting

Stores request counters and rate-limiting metadata.