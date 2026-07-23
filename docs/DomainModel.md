# Ratlas Domain Model

## Core Entities

### 1. User

Represents the person using Ratlas.

---

### 2. Workspace

A dedicated research workspace.

---

### 3. Research Topic

The primary domain being explored.

Examples:
- Deep Learning
- Quantum Computing
- Paintings
- Cancer Immunotherapy

---

### 4. Source

Any source of knowledge.

Types:
- Research Paper
- Website
- Video
- Image
- Presentation
- Book
- GitHub Repository
- Uploaded Document

---

### 5. Concept

A research idea or concept.

Examples:
- Backpropagation
- Crispr Technoloy
- Oil Paintings

---

### 6. Research Node

Represents one important milestone in research evolution.

Contains:
- Problem
- Solution
- Limitations
- Impact
- Research Gap

---

### 7. Evolution Edge

Represents how one Research Node influenced another.

---

### 8. Knowledge Graph

Stores relationships between concepts, papers, researchers and evolution nodes.

---

### 9. Chat Session

Stores research conversations.

### Reesearch Session

will Have access to Documents , Research Topics, Structured Document, Evolution Graphs, Learning Graphs, Chat History, Generated Artifacts