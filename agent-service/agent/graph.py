from langgraph.graph import END, START, StateGraph

from agent.aggregator import aggregator_node
from agent.apm_agent import apm_agent_node
from agent.db_agent import db_agent_node
from agent.infra_agent import infra_agent_node
from agent.state import AgentState
from agent.supervisor import supervisor


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("supervisor", supervisor)
    builder.add_node("apm_agent", apm_agent_node)
    builder.add_node("db_agent", db_agent_node)
    builder.add_node("infra_agent", infra_agent_node)
    builder.add_node("aggregator", aggregator_node)

    builder.add_edge(START, "supervisor")

    builder.add_edge("supervisor", "apm_agent")
    builder.add_edge("supervisor", "db_agent")
    builder.add_edge("supervisor", "infra_agent")

    builder.add_edge(["apm_agent", "db_agent", "infra_agent"], "aggregator")

    builder.add_edge("aggregator", END)

    return builder.compile()


graph = build_graph()
