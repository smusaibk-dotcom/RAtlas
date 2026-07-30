from pydantic import BaseModel

from application.dto.candidate import Candidate


class CandidateDiscoveryResponse(BaseModel):
    candidates: list[Candidate]