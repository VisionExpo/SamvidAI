from samvidai.llm.prompts.qa import build_qa_prompt

def test_qa_prompt_contains_question():
    # Pass proper dict format for contexts
    contexts = [{"page_number": 1, "text": "Clause text"}]
    prompt = build_qa_prompt("What is termination?", contexts)
    assert "What is termination?" in prompt
    assert "Clause text" in prompt
