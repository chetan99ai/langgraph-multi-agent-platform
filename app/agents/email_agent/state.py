# Pydantic state models for Email

from pydantic import BaseModel, Field

class EmailState(BaseModel):
    """The global shared state for our LangGraph email execution loop."""
    question: str = ""
    mail_reason: str = ""
    recipient_name: str = ""
    recipient_email: str = ""
    subject: str = ""
    body: str = ""
    feedback: str = ""
    feedback_count: int = 0  # Max Count 3
    response: str = ""

class UserDetails(BaseModel):
    """The structured data structure the LLM will extract from the user's initial query."""
    mail_reason: str = Field(description="Reason for the email, like why the user wants to send this email.")
    recipient_name: str = Field(description="Recipient / receiver name, if available.")
    recipient_email: str = Field(description="Recipient / receiver email address.")

class DraftEmail(BaseModel):
    """The structured data structure the LLM will use to draft the subject and body."""
    subject: str = Field(description="Email subject within 40 Words")
    body: str = Field(description="Email Body including proper details, reason, greetings, and signature")
