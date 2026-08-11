from typing import TypedDict


class AgentState(TypedDict):
    incident_description: str
    relevant_agents: list[str]
    apm_findings: str
    db_findings: str
    infra_findings: str
    final_report: str
