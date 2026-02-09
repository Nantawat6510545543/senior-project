from fastapi import APIRouter
from pydantic import TypeAdapter
from app.core.session_store import create_session, get_session

router = APIRouter(prefix="/session", tags=["session"])


@router.post("")
def open_session():
    sid = create_session()
    return {"session_id": sid}

@router.get("/{sid}")
def read_session(sid: str):
    return get_session(sid)

@router.patch("/{sid}/{schema_type}")
def patch_session(sid: str, schema_type: str, payload: dict | None):
    session = get_session(sid)

    if schema_type not in type(session).model_fields:
        return {"error": f"Unknown schema type '{schema_type}'"}

    # Convert from dict to Schema
    field = type(session).model_fields[schema_type]
    annotation = field.annotation

    if payload is None:
        value = None
    else:
        value = TypeAdapter(annotation).validate_python(payload)

    setattr(session, schema_type, value)
    return {"ok": True}