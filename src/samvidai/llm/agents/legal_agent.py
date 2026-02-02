from samvidai.llm.prompts.qa import build_qa_prompt
from samvidai.llm.prompts.risk_analysis import build_risk_prompt
from samvidai.llm.prompts.summarization import build_summary_prompt
from samvidai.llm.inference import run_llm

class LegalAgent:
    """
    Central reasoning agent for legal tasks.
    """

    def answer_question(self, question: str, context: list[str]) -> str:
        prompt = build_qa_prompt(question, context)
        return run_llm(prompt)

    def analyze_risk(self, clause_text: str) -> str:
        prompt = build_risk_prompt(clause_text)
        return run_llm(prompt)

    def summarize_document(self, context: list[str]) -> str:
        prompt = build_summary_prompt(context)
        return run_llm(prompt)