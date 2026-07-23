# Ratlas Domain Services

---

## 1. Coordinator Agent

### Responsibility
Orchestrates the complete execution flow of Ratlas.

---

## 2. Query Understanding Service

### Responsibility
Analyzes the user query, detects intent, determines research domain and decides whether clarification is required.

---

## 3. Content Extraction Service

### Responsibility
Transforms uploaded documents into a Structured Document.

---

## 4. Knowledge Extraction Service

### Responsibility
Extracts, validates, merges and normalizes knowledge from the Structured Document.

---

## 5. Document Overview Service

### Responsibility
Generates the Document Overview shown to the user before workflow selection.

---

## 6. Research Workflow Router

### Responsibility
Selects the appropriate Research Workflow based on the user's intent.

---

## 7. Coverage Evaluation Service

### Responsibility
Determines whether sufficient knowledge has been collected to reconstruct the research domain.

---

## 8. Evolution Engine

### Responsibility
Constructs deterministic Evolution Graphs.

---

## 9. Learning Engine

### Responsibility
Constructs prerequisite-based Learning Graphs.

---

## 10. Search Service

### Responsibility
Retrieves trusted external research sources.