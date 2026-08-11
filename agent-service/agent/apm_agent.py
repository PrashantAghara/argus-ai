from langchain.agents import create_agent

from agent.common import run_domain_agent
from agent.llm import get_llm
from agent.state import AgentState
from agent.tools import prometheus_query, prometheus_targets_up

apm_agent = create_agent(
    get_llm(),
    tools=[prometheus_targets_up, prometheus_query],
    system_prompt=(
        "You are an APM (application performance monitoring) specialist investigating "
        "a production incident. Use the available Prometheus tools to check target "
        "health and relevant metrics. Report findings in 2-4 concise sentences — "
        "focus on latency, error rates, and service availability."
    ),
)


def apm_agent_node(state: AgentState) -> dict:
    return run_domain_agent(apm_agent, "apm", state, "apm_findings")
