"""Scout & Incubator pipeline for Agentit.

Ingests, verifies, classifies, and manages ecosystem tools, repos, tweets,
and skills before promoting them into Agentit's architecture.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import yaml
from pathlib import Path
from typing import Any

INCUBATOR_DIR = Path(__file__).resolve().parents[1] / "incubator"
CANDIDATES_FILE = INCUBATOR_DIR / "candidates.yaml"
REJECTED_FILE = INCUBATOR_DIR / "rejected.yaml"


def _slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "-", slug)[:50]


def load_candidates() -> dict[str, Any]:
    if not CANDIDATES_FILE.is_file():
        return {"version": 1, "candidates": []}
    try:
        data = yaml.safe_load(CANDIDATES_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {"version": 1, "candidates": []}


def save_candidates(data: dict[str, Any]) -> None:
    INCUBATOR_DIR.mkdir(parents=True, exist_ok=True)
    content = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

    fd, temp_path_str = tempfile.mkstemp(prefix=".cand-tmp-", dir=INCUBATOR_DIR, text=True)
    temp_path = Path(temp_path_str)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(fd)
        os.replace(temp_path, CANDIDATES_FILE)
        os.chmod(CANDIDATES_FILE, 0o600)
    finally:
        temp_path.unlink(missing_ok=True)


def load_rejected() -> dict[str, Any]:
    if not REJECTED_FILE.is_file():
        return {"version": 1, "rejected": []}
    try:
        data = yaml.safe_load(REJECTED_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {"version": 1, "rejected": []}


def save_rejected(data: dict[str, Any]) -> None:
    INCUBATOR_DIR.mkdir(parents=True, exist_ok=True)
    content = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

    fd, temp_path_str = tempfile.mkstemp(prefix=".rej-tmp-", dir=INCUBATOR_DIR, text=True)
    temp_path = Path(temp_path_str)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(fd)
        os.replace(temp_path, REJECTED_FILE)
        os.chmod(REJECTED_FILE, 0o600)
    finally:
        temp_path.unlink(missing_ok=True)


def add_candidate(url_or_claim: str, cand_type: str = "evaluated_idea") -> dict[str, Any]:
    data = load_candidates()
    cand_id = _slugify(url_or_claim.split("/")[-1] if "/" in url_or_claim else url_or_claim)
    if not cand_id:
        cand_id = f"candidate-{len(data['candidates']) + 1}"

    candidate = {
        "id": cand_id,
        "source": url_or_claim,
        "claim": "Scouted ecosystem idea/tool",
        "type": cand_type,
        "status": "incubating",
        "decision": "pending_evaluation",
    }

    # Avoid duplicate additions
    for existing in data["candidates"]:
        if existing.get("id") == cand_id or existing.get("source") == url_or_claim:
            return existing

    data["candidates"].append(candidate)
    save_candidates(data)
    return candidate


def reject_candidate(cand_id: str, reason: str) -> bool:
    candidates_data = load_candidates()
    rejected_data = load_rejected()

    found = None
    remaining = []
    for item in candidates_data.get("candidates", []):
        if item.get("id") == cand_id:
            found = item
        else:
            remaining.append(item)

    if not found:
        return False

    candidates_data["candidates"] = remaining
    found["reason"] = reason
    found["decision"] = "rejected"
    rejected_data.setdefault("rejected", []).append(found)

    save_candidates(candidates_data)
    save_rejected(rejected_data)
    return True


def inspect_candidate(cand_id: str) -> dict[str, Any] | None:
    data = load_candidates()
    for item in data.get("candidates", []):
        if item.get("id") == cand_id:
            return item
    rej = load_rejected()
    for item in rej.get("rejected", []):
        if item.get("id") == cand_id:
            return item
    return None
