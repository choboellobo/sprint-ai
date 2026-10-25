#!/usr/bin/env python3
"""Serve a read-only sprint board from a project's Markdown files."""

import argparse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import webbrowser


STATUSES = ("Backlog", "To Do", "In Progress", "In QA", "Waiting For", "Done")
UI_DIR = Path(__file__).resolve().parent / "ui"


def cells(line):
    return [part.strip() for part in line.strip().strip("|").split("|")]


def tables(markdown):
    lines = markdown.splitlines()
    for index in range(len(lines) - 1):
        if not lines[index].lstrip().startswith("|"):
            continue
        headers = cells(lines[index])
        separators = cells(lines[index + 1])
        if len(headers) != len(separators) or not all(
            re.fullmatch(r":?-{3,}:?", item) for item in separators
        ):
            continue
        rows = []
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
            values = cells(lines[cursor])
            if len(values) == len(headers):
                rows.append(dict(zip(headers, values)))
            cursor += 1
        yield rows, set(headers)


def read_text(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def value(row, name):
    return next((text for key, text in row.items() if key.lower() == name.lower()), "")


def normalize(value_text):
    return "" if value_text in ("—", "-", "–") else value_text.strip()


def backlog_items(markdown):
    for rows, headers in tables(markdown):
        if {"ID", "Story"}.issubset(headers):
            return {
                value(row, "ID"): {
                    "id": value(row, "ID"),
                    "story": value(row, "Story"),
                    "areas": normalize(value(row, "Areas")),
                    "plan": normalize(value(row, "Plan")),
                }
                for row in rows
                if value(row, "ID")
            }

    # Older backlogs used numbered stories instead of a table.
    result = {}
    for line in markdown.splitlines():
        match = re.match(r"^\s*(\d+[a-z]?)\.\s+(.+)$", line)
        if not match:
            continue
        story_id, story = match.groups()
        plan_match = re.search(r"\s+Plan:\s+(\S+)", story)
        plan = plan_match.group(1) if plan_match else ""
        story = re.split(r"\s+(?:Plan|Requires):", story, maxsplit=1)[0]
        result[story_id] = {"id": story_id, "story": story, "areas": "", "plan": plan}
    return result


def plan_details(project, reference):
    reference = normalize(reference).strip("`")
    link = re.fullmatch(r"\[[^]]+\]\(([^)]+)\)", reference)
    if link:
        reference = link.group(1)
    if not reference:
        return {"path": "", "criteria": [], "verification": []}
    path = (project / reference).resolve()
    if not path.is_relative_to(project) or path.suffix.lower() != ".md" or not path.is_file():
        return {"path": reference, "criteria": [], "verification": []}
    if path.stat().st_size > 200_000:
        return {"path": reference, "criteria": [], "verification": []}
    details = {"path": reference, "criteria": [], "verification": []}
    section = ""
    for line in read_text(path).splitlines():
        if line.startswith("## "):
            heading = line[3:].strip().lower()
            section = (
                "criteria" if heading in ("acceptance criteria", "criterios de aceptación")
                else "verification" if heading in ("verification", "verificación")
                else ""
            )
        elif section and re.match(r"^\s*[-*]\s+", line):
            details[section].append(re.sub(r"^\s*[-*]\s+(?:\[[ xX]\]\s*)?", "", line))
    return details


def metadata(markdown, label):
    match = re.search(rf"^{re.escape(label)}:\s*(.+)$", markdown, re.MULTILINE)
    return match.group(1).strip() if match else ""


def sprint_state(project, path, backlog, include_backlog=False, exclude_backlog_ids=None):
    sprint_text = read_text(path)
    sprint_rows = []
    for rows, headers in tables(sprint_text):
        if {"ID", "Status"}.issubset(headers):
            sprint_rows = rows
            break

    items = []
    scheduled = set()
    for row in sprint_rows:
        story_id = value(row, "ID")
        if not story_id:
            continue
        scheduled.add(story_id)
        original = backlog.get(story_id, {})
        reference = normalize(value(row, "Plan")) or original.get("plan", "")
        status = value(row, "Status") or "To Do"
        items.append({
            "id": story_id,
            "story": value(row, "Story") or original.get("story", ""),
            "areas": normalize(value(row, "Areas")) or original.get("areas", ""),
            "status": status,
            "nextAction": normalize(value(row, "Next action")),
            "plan": plan_details(project, reference),
        })
    if include_backlog:
        for story_id, row in backlog.items():
            if story_id not in scheduled and story_id not in (exclude_backlog_ids or set()):
                items.append({**row, "status": "Backlog", "nextAction": "", "plan": plan_details(project, row["plan"])})

    heading = re.search(r"^#\s+Sprint:\s*(.+)$", sprint_text, re.MULTILINE)
    counts = {status: sum(item["status"] == status for item in items) for status in STATUSES}
    return {
        "id": metadata(sprint_text, "ID") or (path.stem if path.name != "SPRINT.md" else ""),
        "sprint": heading.group(1) if heading else "Sin sprint activo",
        "goal": metadata(sprint_text, "Goal"),
        "dates": metadata(sprint_text, "Dates"),
        "milestone": metadata(sprint_text, "Milestone"),
        "hasSprint": bool(sprint_text),
        "items": items,
        "counts": counts,
        "areas": sorted({area.strip() for item in items for area in item["areas"].split(",") if area.strip()}),
    }


def milestone_items(markdown, sprints):
    for rows, headers in tables(markdown):
        if {"ID", "Name", "Goal", "Status", "Target", "Sprints"}.issubset(headers):
            result = []
            by_id = {sprint["id"]: sprint for sprint in sprints if sprint["id"]}
            for row in rows:
                sprint_ids = [part.strip() for part in normalize(value(row, "Sprints")).split(",") if part.strip()]
                stories = {}
                for sprint_id in sprint_ids:
                    for item in by_id.get(sprint_id, {}).get("items", []):
                        if item["status"] != "Backlog":
                            stories[item["id"]] = item["status"]
                result.append({
                    "id": value(row, "ID"),
                    "name": value(row, "Name"),
                    "goal": value(row, "Goal"),
                    "status": value(row, "Status"),
                    "target": normalize(value(row, "Target")),
                    "sprintIds": sprint_ids,
                    "total": len(stories),
                    "done": sum(status == "Done" for status in stories.values()),
                })
            return result
    return []


def load_state(project):
    project = Path(project).resolve()
    backlog = backlog_items(read_text(project / "BACKLOG.md"))
    archive_dir = project / "sprints"
    history = [
        sprint_state(project, path, backlog)
        for path in sorted(archive_dir.glob("*.md"), reverse=True)
        if path.is_file() and path.resolve().is_relative_to(project)
    ] if archive_dir.is_dir() else []
    latest_archived_status = {}
    for sprint in history:
        for item in sprint["items"]:
            latest_archived_status.setdefault(item["id"], item["status"])
    finished_ids = {story_id for story_id, status in latest_archived_status.items() if status == "Done"}
    current = sprint_state(project, project / "SPRINT.md", backlog, include_backlog=True, exclude_backlog_ids=finished_ids)
    milestones = milestone_items(read_text(project / "MILESTONES.md"), list(reversed(history)) + [current])
    return {
        **current,
        "project": project.name,
        "history": history,
        "milestones": milestones,
        "updated": datetime.now().astimezone().isoformat(timespec="seconds"),
    }


def serve(project, port, open_browser):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = urlsplit(self.path).path
            if route == "/api/state":
                body = json.dumps(load_state(project), ensure_ascii=False).encode("utf-8")
                kind = "application/json; charset=utf-8"
            elif route in ("/", "/style.css", "/app.js"):
                name = "index.html" if route == "/" else route[1:]
                body = (UI_DIR / name).read_bytes()
                kind = {"index.html": "text/html", "style.css": "text/css", "app.js": "text/javascript"}[name] + "; charset=utf-8"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format_string, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"Tablero: {url}", flush=True)
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description="Open a local sprint-ai board")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project directory with BACKLOG.md or SPRINT.md")
    parser.add_argument("--port", type=int, default=0, help="Local port (default: automatic)")
    parser.add_argument("--no-open", action="store_true", help="Print URL without opening a browser")
    args = parser.parse_args()
    project = args.project.resolve()
    if not project.is_dir() or not any((project / name).is_file() for name in ("BACKLOG.md", "SPRINT.md", "MILESTONES.md")):
        parser.error("--project must contain BACKLOG.md, SPRINT.md, or MILESTONES.md")
    serve(project, args.port, not args.no_open)


if __name__ == "__main__":
    main()
