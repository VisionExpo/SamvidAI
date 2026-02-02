from samvidai.llm.prompts.qa import build_qa_prompt

def test_qa_prompt_contains_question():
    prompt = build_qa_prompt("What is termination?", ["Clause text"])
    assert "What is termination?" in prompt
