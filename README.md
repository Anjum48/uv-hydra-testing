# uv-hydra-testing

Small reproducibility project for debugging Hydra override behavior when dependencies are installed with `uv` vs `pip`.

## What this project does

- Runs a single Hydra entrypoint (`entrypoint.py`) using `config/config.yaml`.
- Initializes a ClearML task with `task_name` from `run.run_name`.
- Writes Hydra run artifacts under `output/<timestamp>/`.
- Captures effective overrides in `output/<timestamp>/.hydra/overrides.yaml`.

This repository is intentionally minimal so override behavior can be inspected without unrelated application complexity.

## Repository layout

```
entrypoint.py                 # Hydra entrypoint
config/config.yaml            # Base app + Hydra runtime config
requirements.txt              # Pinned dependencies
output/<timestamp>/.hydra/    # Generated Hydra artifacts per run
docs/                         # PRD, technical design, deploy, debug docs
```

## Prerequisites

- Windows PowerShell examples are shown below.
- Python must be compatible with packages pinned in `requirements.txt`.

## Setup and run with pip

```powershell
python -m venv .venv_pip
.\.venv_pip\Scripts\Activate.ps1
pip install -r .\requirements.txt
python .\entrypoint.py
```

Run with an override:

```powershell
python .\entrypoint.py run.run_name=McLaren
```

## Setup and run with uv

```powershell
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -r .\requirements.txt
python .\entrypoint.py
```

Run with an override:

```powershell
python .\entrypoint.py run.run_name=McLaren
```

## Verify Hydra override behavior

After each run, inspect the newest folder in `output/`.

Expected files:

- `.hydra/config.yaml` (resolved application config)
- `.hydra/hydra.yaml` (resolved Hydra internals)
- `.hydra/overrides.yaml` (exact CLI overrides passed)

Example expected content in `.hydra/overrides.yaml` when run with `run.run_name=McLaren`:

```yaml
- run.run_name=McLaren
```

## Typical comparison workflow (pip vs uv)

1. Run once in `pip` environment with the same override(s).
2. Run once in `uv` environment with the same override(s).
3. Compare each run's `.hydra/overrides.yaml` and `.hydra/config.yaml`.
4. If behavior differs, compare package versions and Python versions between environments.

## Notes

- Existing sample run folders are already checked in under `output/` for reference.
- `entrypoint.py` prints the resolved Hydra config to stdout and initializes ClearML.
- Additional details: see `docs/PRD.md`, `docs/TDD.md`, `docs/deploy.md`, and `docs/debug-playbook.md`.