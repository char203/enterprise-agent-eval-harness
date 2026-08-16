import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import exact
from inspect_ai.solver import system_message, generate


PROJECT_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = PROJECT_ROOT / "policies" / "support_policy.txt"

SUPPORT_POLICY = POLICY_PATH.read_text()

SYSTEM_PROMPT = f"""
You are an enterprise customer-support decision agent for Relay.

Your task is to classify each support ticket into exactly ONE action:

RESOLVE
REQUEST_INFO
ESCALATE

You must follow the support policy below.

--- SUPPORT POLICY ---

{SUPPORT_POLICY}

--- END POLICY ---

Use only the supplied policy and ticket information when making your decision.

Return ONLY one of these exact labels:
RESOLVE
REQUEST_INFO
ESCALATE

Do not provide explanations or additional text.
"""

def load_cases():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    path = PROJECT_ROOT / "datasets" / "support_cases.json"
    cases = json.loads(path.read_text())

    return [
        Sample(
            input=case["input"],
            target=case["target"],
        )
        for case in cases
    ]


@task
def support_eval():
    return Task(
        dataset=load_cases(),
        solver=[
            system_message(SYSTEM_PROMPT),
            generate(),
        ],
        scorer=exact(),
    )
