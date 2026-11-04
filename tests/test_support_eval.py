import json

from evals import support_eval


def test_policy_defines_every_label():
    for label in support_eval.LABELS:
        assert label in support_eval.SUPPORT_POLICY


def test_system_prompt_embeds_policy_and_labels():
    assert support_eval.SUPPORT_POLICY.strip() in support_eval.SYSTEM_PROMPT
    for label in support_eval.LABELS:
        assert label in support_eval.SYSTEM_PROMPT


def test_load_cases_matches_dataset():
    samples = support_eval.load_cases()
    raw = json.loads(support_eval.DATASET_PATH.read_text())
    assert [(s.input, s.target) for s in samples] == [(c["input"], c["target"]) for c in raw]


def test_load_cases_accepts_custom_path(tmp_path):
    path = tmp_path / "cases.json"
    path.write_text(json.dumps([{"input": "Refund $900 please", "target": "ESCALATE"}]))
    [sample] = support_eval.load_cases(path)
    assert sample.input == "Refund $900 please"
    assert sample.target == "ESCALATE"


def test_task_builds_with_full_dataset():
    task = support_eval.support_eval()
    assert len(task.dataset) == len(support_eval.load_cases())
