# Setup for live notebook execution

The default is live inference against Ollama. Each inference cell sends a fresh request. Previous notebook outputs and `results/*.json` are records only; they are never replayed as model responses.

## Install the environment

Prerequisites: Python 3.10+, a terminal, and [Ollama](https://ollama.com/download) installed on the machine running the notebook kernel. Model downloads and Python package installation need internet access.

For a new checkout, clone the repository, then create the environment:

```sh
git clone https://github.com/manimalakumar/small-llm-information-extraction.git
cd small-llm-information-extraction
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --sys-prefix --name small-llm-information-extraction --display-name "Python (small-llm-information-extraction)"
```

For an existing checkout, skip `git clone` and change into its project folder before running the environment commands.

The dedicated kernel is installed inside this virtual environment. Select **Python (small-llm-information-extraction)** when opening the notebook. Launch Jupyter using this environment so it can discover that kernel.

## Start Ollama and prepare the models

Start the Ollama desktop application, or keep this command running in a separate terminal:

```sh
ollama serve
```

The default endpoint is `http://127.0.0.1:11434`. If `OLLAMA_HOST` was set for another project, unset it in the terminal that will launch Jupyter to use this local default:

```sh
unset OLLAMA_HOST
```

In the activated environment, prepare and verify the two models and fixed excerpt files:

```sh
python scripts/setup.py
```

This pulls `qwen2.5:0.5b-base` and `qwen2.5:0.5b-instruct`, checks the API and saved excerpts, and writes model metadata to `results/setup.json`. Existing local model data is reused by Ollama. Neither inference cell downloads models. After setup, the demo can run without internet using local Ollama.

## Run live

```sh
python -m jupyterlab main.ipynb
```

Choose **Restart Kernel and Run All Cells** for a complete fresh run, or execute cells in order for a presentation. The first cell checks the server, model availability, and saved inputs. Each inference cell prints **Live Ollama request**, the model, and a UTC timestamp before sending the request; its raw response appears directly below. The comparison table uses the responses returned during that kernel session. Save the main notebook to keep the new outputs.

`TASK` is editable in the notebook. Restart and run all cells after changing it. When changing either pasted announcement, update its matching file in `data/` too; the equality checks intentionally detect mismatches, ignoring trailing newlines. Missing prices and conflicting years are part of the exercise.

## Troubleshooting

- **Cannot reach Ollama:** start the app or `ollama serve`, check `OLLAMA_HOST`, and rerun the first cell. The kernel must be permitted to connect to the local server.
- **Missing models:** rerun `python scripts/setup.py` while Ollama is running.
- **Kernel not found / missing IPython:** activate `.venv`, rerun the dependency and kernel installation commands, and launch Jupyter with `python -m jupyterlab` from that environment.
- **Wrong working directory:** launch from this project folder; `scripts/` and `data/` must remain beside the notebook.
- **Output reaches 256 tokens:** the notebook flags truncation. This is an observed model behavior; setup or successful execution does not imply a correct model answer.

Outputs are saved in the main notebook. Timestamped JSON records in `results/` retain the exact request, response, excerpt hash, model digests, runtime version, and generation settings for inspection.
