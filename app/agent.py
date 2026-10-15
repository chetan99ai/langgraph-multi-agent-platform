#production-ready platform routing architecture
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from langgraph.types import Command

# Import the compiled email graph you completed in the previous step
from app.agents.email_agent.graph import email_graph

app = BedrockAgentCoreApp()

@app.entrypoint
def orchestrate_platform_agents(payload, context):
    """
    The master entrypoint for the Amazon Bedrock AgentCore serverless runtime.
    Routes execution to the correct agent graph based on user intent or metadata.
    """
    input_text = payload.get("input", {}).get("text", "")
    
    # sessionId acts as the persistent thread identifier for conversational tracking
    thread_id = payload.get("sessionId", "platform_default_thread")
    config = {"configurable": {"thread_id": thread_id}}
    
    # 🧠 MULTI-AGENT ROUTING ENGINE
    # Step A: Check if there's an ongoing thread active in the Email Graph
    email_state = email_graph.get_state(config)
    
    if email_state.next:
        # The Email Graph is warm and currently waiting at a human-in-the-loop interrupt
        result = email_graph.invoke(Command(resume=input_text), config=config)
        return format_email_agent_response(email_graph.get_state(config), result)
        
    # Step B: If no active thread exists, route based on text intent rules
    # (As you build more agents, you can expand this block to handle custom classifiers)
    lowered_input = input_text.lower()
    if "email" in lowered_input or "mail" in lowered_input or "send to" in lowered_input:
        # Route fresh session directly into the Email Agent pipeline
        result = email_graph.invoke({"question": input_text}, config=config)
        return format_email_agent_response(email_graph.get_state(config), result)
        
    # Placeholder block for handling your future agents
    # elif "research" in lowered_input:
    #     return research_graph.invoke(...)

    # Default fallback response if no agent rules match the user intent
    return {
        "output": {
            "text": "I am your central AI Broker. Please ask me to manage an email task to get started."
        }
    }


def format_email_agent_response(current_graph_state, fallback_result):
    """Parses LangGraph execution outcomes into a structured Bedrock JSON response contract."""
    # Check if the graph execution hit the review_node interrupt barrier
    if current_graph_state.next:
        interrupt_info = current_graph_state.tasks.interrupts[0].value
        return {
            "output": {
                "text": f"STATUS: AWAITING_APPROVAL\n"
                        f"Subject: {interrupt_info.get('subject')}\n"
                        f"Body: {interrupt_info.get('body')}\n\n"
                        f"{interrupt_info.get('message')}"
            }
        }
    
    # The graph reached the END node cleanly
    return {
        "output": {
            "text": fallback_result.get("response", "Workflow successfully finalized.")
        }
    }


if __name__ == "__main__":
    app.run()
