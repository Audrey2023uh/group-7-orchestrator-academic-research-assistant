"""Persistent memory tests: isolation, redaction, restart survival, clear controls."""
from __future__ import annotations

from pathlib import Path

import memory.store as store
from memory.service import (
    approve_decision,
    clear_user_memory,
    delete_memory_item,
    get_or_create_session,
    list_memory,
    load_session_messages,
    pin_finding,
    save_message,
)
from main_system import run_system


def _fresh_db(tmp_path: Path):
    db = tmp_path / "memory.db"
    store.configure(db)
    return db


def test_short_and_long_term_memory_isolated(tmp_path):
    _fresh_db(tmp_path)
    a = get_or_create_session("usr_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", title="A")
    b = get_or_create_session("usr_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", title="B")
    save_message(a["user_id"], a["session_id"], "user", "Alice question")
    save_message(b["user_id"], b["session_id"], "user", "Bob question")
    pin_finding(a["user_id"], "Alice finding", "Important for Alice only")
    pin_finding(b["user_id"], "Bob finding", "Important for Bob only")

    assert [m["content"] for m in load_session_messages(a["user_id"], a["session_id"])] == [
        "Alice question"
    ]
    assert [m["content"] for m in load_session_messages(b["user_id"], b["session_id"])] == [
        "Bob question"
    ]
    assert all(i["title"].startswith("Alice") for i in list_memory(a["user_id"]))
    assert all(i["title"].startswith("Bob") for i in list_memory(b["user_id"]))


def test_secrets_are_not_stored(tmp_path):
    _fresh_db(tmp_path)
    session = get_or_create_session("usr_cccccccccccccccccccccccccccccccc")
    save_message(
        session["user_id"],
        session["session_id"],
        "user",
        "please remember api_key=sk-secret-demo-123 and password=hunter2",
    )
    msgs = load_session_messages(session["user_id"], session["session_id"])
    body = msgs[0]["content"]
    assert "sk-secret-demo-123" not in body
    assert "hunter2" not in body
    assert "REDACTED" in body or "api" in body.lower()


def test_memory_survives_reconfigure_restart(tmp_path):
    db = _fresh_db(tmp_path)
    session = get_or_create_session("usr_dddddddddddddddddddddddddddddddd", title="Persist me")
    pin_finding(session["user_id"], "Durable finding", "Should survive reopen")
    approve_decision(session["user_id"], "Use 5 reviewers", "User approved smaller demo run")

    # Simulate process restart: reset init flag and reconnect to same file
    store._initialized_for = None
    store.configure(db)
    items = list_memory(session["user_id"])
    titles = {i["title"] for i in items}
    assert "Durable finding" in titles
    assert "Use 5 reviewers" in titles
    assert Path(db).exists()


def test_clear_and_delete_controls(tmp_path):
    _fresh_db(tmp_path)
    session = get_or_create_session("usr_eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    pinned = pin_finding(session["user_id"], "Temp", "delete me")
    assert delete_memory_item(session["user_id"], pinned["id"]) is True
    assert list_memory(session["user_id"]) == []
    pin_finding(session["user_id"], "Again", "wipe later")
    cleared = clear_user_memory(session["user_id"])
    assert cleared["memory_items"] >= 1
    assert list_memory(session["user_id"]) == []


def test_graph_persists_research_memory(tmp_path):
    _fresh_db(tmp_path)
    uid = "usr_ffffffffffffffffffffffffffffffff"
    session = get_or_create_session(uid, title="Graph run")
    state = run_system(
        target_reviewers=3,
        max_rounds=5,
        user_id=uid,
        session_id=session["session_id"],
        user_notes="Focus on methodological rigor",
        persist_memory=True,
    )
    assert state.terminated is True
    assert len(state.reviews) == 3
    kinds = {i["kind"] for i in list_memory(uid)}
    assert "reviewed_paper" in kinds
    assert "agent_output" in kinds
    assert "session_summary" in kinds
