FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY evals/ ./evals/
COPY datasets/ ./datasets/
COPY policies/ ./policies/
COPY agents/ ./agents/

RUN mkdir -p logs

CMD ["inspect", "eval", "evals/support_eval.py", "--model", "ollama/qwen3:4b"]
