# agents.local.md

## Session context
- Repository: reachy_mini_retail_assistant
- Robot type: Lite (USB connection to laptop)
- Preferred implementation language: Python
- Priority: executable implementation progress over planning-only updates

## Architecture
- **Edge Backend** (`reachy_edge/`) — FastAPI on port 8000, serves product search, promos, store info
- **Karen Whisperer** (`../reachy_mini_karen_whisperer/`) — robot conversation app that calls the Edge Backend API via HTTP tools in the `retail_assistant` profile
- The KW profile tools (`lookup_product`, `get_active_promos`, `get_store_info`) call `RETAIL_API_URL` (default `http://localhost:8000`)

## Environment notes
- reachy-mini SDK v1.2.13 installed
- Port 8000 may be blocked on Windows; use 8001 or 8002 as fallback
- OpenAI key not needed for API/tool testing (only for `/interact` LLM flow)
- If dependencies cannot be installed due network/proxy constraints, run static validation (`compileall`) and keep code import-safe.
- Keep runtime backend choices configurable via environment variables.
