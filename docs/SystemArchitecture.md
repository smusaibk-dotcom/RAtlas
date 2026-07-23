``` mermaid
flowchart   TD

    %% ===========================
    %% CLIENT LAYER
    %% ===========================
    U[User]

    subgraph FE["Frontend (Web Application)"]
        UI[Research Workspace UI]
    end

    U --> UI

    %% ===========================
    %% BACKEND
    %% ===========================
    UI -->|HTTPS / WebSocket| API[FastAPI Backend]

    %% ===========================
    %% CORE SERVICES
    %% ===========================
    API --> AUTH[Authentication Service]
    API --> WS[Workspace Service]
    API --> ORCH[Agent Orchestrator]

    %% ===========================
    %% AGENTS
    %% ===========================
    subgraph AGENTS["Agent Layer"]
        COORD[Coordinator Agent]
        RESEARCH[Research Agent]
        MULTI[Multimodal Agent]
        GRAPH[Knowledge Graph Agent]
        ANSWER[Answer Generation Agent]
    end

    ORCH --> COORD
    COORD --> RESEARCH
    COORD --> MULTI
    COORD --> GRAPH
    COORD --> ANSWER

    %% ===========================
    %% EXTERNAL KNOWLEDGE
    %% ===========================
    subgraph EXT["External Knowledge Sources"]
        WEB[Web Search]
        ARXIV[arXiv]
        SCHOLAR[Google Scholar]
        PUBMED[PubMed]
        GITHUB[GitHub]
        YOUTUBE[YouTube]
        WIKI[Wikipedia]
    end

    RESEARCH --> WEB
    RESEARCH --> ARXIV
    RESEARCH --> SCHOLAR
    RESEARCH --> PUBMED
    RESEARCH --> GITHUB
    RESEARCH --> YOUTUBE
    RESEARCH --> WIKI

    %% ===========================
    %% USER INGESTION
    %% ===========================
    subgraph INGEST["User Uploaded Sources"]
        PDF[PDF]
        DOC[DOCX]
        PPT[PPTX]
        IMG[Images]
        VIDEO[Videos]
        AUDIO[Audio]
        URL[URLs]
    end

    MULTI --> PDF
    MULTI --> DOC
    MULTI --> PPT
    MULTI --> IMG
    MULTI --> VIDEO
    MULTI --> AUDIO
    MULTI --> URL

    %% ===========================
    %% KNOWLEDGE PIPELINE
    %% ===========================
    subgraph PIPE["Knowledge Processing Pipeline"]
        PARSER[Document Parser]
        OCR[OCR]
        STT[Speech-to-Text]
        EMBED[Embedding Generator]
        EXTRACT[Knowledge Extraction]
        ENTITY[Entity & Relation Extraction]
    end

    RESEARCH --> PARSER
    MULTI --> PARSER

    PARSER --> OCR
    PARSER --> STT
    OCR --> EXTRACT
    STT --> EXTRACT

    EXTRACT --> ENTITY
    ENTITY --> EMBED

    %% ===========================
    %% STORAGE
    %% ===========================
    subgraph STORAGE["Storage Layer"]
        POSTGRES[(PostgreSQL)]
        VECTOR[(Vector Database)]
        KG[(Knowledge Graph)]
        FILES[(Object Storage)]
    end

    PARSER --> FILES
    EMBED --> VECTOR
    ENTITY --> KG
    API --> POSTGRES

    %% ===========================
    %% AI
    %% ===========================
    subgraph AI["AI Layer"]
        RAG[Hybrid RAG Engine]
        EVOLUTION[Research Evolution Engine]
        LLM[LLM]
    end

    VECTOR --> RAG
    KG --> RAG
    RAG --> EVOLUTION
    EVOLUTION --> LLM

    ANSWER --> RAG
    ANSWER --> LLM

    %% ===========================
    %% RESPONSE
    %% ===========================
    LLM --> API
    API --> UI
    ```