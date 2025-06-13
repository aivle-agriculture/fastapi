from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition, ToolNode

from .retriever_factory import setup_retriever
from .agent_nodes import agent_node, grade_documents, rewrite_node, generate_node, AgentState

retriever_tool = setup_retriever()

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node("rewrite", rewrite_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
workflow.add_conditional_edges("retrieve", grade_documents, {"generate": "generate", "rewrite": "rewrite"})
workflow.add_edge("rewrite", "agent")
workflow.add_edge("generate", END)
graph = workflow.compile()