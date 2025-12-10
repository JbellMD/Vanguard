# Vanguard AI Eval Platform

MVP for an AI Evaluation Platform that runs prompts against multiple test cases, combines heuristic rules with an LLM judge, and stores results.

## Running locally (Docker + Postgres)

1. **Set your OpenAI API key** (PowerShell example):

   ```powershell
   $env:OPENAI_API_KEY = "your-key-here"
   ```

2. **Start the stack** from the repo root:

   ```bash
   docker compose -f infra/docker-compose.yml up --build
   ```

3. **Healthcheck**:

   - URL: <http://localhost:8000/health>

4. **Run an eval** (example request):

   - Endpoint: `POST http://localhost:8000/v1/evals/run`
   - Body:

     ```json
     {
       "prompt": "You are a helpful assistant.",
       "target_model": "stub-model-v1",
       "pass_threshold": 0.75,
       "test_cases": [
         { "input": "Say hello.", "expected_output": "hello" },
         { "input": "What is 2+2?", "expected_output": "4" }
       ]
     }
     ```

   You can send this with a tool like `curl`, Postman, or VS Code/IDE HTTP client.

## Running backend without Docker (sqlite)

From `backend/`:

```bash
pip install -r requirements.txt
# Set OPENAI_API_KEY in your shell
uvicorn app.main:app --reload
```

- Healthcheck: <http://localhost:8000/health>
- Eval run: `POST http://localhost:8000/v1/evals/run`
