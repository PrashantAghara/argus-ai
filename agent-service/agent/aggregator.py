from agent.llm import get_llm
from agent.state import AgentState


def aggregator_node(state: AgentState) -> dict:
    prompt = (
        "Synthesize a concise incident report from these specialist findings.\n\n"
        f"Incident: {state['incident_description']}\n\n"
        f"APM findings: {state.get('apm_findings', 'N/A')}\n\n"
        f"DB findings: {state.get('db_findings', 'N/A')}\n\n"
        f"Infra findings: {state.get('infra_findings', 'N/A')}\n\n"
        "Write a short report covering: likely root cause, affected systems, "
        "and recommended next steps."
    )
    response = get_llm().invoke(prompt)
    return {"final_report": response.content}
