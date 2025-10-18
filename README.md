```markdown
# BGI25 Hackathon — ASI1-mini demo

This repository contains a minimal demo and example client for calling the ASI1-mini model hosted on ASICloud:
https://asicloud.cudos.org/inference/models/asi1-mini

Overview
- Language: Python 3.11+
- Components: CLI client, simple FastAPI demo, Dockerfile, CI, and unit tests (mocked)

Quickstart (local)
1. Create virtualenv:
   python -m venv .venv && source .venv/bin/activate
2. Install dependencies:
   pip install -r requirements.txt
3. Set env vars:
   - ASICLOUD_INFERENCE_URL (defaults to the model page URL)
   - ASICLOUD_API_KEY (if required)
4. Run CLI example:
   python -m src.client.asi_client --text "Hello world"

Run the demo API (FastAPI)
1. Start locally:
   uvicorn src.app.demo_api:app --reload --port 8000
2. POST JSON to /infer e.g.:
   curl -X POST -H "Content-Type: application/json" -d '{"input": "Hello"}' http://localhost:8000/infer

Docker
- Build: docker build -t bgi25-asi-demo .
- Run: docker run -e ASICLOUD_API_KEY="$KEY" -p 8000:8000 bgi25-asi-demo

Testing & CI
- Tests are in the tests/ directory and mock external network calls.
- CI runs lint (black) and pytest.

Security & Notes
- Do NOT commit your ASICLOUD_API_KEY. Use environment variables or CI secrets.
- Confirm the exact API schema for ASI1-mini on ASICloud before production use.
- In CI, tests do not call the external API; they use mocks.

License
This project is licensed under the MIT License. See LICENSE for details.
```
