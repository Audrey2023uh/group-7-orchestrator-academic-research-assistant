(() => {
  let userId = null;
  let sessionId = null;

  const $ = (id) => document.getElementById(id);
  const statusEl = $("status");
  const logEl = $("liveLog");
  const resultsEl = $("results");

  function setStatus(msg) {
    statusEl.textContent = msg;
  }

  function appendLog(line) {
    logEl.textContent += line + "\n";
    logEl.scrollTop = logEl.scrollHeight;
  }

  async function api(path, options = {}) {
    const res = await fetch(path, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    if (res.status === 204) return null;
    return res.json();
  }

  async function boot() {
    const me = await api("/api/me");
    userId = me.user_id;
    $("userLabel").textContent = userId;
    const created = await api("/api/sessions", {
      method: "POST",
      body: JSON.stringify({ title: "Live research session" }),
    });
    sessionId = created.session_id;
    await refreshSessions();
    await refreshMemory();
    await refreshChat();
    setStatus("Ready");
  }

  async function refreshSessions() {
    const data = await api("/api/sessions");
    const list = $("sessionList");
    list.innerHTML = "";
    (data.sessions || []).forEach((s) => {
      const li = document.createElement("li");
      if (s.session_id === sessionId) li.classList.add("active");
      li.innerHTML = `<div><div>${escapeHtml(s.title || "Session")}</div><div class="meta">${escapeHtml(s.status)} · ${escapeHtml(s.updated_at || "")}</div></div>`;
      const del = document.createElement("button");
      del.className = "tiny danger";
      del.textContent = "Delete";
      del.onclick = async (e) => {
        e.stopPropagation();
        if (!confirm("Delete this session and its short-term messages?")) return;
        await api(`/api/sessions/${encodeURIComponent(s.session_id)}`, { method: "DELETE" });
        if (sessionId === s.session_id) {
          const created = await api("/api/sessions", { method: "POST", body: JSON.stringify({ title: "Live research session" }) });
          sessionId = created.session_id;
        }
        await refreshSessions();
        await refreshChat();
        await refreshMemory();
      };
      li.onclick = async () => {
        sessionId = s.session_id;
        await refreshSessions();
        await refreshChat();
      };
      li.appendChild(del);
      list.appendChild(li);
    });
  }

  async function refreshMemory() {
    const kind = $("memKind").value;
    const q = kind ? `?kind=${encodeURIComponent(kind)}` : "";
    const data = await api(`/api/memory${q}`);
    const list = $("memoryList");
    list.innerHTML = "";
    (data.items || []).forEach((item) => {
      const li = document.createElement("li");
      li.innerHTML = `<div><div><strong>${escapeHtml(item.kind)}</strong> · ${escapeHtml(item.title)}</div><div class="meta">${escapeHtml((item.content || "").slice(0, 140))}</div></div>`;
      const del = document.createElement("button");
      del.className = "tiny danger";
      del.textContent = "Delete";
      del.onclick = async () => {
        await api(`/api/memory/${item.id}`, { method: "DELETE" });
        await refreshMemory();
      };
      li.appendChild(del);
      list.appendChild(li);
    });
  }

  async function refreshChat() {
    if (!sessionId) return;
    const data = await api(`/api/sessions/${encodeURIComponent(sessionId)}/messages`);
    const chat = $("chat");
    chat.innerHTML = "";
    (data.messages || []).forEach((m) => {
      const div = document.createElement("div");
      div.className = `bubble ${m.role || "user"}`;
      div.textContent = m.content;
      chat.appendChild(div);
    });
    chat.scrollTop = chat.scrollHeight;
  }

  function escapeHtml(s) {
    return String(s || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  $("btnNewSession").onclick = async () => {
    const created = await api("/api/sessions", {
      method: "POST",
      body: JSON.stringify({ title: "Live research session" }),
    });
    sessionId = created.session_id;
    await refreshSessions();
    await refreshChat();
    setStatus("New session ready");
  };

  $("btnRefreshMem").onclick = () => refreshMemory();
  $("memKind").onchange = () => refreshMemory();

  $("btnClearAll").onclick = async () => {
    if (!confirm("Permanently delete ALL memory and sessions for this user?")) return;
    await api("/api/memory", { method: "DELETE" });
    const created = await api("/api/sessions", {
      method: "POST",
      body: JSON.stringify({ title: "Live research session" }),
    });
    sessionId = created.session_id;
    await refreshSessions();
    await refreshMemory();
    await refreshChat();
    resultsEl.textContent = "";
    logEl.textContent = "";
    setStatus("Memory cleared");
  };

  $("pinForm").onsubmit = async (e) => {
    e.preventDefault();
    await api("/api/memory", {
      method: "POST",
      body: JSON.stringify({
        title: $("pinTitle").value,
        content: $("pinContent").value,
        kind: $("pinKind").value,
        session_id: sessionId,
      }),
    });
    $("pinTitle").value = "";
    $("pinContent").value = "";
    await refreshMemory();
  };

  $("chatForm").onsubmit = async (e) => {
    e.preventDefault();
    const content = $("chatInput").value.trim();
    if (!content || !sessionId) return;
    await api(`/api/sessions/${encodeURIComponent(sessionId)}/messages`, {
      method: "POST",
      body: JSON.stringify({ content, role: "user" }),
    });
    $("chatInput").value = "";
    await refreshChat();
  };

  $("btnRun").onclick = async () => {
    const btn = $("btnRun");
    btn.disabled = true;
    logEl.textContent = "";
    resultsEl.textContent = "";
    setStatus("Running multi-agent workflow…");
    try {
      const payload = {
        session_id: sessionId,
        research_question: $("question").value,
        paper_text: $("paperText").value,
        target_reviewers: Number($("reviewers").value || 5),
        max_rounds: Number($("rounds").value || 5),
        use_bundled_paper: $("useBundled").checked,
      };
      const res = await fetch("/api/research/stream", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(await res.text());
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let finalState = null;
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() || "";
        for (const part of parts) {
          const line = part.split("\n").find((l) => l.startsWith("data: "));
          if (!line) continue;
          const data = JSON.parse(line.slice(6));
          if (data.type === "start") {
            sessionId = data.session_id || sessionId;
            appendLog("session " + sessionId);
          } else if (data.type === "node") {
            appendLog(JSON.stringify(data.event));
            const nodes = Object.keys(data.event || {});
            if (nodes.length) setStatus("Node: " + nodes.join(", "));
          } else if (data.type === "final") {
            finalState = data.state;
          } else if (data.type === "done") {
            setStatus("Completed — long-term memory updated");
          }
        }
      }
      if (finalState) {
        const reviews = finalState.reviews || [];
        resultsEl.textContent =
          `validated=${finalState.is_validated} reviews=${reviews.length} partial=${finalState.partial_output}\n\n` +
          (finalState.meta_analysis || finalState.final_report || "");
      }
      await refreshSessions();
      await refreshMemory();
      await refreshChat();
    } catch (err) {
      setStatus("Error: " + err.message);
      appendLog(String(err));
    } finally {
      btn.disabled = false;
    }
  };

  boot().catch((err) => setStatus("Boot failed: " + err.message));
})();
