from langchain.agents import create_agent

from agent.common import run_domain_agent
from agent.llm import get_llm
from agent.state import AgentState
from agent.tools import prometheus_query

infra_agent = create_agent(
    get_llm(),
    tools=[prometheus_query],
    system_prompt=(
        "You are an infrastructure specialist investigating a production incident. "
        "Use PromQL queries against node-exporter and cAdvisor metrics (e.g. "
        "container_cpu_usage_seconds_total, node_memory_MemAvailable_bytes) to check "
        "host and container resource health. Report findings in 2-4 concise sentences."
    ),
)


def infra_agent_node(state: AgentState) -> dict:
    return run_domain_agent(infra_agent, "infra", state, "infra_findings")
