"""Run before presenting: pull models, verify API, and check fixed excerpts."""
import json
import shutil
import subprocess

from demo import BASE, INSTRUCT, ROOT, preflight


def main():
    if not shutil.which("ollama"):
        raise SystemExit("Install Ollama from https://ollama.com/download, then start it.")
    for model in (BASE, INSTRUCT):
        subprocess.run(["ollama", "pull", model], check=True)
    environment = preflight()
    for name in ("infosecon", "times_square"):
        text = (ROOT / "data" / f"{name}.txt").read_text()
        if not text.strip():
            raise SystemExit(f"Empty excerpt: {name}")
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "setup.json").write_text(json.dumps(environment, indent=2) + "\n")
    print("Ready. Open the notebook and run from the top.")


if __name__ == "__main__":
    main()
