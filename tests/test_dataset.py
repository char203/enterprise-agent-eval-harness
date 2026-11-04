import json
from collections import Counter

from evals.support_eval import DATASET_PATH, LABELS


def load_raw_cases():
    return json.loads(DATASET_PATH.read_text())


def test_every_case_has_input_and_valid_target():
    for case in load_raw_cases():
        assert set(case) == {"input", "target"}
        assert case["input"].strip()
        assert case["target"] in LABELS


def test_inputs_are_unique():
    inputs = [case["input"].strip().lower() for case in load_raw_cases()]
    duplicates = [text for text, n in Counter(inputs).items() if n > 1]
    assert not duplicates


def test_every_label_is_represented():
    targets = Counter(case["target"] for case in load_raw_cases())
    assert set(targets) == set(LABELS)
