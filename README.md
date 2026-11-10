# Small LLM Information Extraction

A compact, hands-on demonstration of structured information extraction using small language models. Compare base and instruction-tuned Qwen2.5-0.5B models to explore instruction following, evidence handling, and the limits of plausible-looking answers.

## Start Here

Open **[main.ipynb](main.ipynb)** for the tutorial:

1. **Triangle InfoSeCon:** Run Qwen2.5-0.5B Base on a straightforward conference announcement.
2. **Times Square:** Run the same base model on an event description containing missing admission-price information and conflicting years.
3. **Base vs. Instruct:** Run Qwen2.5-0.5B Instruct on the same Times Square excerpt and compare the responses against the source evidence.

The demonstration explores what changes when a model is instruction-tuned—and why a plausible response is not necessarily a reliable extraction.

## Live Execution

**The notebook runs local inference by default.** It does not load saved model responses.

Follow **[setup.md](setup.md)** for installation, virtual environment setup, Ollama model preparation, Jupyter kernel selection, and troubleshooting.

Open `main.ipynb` using the **Python (small-llm-information-extraction)** kernel, restart the kernel, and run all cells or execute them sequentially.

Each inference call:

- Sends a fresh request to the local Ollama server.
- Displays an execution timestamp.
- Records the full model response for later inspection.

Saved results are not used as response caches.

## Experiment Design

The task extracts event details, including the event name, location, date components, time, admission price, and conflicting years.

The Times Square example deliberately contains ambiguous evidence: December 31 is stated, the countdown targets 2027, and the description refers to New Year's Eve 2025. Neither event excerpt states an admission price.

The task instructs models to report missing information as **“Not stated”** and contradictory years as **“Conflicting”**, rather than inventing an answer.

Both model variants receive the same task instructions and generation settings:

| Configuration | Implementation |
|---|---|
| Base model | Qwen2.5-0.5B Base, Ollama `/api/generate` with `raw=True` |
| Instruction-tuned model | Qwen2.5-0.5B Instruct, Ollama `/api/chat` with the model's chat template |
| Temperature | 0 |
| Random seed | Fixed |
| Output limit | 256 tokens |
| Evaluation | Inspect responses against source evidence |

The experiment does not use schema enforcement, automatic repair, retry selection, or shared conversation history.

A fixed seed and temperature reduce variation but do not guarantee identical results across runtime versions or backends.

## Repository Structure

| Path | Purpose |
|---|---|
| `main.ipynb` | Live tutorial, prompts, model responses, and instructor rubric |
| `setup.md` | Installation, model preparation, execution, and troubleshooting |
| `scripts/demo.py` | Model requests, generation settings, and run recording |
| `scripts/setup.py` | Model downloads and environment preflight |
| `data/` | Frozen plain-text event excerpts |
| `results/` | Timestamped execution records and setup metadata |

The event excerpts are stored locally and checked against the notebook inputs to prevent silent changes. The demo does not fetch live event pages.

Execution records include exact inputs, unmodified responses, excerpt hashes, model digests, and runtime information.

## What to Observe

The tutorial illustrates three practical questions:

1. **Instruction following:** How does a base model behave compared with an instruction-tuned model?
2. **Evidence handling:** Does the model distinguish missing or contradictory information from supported facts?
3. **Application readiness:** What additional validation would be necessary before using extracted information in a real application?

An apparently successful extraction is an observation, not proof of model reliability.

## Scope and Limitations

This is an educational demonstration, not a comprehensive benchmark or production extraction pipeline.

The examples are intentionally small, and their outcomes should not be generalized into claims that instruction tuning always improves extraction accuracy.

The purpose is to illustrate how model behavior, task instructions, and evidence validation influence the journey from an AI model to a useful application.

## References

- [Ollama Generate API](https://docs.ollama.com/api/generate)
- [Ollama Chat API](https://docs.ollama.com/api/chat)
- [Qwen2.5-0.5B Base](https://ollama.com/library/qwen2.5:0.5b-base)
- [Qwen2.5-0.5B Instruct](https://ollama.com/library/qwen2.5:0.5b-instruct)
