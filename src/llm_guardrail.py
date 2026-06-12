import html
import json
import threading
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Deque, Optional


VALID_STATUSES = {"passed", "blocked"}


@dataclass(frozen=True)
class Entry:
    """A single LLM interaction record."""

    timestamp: str  # ISO‑8601 UTC string
    module: str
    prompt: str
    response: str
    status: str

    @staticmethod
    def create(module: str, prompt: str, response: str, status: str) -> "Entry":
        """Factory that validates inputs and stamps the entry."""
        if status not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        ts = datetime.now(timezone.utc).isoformat()
        return Entry(timestamp=ts, module=module, prompt=prompt, response=response, status=status)


class DashboardStore:
    """Thread‑safe in‑memory store for the last 100 LLM entries."""

    def __init__(self, maxlen: int = 100):
        self._entries: Deque[Entry] = deque(maxlen=maxlen)
        self._lock = threading.Lock()

    def add_entry(self, module: str, prompt: str, response: str, status: str) -> None:
        """Validate and store a new entry."""
        entry = Entry.create(module, prompt, response, status)
        with self._lock:
            self._entries.append(entry)

    def get_entries(self) -> List[Entry]:
        """Return entries ordered from newest to oldest."""
        with self._lock:
            return list(reversed(self._entries))


def generate_dashboard_html(entries: List[Entry]) -> str:
    """Render a minimal HTML dashboard for the given entries."""
    rows = []
    for e in entries:
        row = (
            f"<tr>"
            f"<td>{html.escape(e.timestamp)}</td>"
            f"<td>{html.escape(e.module)}</td>"
            f"<td>{html.escape(e.prompt)}</td>"
            f"<td>{html.escape(e.response)}</td>"
            f"<td>{html.escape(e.status)}</td>"
            f"</tr>"
        )
        rows.append(row)

    table_body = "\n".join(rows) if rows else "<tr><td colspan='5'>No entries yet.</td></tr>"
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LLM Guardrail Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; font-family: monospace; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>LLM Guardrail – Last {len(entries)} Responses</h1>
    <table>
        <thead>
            <tr>
                <th>Timestamp (UTC)</th>
                <th>Module</th>
                <th>Prompt</th>
                <th>Response</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {table_body}
        </tbody>
    </table>
</body>
</html>"""
    return html_doc


class _DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves the dashboard HTML."""

    # The store is injected as a class attribute before server start.
    store: Optional[DashboardStore] = None

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return
        entries = self.store.get_entries() if self.store else []
        html_content = generate_dashboard_html(entries).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_content)))
        self.end_headers()
        self.wfile.write(html_content)

    def log_message(self, format: str, *args) -> None:  # suppress console noise
        return


def run_server(host: str = "127.0.0.1", port: int = 8000, store: Optional[DashboardStore] = None) -> None:
    """Start a blocking HTTP server that serves the live dashboard."""
    if store is None:
        store = DashboardStore()
    _DashboardHandler.store = store
    server = HTTPServer((host, port), _DashboardHandler)
    print(f"LLM Guardrail dashboard listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server.server_close()
