"""Interactive FastAPI UI for the Academic Research Assistant.

Serves the live multi-agent workflow (LangGraph) plus per-user SQLite memory.
This is the runtime entrypoint for Docker / Render / Hugging Face Spaces.
"""
from __future__ import annotations

import json
import os
import re
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv()

from main_system import run_system, stream_system  # noqa: E402
from memory.service import (  # noqa: E402
    approve_decision,
    clear_user_memory,
    delete_memory_item,
    delete_session,
    get_or_create_session,
    list_memory,
    list_sessions,
    load_session_messages,
    pin_finding,
    save_message,
)
from memory.store import db_path, init_db  # noqa: E402

STATIC = ROOT / "static"
UPLOADS = ROOT / "data" / "uploads"
COOKIE = "ara_user_id"
UID_RE = re.compile(r"^usr_[a-f0-9]{32}$")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    UPLOADS.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="Academic Research Assistant", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
if STATIC.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC)), name="assets")


def _user_id(request: Request, response: Response) -> str:
    uid = request.cookies.get(COOKIE, "")
    if not UID_RE.match(uid):
        uid = "usr_" + uuid4().hex
    response.set_cookie(
        COOKIE,
        uid,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https",
    )
    return uid


class SessionIn(BaseModel):
    title: str | None = None
    session_id: str | None = None


class MessageIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=8000)
    role: str = "user"


class PinIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=240)
    content: str = Field(..., min_length=1, max_length=20000)
    session_id: str | None = None
    kind: str = "finding"


class ResearchIn(BaseModel):
    session_id: str | None = None
    research_question: str = ""
    paper_text: str = ""
    target_reviewers: int = Field(default=5, ge=1, le=20)
    max_rounds: int = Field(default=5, ge=1, le=8)
    use_bundled_paper: bool = True


@app.get("/")
def index() -> FileResponse:
    page = STATIC / "app.html"
    if not page.exists():
        raise HTTPException(500, "Live app UI is missing")
    return FileResponse(page)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "service": "academic-research-assistant",
        "memory_db": str(db_path()),
        "graph": "langgraph",
    }


@app.get("/api/me")
def me(request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    return {"user_id": uid}


@app.post("/api/sessions")
def create_session(body: SessionIn, request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    return get_or_create_session(uid, session_id=body.session_id, title=body.title)


@app.get("/api/sessions")
def sessions(request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    return {"sessions": list_sessions(uid)}


@app.delete("/api/sessions/{session_id}")
def remove_session(session_id: str, request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    ok = delete_session(uid, session_id)
    if not ok:
        raise HTTPException(404, "Session not found")
    return {"deleted": True, "session_id": session_id}


@app.get("/api/sessions/{session_id}/messages")
def session_messages(session_id: str, request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    return {"messages": load_session_messages(uid, session_id)}


@app.post("/api/sessions/{session_id}/messages")
def post_message(
    session_id: str, body: MessageIn, request: Request, response: Response
) -> dict[str, Any]:
    uid = _user_id(request, response)
    get_or_create_session(uid, session_id=session_id)
    return save_message(uid, session_id, body.role, body.content)


@app.get("/api/memory")
def memory(
    request: Request,
    response: Response,
    kind: str | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    uid = _user_id(request, response)
    return {"items": list_memory(uid, kind=kind, session_id=session_id)}


@app.post("/api/memory")
def pin_memory(body: PinIn, request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    if body.kind == "decision":
        return approve_decision(uid, body.title, body.content, session_id=body.session_id)
    return pin_finding(uid, body.title, body.content, session_id=body.session_id)


@app.delete("/api/memory/{item_id}")
def remove_memory(item_id: int, request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    ok = delete_memory_item(uid, item_id)
    if not ok:
        raise HTTPException(404, "Memory item not found")
    return {"deleted": True, "id": item_id}


@app.delete("/api/memory")
def wipe_memory(request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    return {"cleared": clear_user_memory(uid)}


def _paper_path_for(body: ResearchIn, session_id: str) -> str:
    if body.use_bundled_paper and not (body.paper_text or "").strip():
        return str(ROOT / "data" / "paper_extract.txt")
    UPLOADS.mkdir(parents=True, exist_ok=True)
    path = UPLOADS / f"{session_id}.txt"
    text = (body.paper_text or "").strip() or (
        (ROOT / "data" / "paper_extract.txt").read_text(encoding="utf-8", errors="replace")
    )
    path.write_text(text[:200000], encoding="utf-8")
    return str(path)


@app.post("/api/research")
def research(body: ResearchIn, request: Request, response: Response) -> dict[str, Any]:
    uid = _user_id(request, response)
    session = get_or_create_session(uid, session_id=body.session_id, title=body.research_question or None)
    sid = session["session_id"]
    notes = (body.research_question or "").strip()
    if notes:
        save_message(uid, sid, "user", notes)
    state = run_system(
        target_reviewers=body.target_reviewers,
        max_rounds=body.max_rounds,
        paper_path=_paper_path_for(body, sid),
        user_id=uid,
        session_id=sid,
        user_notes=notes,
        persist_memory=True,
    )
    save_message(uid, sid, "assistant", f"Workflow finished. Reviews={len(state.reviews)} validated={state.is_validated}")
    return {
        "session_id": sid,
        "terminated": state.terminated,
        "validated": state.is_validated,
        "partial": state.partial_output,
        "reviews": len(state.reviews),
        "meta_analysis": state.meta_analysis,
        "final_report": state.final_report,
        "analysis": state.analysis_payload,
        "review_summaries": [
            {
                "reviewer_id": r.get("reviewer_id"),
                "expertise": r.get("expertise"),
                "recommendation": r.get("recommendation"),
                "confidence": r.get("confidence"),
            }
            for r in state.reviews
        ],
    }


def _jsonable(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(x) for x in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


@app.post("/api/research/stream")
def research_stream(body: ResearchIn, request: Request, response: Response) -> StreamingResponse:
    uid = _user_id(request, response)
    session = get_or_create_session(uid, session_id=body.session_id, title=body.research_question or None)
    sid = session["session_id"]
    notes = (body.research_question or "").strip()
    if notes:
        save_message(uid, sid, "user", notes)
    paper_path = _paper_path_for(body, sid)

    def gen():
        yield f"data: {json.dumps({'type': 'start', 'session_id': sid})}\n\n"
        for chunk in stream_system(
            target_reviewers=body.target_reviewers,
            max_rounds=body.max_rounds,
            paper_path=paper_path,
            user_id=uid,
            session_id=sid,
            user_notes=notes,
            persist_memory=True,
        ):
            payload = _jsonable(chunk)
            if payload.get("type") == "node" and isinstance(payload.get("event"), dict):
                slim = {}
                for node, update in payload["event"].items():
                    if isinstance(update, dict):
                        slim[node] = {
                            k: update[k]
                            for k in (
                                "route",
                                "reviewer_index",
                                "is_validated",
                                "partial_output",
                                "terminated",
                                "error_log",
                                "token_estimate",
                            )
                            if k in update
                        }
                    else:
                        slim[node] = True
                payload = {"type": "node", "event": slim}
            yield f"data: {json.dumps(payload, default=str)}\n\n"
        save_message(uid, sid, "assistant", "Multi-agent workflow completed and saved to long-term memory.")
        yield f"data: {json.dumps({'type': 'done', 'session_id': sid})}\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("webapp:app", host="0.0.0.0", port=port, reload=False)
