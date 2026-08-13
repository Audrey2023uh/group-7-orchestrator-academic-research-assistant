# Live Application Deployment

This repository's interactive application is a **Python FastAPI + LangGraph** service
(`webapp.py`). It cannot run as a pure static GitHub Pages site.

## Correct runtime

Deploy with any container/Python host:

- Docker locally: `docker compose up --build`
- Hugging Face Spaces (Docker SDK) using this Dockerfile
- Render using `render.yaml`

The GitHub Pages site under `docs/` is a professional landing page with a
**Launch Live App** button that points at the deployed runtime URL.

## Memory

- Backend: SQLite (`MEMORY_DB_PATH`, default `/data/memory.db` in containers)
- Short-term: session messages
- Long-term: reviewed papers, findings, decisions, agent outputs
- Isolated per user cookie (`ara_user_id`)
- Secrets are redacted and not stored
