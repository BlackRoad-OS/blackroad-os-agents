import importlib.util
import pathlib


def load_agent():
    path = pathlib.Path(__file__).resolve().parent.parent / 'agents' / 'org' / 'org-policy-steward-01.py'
    spec = importlib.util.spec_from_file_location('org_policy_steward', path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return module


def test_review_change_returns_summary():
    agent = load_agent()
    result = agent.review_change({'summary': 'Update retention'})
    assert result['change_summary'] == 'Update retention'
    assert result['requires_signoff'] is True


def test_flag_risks_includes_sensitive_data():
    agent = load_agent()
    risks = agent.flag_risks({'data_classification': 'sensitive', 'contractual': True})
    assert any(risk['type'] == 'data' for risk in risks)
    assert any(risk['type'] == 'contract' for risk in risks)
