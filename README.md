# Enterprise Agent Evaluation Harness

Local LLM evaluation project using Inspect AI and Ollama.

## Current setup
- Harness: Inspect AI
- Local model: Qwen3 4B via Ollama
- Task: enterprise customer-support action selection
- Actions: RESOLVE, ESCALATE, REQUEST_INFO

## Baseline
First unconstrained 3-sample run:
- Exact-match mean: 0.000
- Input tokens: 59
- Output tokens: 5,827
- Total tokens: 5,886
- Total time: 2m56s

The baseline revealed that the model generated long reasoning rather than the exact action label.

## Run
Start Ollama:
`ollama serve`

Then:
`source .venv/bin/activate`
`inspect eval evals/support_eval.py --model ollama/qwen3:4b`

The ZIP intentionally excludes the local virtual environment, Ollama model weights, and raw Inspect logs.
Recreate dependencies with `pip install -r requirements.txt` and the model with `ollama pull qwen3:4b`.
