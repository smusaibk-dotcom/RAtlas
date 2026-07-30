from pydantic import BaseModel


class Candidate(BaseModel):
    text: str
    candidate_type: str
    evidence: str
