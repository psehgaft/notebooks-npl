# notebooks-npl

Jupyter notebooks for natural language processing (NLP) experiments, created during the Red Hat AI Odyssey 2025 programme (team *deep-fried-learning*). The repository collects small, self-contained experiments on intent detection and transformer-based text classification, together with the datasets, pipelines and data-factory material that support them.

> The previous README was the default GitLab project template. This version documents the actual content of the repository.

## Contents

### Notebooks (repository root)

| Notebook | What it does |
| --- | --- |
| `Intents Showcase.ipynb` | Showcase of intent detection: explores how user utterances can be classified into intents for a conversational assistant. |
| `Text Classification Transformers.ipynb` | Text classification with transformer models: prepares data, fine-tunes/evaluates a transformer classifier and inspects the results. |
| `Untitled.ipynb` | Scratch notebook that connects Python to a CouchDB service (`pip install couchdb`, `couchdb.Server(...)`) — kept as a connectivity experiment for the data-factory work. |

### Supporting directories

| Directory | Purpose |
| --- | --- |
| `datasets/` | Datasets used by the notebooks. |
| `pipelines/` | Pipeline definitions and related automation. |
| `generative-ai/` | Generative AI experiments. |
| `data-factory/` | Data-factory material used to prepare and move data. |
| `ai-odyssey-data-factory/` | AI Odyssey data-factory workspace. |

## Getting started

You need Python 3 and Jupyter (Lab or Notebook):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jupyter
jupyter lab
```

Then open the notebook you want to run. Each notebook installs or imports the extra libraries it needs (for example `transformers` for the classification notebook or `couchdb` for the CouchDB experiment), so run the cells from top to bottom the first time.

## A note on the committed virtual environment

This repository also contains a Python virtual environment committed by mistake (`bin/`, `lib/`, `etc/`, `share/` and `pyvenv.cfg` at the root). Do **not** reuse it — it is machine-specific. Create a fresh environment as shown above, and consider adding those paths to `.gitignore` in a future cleanup.

## Origin

The project started on Red Hat's internal GitLab (`ai-odyssey-2025/deep-fried-learning/notebooks-npl`) and is mirrored here for reference.
