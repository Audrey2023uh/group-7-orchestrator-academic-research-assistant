"""High-level memory API: isolation, redaction, short-term and long-term records."""
from __future__ import annotations

import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any

from agents import redact_text
from memory.store import get_conn, init_db

KIND_PAPER = "reviewed_paper"
KIND_FINDING = "finding"
KIND_DECISION = "decision"
KIND_OUTPUT = "agent_output"
KIND_SUMMARY = "session_summary"

ALLOWED_KINDS = {KIND_PAPER, KIND_FINDING, KIND_DECISION, KIND_OUTPUT, KIND_SUMMARY}
ALLOWED_ROLES = {"user", "assistant", "system", "agent"}

_SECRET_FIELD = re.compile(
    r"(?i)\b(api[_-]?key|password|passwd|secret|token|authorization|bearer|private[_-]?key)\b"
)
_KEY_BLOB = re.compile(
    r"(?i)\b(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|Bearer\s+[A-Za-z0-9._\-]+)\b"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def _safe_text(value: str | None, *, limit: int = 20000) -> str:
    text = redact_text(value or "")
    text = _KEY_BLOB.sub("[REDACTED]", text)
    if _SECRET_FIELD.search(text) and ("=" in text or ":" in text):
        text = redact_text(text)
    return text[:limit]


def _looks_like_secret(text: str) -> bool:
    if _KEY_BLOB.search(text or ""):
        return True
    lowered = (text or "").lower()
    if any(s in lowered for s in ("api_key=", "apikey=", "password=", "secret=", "token=")):
        return True
    return False


def ensure_user(user_id: str) -> str:
    init_db()
    uid = (user_id or "").strip() or _new_id("usr")
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users(user_id, created_at) VALUES (?, ?)",
            (uid, _now()),
        )
    return uid


def get_or_create_session(
    user_id: str,
    session_id: str | None = None,
    title: str | None = None,
) -> dict[str, Any]:
    uid = ensure_user(user_id)
    now = _now()
    with get_conn() as conn:
        if session_id:
            row = conn.execute(
                "SELECT * FROM sessions WHERE session_id = ? AND user_id = ?",
                (session_id, uid),
            ).fetchone()
            if row:
                return dict(row)
        sid = _new_id("ses")
        label = _safe_text(title or "New research session", limit=200)
        conn.execute(
            """
            INSERT INTO sessions(session_id, user_id, title, status, created_at, updated_at)
            VALUES (?, ?, ?, 'active', ?, ?)
            """,
            (sid, uid, label, now, now),
        )
        row = conn.execute(
            "SELECT * FROM sessions WHERE session_id = ? AND user_id = ?",
            (sid, uid),
        ).fetchone()
        return dict(row)


def list_sessions(user_id: str) -> list[dict[str, Any]]:
    uid = ensure_user(user_id)
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT * FROM sessions
            WHERE user_id = ?
            ORDER BY updated_at DESC
            """,
            (uid,),
        ).fetchall()
        return [dict(r) for r in rows]


def save_message(user_id: str, session_id: str, role: str, content: str) -> dict[str, Any]:
    uid = ensure_user(user_id)
    role_n = role if role in ALLOWED_ROLES else "user"
    body = _safe_text(content, limit=8000)
    if _looks_like_secret(content):
        body = _safe_text(content, limit=8000)
    get_or_create_session(uid, session_id)
    now = _now()
    with get_conn() as conn:
        owned = conn.execute(
            "SELECT 1 FROM sessions WHERE session_id = ? AND user_id = ?",
            (session_id, uid),
        ).fetchone()
        if not owned:
            raise ValueError("session not found for user")
        cur = conn.execute(
            """
            INSERT INTO messages(user_id, session_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (uid, session_id, role_n, body, now),
        )
        conn.execute(
            "UPDATE sessions SET updated_at = ? WHERE session_id = ? AND user_id = ?",
            (now, session_id, uid),
        )
        return {
            "id": cur.lastrowid,
            "user_id": uid,
            "session_id": session_id,
            "role": role_n,
            "content": body,
            "created_at": now,
        }


def load_session_messages(user_id: str, session_id: str, *, limit: int = 200) -> list[dict[str, Any]]:
    uid = ensure_user(user_id)
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, role, content, created_at
            FROM messages
            WHERE user_id = ? AND session_id = ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (uid, session_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def _insert_item(
    conn: sqlite3.Connection,
    *,
    user_id: str,
    session_id: str | None,
    kind: str,
    title: str,
    content: str,
    metadata: dict[str, Any] | None = None,
) -> int:
    if kind not in ALLOWED_KINDS:
        raise ValueError(f"unsupported memory kind: {kind}")
    body = _safe_text(content)
    if _looks_like_secret(content) and not body.strip():
        return 0
    meta = json.dumps(metadata or {}, ensure_ascii=True)
    meta = _safe_text(meta, limit=4000)
    cur = conn.execute(
        """
        INSERT INTO memory_items(user_id, session_id, kind, title, content, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, session_id, kind, _safe_text(title, limit=240), body, meta, _now()),
    )
    return int(cur.lastrowid)


def pin_finding(
    user_id: str,
    title: str,
    content: str,
    session_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    uid = ensure_user(user_id)
    with get_conn() as conn:
        item_id = _insert_item(
            conn,
            user_id=uid,
            session_id=session_id,
            kind=KIND_FINDING,
            title=title,
            content=content,
            metadata=metadata,
        )
    return {"id": item_id, "kind": KIND_FINDING, "title": title}


def approve_decision(
    user_id: str,
    title: str,
    content: str,
    session_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    uid = ensure_user(user_id)
    with get_conn() as conn:
        item_id = _insert_item(
            conn,
            user_id=uid,
            session_id=session_id,
            kind=KIND_DECISION,
            title=title,
            content=content,
            metadata=metadata or {"approved": True},
        )
    return {"id": item_id, "kind": KIND_DECISION, "title": title}


def list_memory(
    user_id: str,
    *,
    kind: str | None = None,
    session_id: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    uid = ensure_user(user_id)
    sql = "SELECT * FROM memory_items WHERE user_id = ?"
    args: list[Any] = [uid]
    if kind:
        sql += " AND kind = ?"
        args.append(kind)
    if session_id:
        sql += " AND session_id = ?"
        args.append(session_id)
    sql += " ORDER BY id DESC LIMIT ?"
    args.append(limit)
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(sql, args).fetchall()]


def delete_memory_item(user_id: str, item_id: int) -> bool:
    uid = ensure_user(user_id)
    with get_conn() as conn:
        cur = conn.execute(
            "DELETE FROM memory_items WHERE id = ? AND user_id = ?",
            (item_id, uid),
        )
        return cur.rowcount > 0


def delete_session(user_id: str, session_id: str) -> bool:
    uid = ensure_user(user_id)
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM messages WHERE user_id = ? AND session_id = ?",
            (uid, session_id),
        )
        conn.execute(
            "DELETE FROM memory_items WHERE user_id = ? AND session_id = ?",
            (uid, session_id),
        )
        cur = conn.execute(
            "DELETE FROM sessions WHERE session_id = ? AND user_id = ?",
            (session_id, uid),
        )
        return cur.rowcount > 0


def clear_user_memory(user_id: str) -> dict[str, int]:
    uid = ensure_user(user_id)
    with get_conn() as conn:
        msg = conn.execute("DELETE FROM messages WHERE user_id = ?", (uid,)).rowcount
        items = conn.execute("DELETE FROM memory_items WHERE user_id = ?", (uid,)).rowcount
        sessions = conn.execute("DELETE FROM sessions WHERE user_id = ?", (uid,)).rowcount
    return {"messages": msg, "memory_items": items, "sessions": sessions}


def memory_brief_for_user(user_id: str, *, max_chars: int = 1800) -> str:
    """Compact long-term context for the coordinator/analyzer (not reviewer isolation)."""
    items = list_memory(user_id, limit=24)
    if not items:
        return ""
    lines = ["Long-term research memory for this user (do not treat as secrets):"]
    for item in reversed(items[-16:]):
        kind = item.get("kind", "")
        title = item.get("title", "")
        snippet = (item.get("content") or "").replace("\n", " ")[:220]
        lines.append(f"- [{kind}] {title}: {snippet}")
    brief = _safe_text("\n".join(lines), limit=max_chars)
    return brief


def persist_research_run(
    *,
    user_id: str,
    session_id: str | None,
    state: Any,
) -> list[int]:
    """Save a completed (or partial) graph run into long-term memory."""
    uid = ensure_user(user_id)
    payload = state.model_dump() if hasattr(state, "model_dump") else dict(state)
    analysis = payload.get("analysis_payload") or {}
    paper_title = analysis.get("title") or "Untitled paper"
    paper_id = analysis.get("paper_id") or "unknown"
    reviews = payload.get("reviews") or []
    recs: dict[str, int] = {}
    for review in reviews:
        rec = review.get("recommendation", "unknown")
        recs[rec] = recs.get(rec, 0) + 1

    findings: list[str] = []
    findings.extend(f"Claim: {c}" for c in analysis.get("claims") or [])
    findings.extend(f"Limitation: {lim}" for lim in analysis.get("limitations") or [])

    created: list[int] = []
    with get_conn() as conn:
        if session_id:
            conn.execute(
                """
                UPDATE sessions
                SET title = ?, updated_at = ?, status = ?
                WHERE session_id = ? AND user_id = ?
                """,
                (
                    _safe_text(paper_title, limit=200),
                    _now(),
                    "partial" if payload.get("partial_output") else "completed",
                    session_id,
                    uid,
                ),
            )
        created.append(
            _insert_item(
                conn,
                user_id=uid,
                session_id=session_id,
                kind=KIND_PAPER,
                title=f"{paper_id}: {paper_title}",
                content=json.dumps(
                    {
                        "paper_id": paper_id,
                        "title": paper_title,
                        "sections": analysis.get("sections_covered", []),
                        "claims": analysis.get("claims", []),
                        "limitations": analysis.get("limitations", []),
                    },
                    ensure_ascii=True,
                ),
                metadata={"paper_id": paper_id, "source": "analyzer"},
            )
        )
        if findings:
            created.append(
                _insert_item(
                    conn,
                    user_id=uid,
                    session_id=session_id,
                    kind=KIND_FINDING,
                    title=f"Analyzer findings — {paper_id}",
                    content="\n".join(findings),
                    metadata={"paper_id": paper_id, "source": "analyzer"},
                )
            )
        review_lines = [
            f"Reviewer {r.get('reviewer_id')}: {r.get('recommendation')} "
            f"(confidence {r.get('confidence')}) — {r.get('expertise')}"
            for r in reviews
        ]
        created.append(
            _insert_item(
                conn,
                user_id=uid,
                session_id=session_id,
                kind=KIND_OUTPUT,
                title=f"Independent reviews ({len(reviews)})",
                content="\n".join(review_lines) or "No reviews",
                metadata={"count": len(reviews), "tally": recs},
            )
        )
        meta = payload.get("meta_analysis") or payload.get("final_report") or ""
        if meta:
            created.append(
                _insert_item(
                    conn,
                    user_id=uid,
                    session_id=session_id,
                    kind=KIND_OUTPUT,
                    title="Meta-analysis report",
                    content=meta,
                    metadata={"partial": bool(payload.get("partial_output"))},
                )
            )
        created.append(
            _insert_item(
                conn,
                user_id=uid,
                session_id=session_id,
                kind=KIND_SUMMARY,
                title=f"Session summary — {paper_id}",
                content=(
                    f"Paper: {paper_title}\n"
                    f"Reviews: {len(reviews)}\n"
                    f"Validated: {payload.get('is_validated')}\n"
                    f"Partial: {payload.get('partial_output')}\n"
                    f"Recommendation tally: {json.dumps(recs)}\n"
                ),
                metadata={"tally": recs, "terminated": payload.get("terminated")},
            )
        )
    return [i for i in created if i]
