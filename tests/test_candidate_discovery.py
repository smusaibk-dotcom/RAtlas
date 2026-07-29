from application.agents.candidate_discovery_agent import CandidateDiscoveryAgent
from application.dto.chunk import Chunk


chunk = Chunk(
    chunk_id="test_chunk",
    resource_type="text",
    resource_id="test_resource",
    chunk_index=0,
    content={
        "heading": "Transformer",
        "text": """
The Transformer architecture was introduced in the paper
'Attention Is All You Need'. It replaces recurrent neural
networks with self-attention. The model achieved state-of-the-art
results on machine translation benchmarks.
"""
    },
    metadata={}
)

agent = CandidateDiscoveryAgent()

response = agent.run(chunk)

print(response)