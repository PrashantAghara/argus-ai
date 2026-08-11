from langchain.agents import create_agent

from agent.common import run_domain_agent
from agent.llm import get_llm
from agent.state import AgentState
from agent.tools import db_top_queries

db_agent = create_agent(
    get_llm(),
    tools=[db_top_queries],
    system_prompt=(
        "You are a database performance specialist investigating a production incident. "
        "Use pg_stat_statements data to identify the most likely slow-query contributors. "
        "Report findings in 2-4 concise sentences."
    ),
)


def db_agent_node(state: AgentState) -> dict:
    return run_domain_agent(db_agent, "db", state, "db_findings")
