"""Small Ollama client; no third-party runtime dependencies."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "qwen2.5:0.5b-base"
INSTRUCT = "qwen2.5:0.5b-instruct"
OPTIONS = {"temperature": 0, "seed": 42, "num_predict": 256, "num_ctx": 2048}


def api(endpoint, payload=None):
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    if not host.startswith(("http://", "https://")):
        host = "http://" + host
    data = None if payload is None else json.dumps(payload).encode()
    request = Request(host + "/api/" + endpoint, data=data,
                      headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=180) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"Ollama {endpoint}: HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError) as exc:
        raise RuntimeError("Cannot reach Ollama. See setup.md: start `ollama serve`, "
                           "then run `python scripts/setup.py` before retrying.") from exc


def preflight():
    tags = api("tags")["models"]
    by_name = {m["name"]: m for m in tags}
    missing = [m for m in (BASE, INSTRUCT) if m not in by_name]
    if missing:
        raise RuntimeError("Missing models: " + ", ".join(missing) +
                           ". See setup.md and run `python scripts/setup.py`.")
    return {"ollama_version": api("version").get("version"),
            "models": {m: by_name[m] for m in (BASE, INSTRUCT)}}


def prompt_for(excerpt, task):
    return task + "\n\nSupplied text:\n<announcement>\n" + excerpt + "\n</announcement>\n\nAnswer:\n"


def run_case(excerpt, model, case, task):
    """One fresh request; preserve the complete raw response and exact input."""
    if model not in (BASE, INSTRUCT):
        raise ValueError("Choose BASE or INSTRUCT.")
    environment = preflight()
    prompt = prompt_for(excerpt, task)
    payload = {"model": model, "stream": False, "options": dict(OPTIONS), "keep_alive": "5m"}
    if model == BASE:
        endpoint = "generate"
        payload.update(prompt=prompt, raw=True)
    else:
        endpoint = "chat"
        payload["messages"] = [{"role": "user", "content": prompt}]
    print(f"Live Ollama request: {model} / {case} at "
          f"{datetime.now(timezone.utc).isoformat()}", flush=True)
    response = api(endpoint, payload)
    output = response.get("response", "") if model == BASE else response.get("message", {}).get("content", "")
    timestamp = datetime.now(timezone.utc)
    record = {"case": case, "timestamp_utc": timestamp.isoformat(),
              "excerpt_sha256": hashlib.sha256(excerpt.encode()).hexdigest(),
              "environment": environment, "endpoint": endpoint, "request": payload,
              "response": response, "output": output}
    directory = ROOT / "results"
    directory.mkdir(exist_ok=True)
    safe_case = "".join(c if c.isalnum() or c in "-_" else "_" for c in case)
    path = directory / f"{timestamp:%Y%m%dT%H%M%S%fZ}-{safe_case}.json"
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(output)
    if response.get("done_reason") == "length":
        print("\n[Output reached the 256-token limit; mark it truncated.]")
    print(f"\nSaved run: {path.name}")
    return record
