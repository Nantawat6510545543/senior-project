from uuid import uuid4
from typing import Dict
from ..schemas.session_schema import PipelineSession

SESSIONS: Dict[str, PipelineSession] = {}

def create_session(input_data: dict) -> str:
    sid = uuid4().hex[:8]
    SESSIONS[sid] = PipelineSession(input=input_data)
    return sid

def get_session(sid: str) -> PipelineSession:
    return SESSIONS[sid]
