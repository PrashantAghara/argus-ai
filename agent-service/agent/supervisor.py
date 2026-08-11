from agent.llm import get_llm
from agent.state import AgentState


def supervisor(state: AgentState) -> dict:
    incident = state["incident_description"]

    prompt = (
        f'An incident was reported: "{incident}"\n\n'
        "Decide which specialist teams should investigate. Respond with ONLY a "
        "comma-separated subset of: apm, db, infra. Include a team only if it's "
        "plausibly relevant to this incident. If unsure, include all three."
    )
    response = get_llm().invoke(prompt)
    text = response.content.lower()
    relevant = [name for name in ("apm", "db", "infra") if name in text]

    if not relevant:
        relevant = ["apm", "db", "infra"]
    return {"relevant_agents": relevant}
