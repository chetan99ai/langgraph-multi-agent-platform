import os
import logging
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

# Import state schemas and utilities
from app.agents.email_agent.state import EmailState, UserDetails, DraftEmail
from app.agents.email_agent.utils.send_email import send_email

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🎛️ DYNAMIC ENGINE INITIALIZATION
def get_llm_engine():
    """
    Evaluates the environment target flag at execution runtime.
    Dynamically loads the requested LLM connector package on-demand.
    """
    env_target = os.getenv("ENV_TARGET", "local").lower()
    
    if env_target == "aws":
        logger.info("🚀 Routing workflow inference execution to Amazon Bedrock (Claude 3.5 Sonnet)")
        from langchain_aws import ChatBedrockConverse
        return ChatBedrockConverse(
            # model_id="anthropic.claude-sonnet-4-6", # Need to open a aws support case to get access
            model_id="amazon.nova-pro-v1:0", # We will use this one as of now
            temperature=0.0
        )
    else:
        logger.info("💻 Routing workflow inference execution to Groq (Llama 3.3)")
        from langchain_groq import ChatGroq
        # Change only this model string to talk to Groq's live server!
        return ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.0
        )


# Instantiate the LLM dynamically using the runner block
llm = get_llm_engine()


# nodes, router, and graph compilation code:

def retriever_node(state: EmailState) -> EmailState:
    """Extracts explicit recipient fields from raw user prompts."""
    prompt = f"Retrieve the user details from this query: {state.question}."
    llm_for_user_details = llm.with_structured_output(UserDetails)
    user_details: UserDetails = llm_for_user_details.invoke(prompt)

    state.recipient_name = user_details.recipient_name
    state.recipient_email = user_details.recipient_email
    state.mail_reason = user_details.mail_reason
    return state

def draft_node(state: EmailState) -> EmailState:
    """Generates or updates email compositions based on conversational history."""
    prompt = f"""
        Write an email with these details:
        To: {state.recipient_name}
        Request: {state.mail_reason}
        Max body size: 200 words. No extra conversational text outside the email format.
    """
    
    # If the user previously rejected the draft, revise it based on their comments
    if state.feedback:
        prompt = f"""
            Revise this email based on the feedback below.
            Current Email:
            Subject: {state.subject}
            Body: {state.body}
            Feedback: {state.feedback}
            Max body size: 200 words. No extra conversational text outside the email format.
        """

    draft_email_llm = llm.with_structured_output(DraftEmail)
    draft_email: DraftEmail = draft_email_llm.invoke(prompt)
    state.subject = draft_email.subject
    state.body = draft_email.body
    return state

def review_node(state: EmailState) -> EmailState:
    """Pauses graph thread execution to await manual client side human approval."""
    # State-Machine Interrupt: Returns control back to the Bedrock AgentCore wrapper
    response = interrupt({
        "status": "AWAITING_APPROVAL",
        "subject": state.subject,
        "body": state.body,
        "message": "Please approve this draft ('yes') or provide feedback text to rewrite it."
    })

    if response.lower() == "yes":
        state.feedback = ""
    else:
        state.feedback = response
        state.feedback_count += 1
    return state

def review_router(state: EmailState) -> Literal["draft", "send", "cancel"]:
    """Determines branching directions following human interaction passes."""
    if not state.feedback or state.feedback.strip() == "":
        return "send"
    if state.feedback_count > 2:
        return "cancel"
    return "draft"

def cancel_node(state: EmailState) -> EmailState:
    """Gracefully terminates workflows when iteration thresholds are breached."""
    state.response = "Email Not Sent. Feedback loop limit exceeded."
    return state

def send_node(state: EmailState) -> EmailState:
    """Triggers external integration code blocks to dispatch the final email."""
    response = send_email(state.recipient_email, state.subject, state.body)
    state.response = response
    return state

# Build the LangGraph structural flow topology
workflow = StateGraph(EmailState)
workflow.add_node("retriever", retriever_node)
workflow.add_node("draft_node", draft_node)
workflow.add_node("review_node", review_node)
workflow.add_node("send_node", send_node)
workflow.add_node("cancel_node", cancel_node)

workflow.add_edge(START, "retriever")
workflow.add_edge("retriever", "draft_node")
workflow.add_edge("draft_node", "review_node")
workflow.add_conditional_edges("review_node", review_router, {
    "draft": "draft_node",
    "send": "send_node",
    "cancel": "cancel_node"
})
workflow.add_edge("send_node", END)
workflow.add_edge("cancel_node", END)

# Compile the graph using a checkpoint saver memory block to handle interrupts properly
# the local langgraph dev engine has strict rules against compiling graphs with an explicit checkpointer like InMemorySaver() attached.
# email_graph = workflow.compile(checkpointer=InMemorySaver())

# Strip out the explicit checkpointer argument. 
# LangGraph Studio UI and Bedrock AgentCore will handle thread memory automatically!
email_graph = workflow.compile()

