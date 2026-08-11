from agent.state import AgentState


def run_domain_agent(agent, domain: str, state: AgentState, findings_key: str) -> dict:
    if domain not in state.get("relevant_agents", []):
        return {
            findings_key: f"Skipped - supervisor judged '{domain}' irrelevant to this incident."
        }
    result = agent.invoke(
        {"messages": [{"role": "user", "content": state["incident_description"]}]}
    )
    final_message = result["messages"][-1]
    return {findings_key: final_message.content}
