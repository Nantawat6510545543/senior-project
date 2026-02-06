from fastapi import APIRouter, HTTPException
from app.core.session_store import create_session, get_session

router = APIRouter(prefix="/session", tags=["session"])


@router.post("")
def open_session(input: dict):
    sid = create_session(input)
    return {"session_id": sid}

@router.get("/{sid}")
def read_session(sid: str):
    return get_session(sid)

@router.patch("/{sid}/{schema_type}")
def patch_session(sid: str, schema_type: str, payload: dict):
    session = get_session(sid)

    if not hasattr(session, schema_type):
        return {"error": f"Unknown schemas type '{schema_type}'"}

    setattr(session, schema_type, payload)
    return {"ok": True}