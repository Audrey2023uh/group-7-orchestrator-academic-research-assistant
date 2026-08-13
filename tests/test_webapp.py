"""API smoke tests for the interactive live application."""
from __future__ import annotations

from pathlib import Path

import memory.store as store
from fastapi.testclient import TestClient

from webapp import app


def test_health_and_research_flow(tmp_path):
    store.configure(tmp_path / "api_memory.db")
    client = TestClient(app)

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["ok"] is True

    page = client.get("/")
    assert page.status_code == 200
    assert b"Launch workflow" in page.content

    me = client.get("/api/me")
    assert me.status_code == 200
    assert me.json()["user_id"].startswith("usr_")

    session = client.post("/api/sessions", json={"title": "API session"}).json()
    sid = session["session_id"]

    run = client.post(
        "/api/research",
        json={
            "session_id": sid,
            "research_question": "Summarize governance findings",
            "target_reviewers": 2,
            "max_rounds": 5,
            "use_bundled_paper": True,
        },
    )
    assert run.status_code == 200, run.text
    body = run.json()
    assert body["reviews"] == 2
    assert body["validated"] is True
    assert "meta_analysis" in body

    mem = client.get("/api/memory").json()["items"]
    assert any(i["kind"] == "reviewed_paper" for i in mem)

    # Restart-like reconfigure should still see same DB file contents
    store._initialized_for = None
    store.configure(tmp_path / "api_memory.db")
    mem2 = client.get("/api/memory").json()["items"]
    assert len(mem2) >= 1

    wipe = client.delete("/api/memory")
    assert wipe.status_code == 200
    assert client.get("/api/memory").json()["items"] == []
