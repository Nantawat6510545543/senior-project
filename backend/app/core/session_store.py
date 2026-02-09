from uuid import uuid4
from typing import Dict
from ..schemas.session_schema import PipelineSession

SESSIONS: Dict[str, PipelineSession] = {}

def create_session() -> str:
    sid = uuid4().hex[:8]
    SESSIONS[sid] = PipelineSession()
    return sid

def get_session(sid: str) -> PipelineSession:
    return SESSIONS[sid]
