import pytest
from guardrail_terraform import GuardrailTerraform, GuardrailPolicy

def test_upload_policies(tmp_path):
    policy_file = tmp_path / 'policy.json'
    policy_file.write_text('{"policy": "content"}')
    terraform = GuardrailTerraform([str(policy_file)])
    terraform.upload_policies()

def test_upload_policies_non_existent_file():
    terraform = GuardrailTerraform(['non_existent_file.json'])
    with pytest.raises(ValueError):
        terraform.upload_policies()

def test_re_evaluate_llm_calls(capsys):
    terraform = GuardrailTerraform([])
    terraform.re_evaluate_llm_calls()
    captured = capsys.readouterr()
    assert "Re-evaluating pending LLM calls" in captured.out

def test_main(tmp_path, capsys):
    policy_file = tmp_path / 'policy.json'
    policy_file.write_text('{"policy": "content"}')
    import sys
    sys.argv = ['guardrail_terraform.py', '--guardrail_policies', str(policy_file)]
    from guardrail_terraform import main
    main()
    captured = capsys.readouterr()
    assert "Uploading policy" in captured.out
    assert "Re-evaluating pending LLM calls" in captured.out
