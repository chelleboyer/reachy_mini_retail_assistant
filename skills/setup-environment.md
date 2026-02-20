# setup-environment.md

## Purpose
Bootstrap the local development environment when `agents.local.md` is missing.

## Steps
1. Create Python virtual environment:
   - `python -m venv .venv`
2. Activate environment:
   - Linux/macOS: `source .venv/bin/activate`
   - Windows: `.venv\\Scripts\\activate`
3. Install edge dependencies:
   - `pip install -r reachy_edge/requirements.txt`
4. Optional editable install:
   - `pip install -e reachy_edge`
5. Verify imports:
   - `python -c "import reachy_edge; print('ok')"`
6. Run basic checks:
   - `python -m compileall reachy_edge`
   - `pytest -q reachy_edge/tests`

## Notes
- If package installation fails due network policy, proceed with static checks and continue implementation.
- Keep settings configurable via environment variables (`.env` with `pydantic-settings`).
