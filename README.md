# Vanguard AI Eval Platform

MVP for an AI Evaluation Platform that runs prompts against multiple test cases, combines heuristic rules with an LLM judge, and stores results.

## Running locally (Docker + Postgres)

1. **Set your environment variables** (PowerShell examples):

   ```powershell
   $env:OPENAI_API_KEY = "your-openai-key-here"
   $env:API_KEY = "dev-secret"   # optional simple API key for /v1/* endpoints
   ```

2. **Start the stack** from the `infra/` directory:

   ```bash
   cd infra
   docker compose up --build
   ```

3. **Healthcheck**:

   - URL: <http://localhost:8000/health>

4. **Run an eval** (example request):

   - Endpoint: `POST http://localhost:8000/v1/evals/run`
   - Example `curl` (PowerShell-style caret line breaks):

     ```bash
     curl -X POST "http://localhost:8000/v1/evals/run" ^
       -H "Content-Type: application/json" ^
       -H "x-api-key: dev-secret" ^
       -H "X-Project-Id: my-project-id" ^
       --data-raw ^
     "{
       \"prompt\": \"You are a helpful assistant.\",
       \"target_model\": \"stub-model-v1\",
       \"pass_threshold\": 0.75,
       \"test_cases\": [
         { \"input\": \"Say hello.\", \"expected_output\": \"hello\" },
         { \"input\": \"What is 2+2?\", \"expected_output\": \"4\" }
       ]
     }"
     ```

     You can also use Postman or your IDE's HTTP client.

## Running backend without Docker (sqlite)

From `backend/`:

```bash
pip install -r requirements.txt
# Set OPENAI_API_KEY in your shell
uvicorn app.main:app --reload
```

- Healthcheck: <http://localhost:8000/health>
- Eval run: `POST http://localhost:8000/v1/evals/run`
