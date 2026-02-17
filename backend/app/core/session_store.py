from uuid import uuid4
from typing import Dict
from ..schemas.session_schema import PipelineSession

SESSIONS: Dict[str, PipelineSession] = {}

def create_session() -> str:
    sid = uuid4().hex[:8]
    SESSIONS[sid] = PipelineSession()
    return sid

# def get_session(sid: str) -> PipelineSession:
#     return SESSIONS[sid]

from app.core.filter_session_sync import normalize_session

def get_session(sid):
    session = SESSIONS[sid]
    if session:
        session = normalize_session(session)
    return session