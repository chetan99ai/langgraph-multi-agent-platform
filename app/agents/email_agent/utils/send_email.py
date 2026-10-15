import smtplib
from email.message import EmailMessage
import os
import logging

# Configure basic logging output for container observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(recepient_email: str, Subject: str, body: str) -> str:
    """Dispatches emails using secure SMTP configurations driven entirely by environment variables."""
    logger.info(f"Initiating dynamic SMTP outbound request to: {recepient_email}")
    
    # 1. Setup email data dynamically from environment variables injected by the runtime environment
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT_RAW = os.getenv("SMTP_PORT")
    RECEIVER_EMAIL = recepient_email

    # Fail early with clear logs if any configuration variables are missing
    if not SENDER_EMAIL:
        logger.error("Environment variable 'SENDER_EMAIL' is missing.")
        return "Failed to send email: SENDER_EMAIL environment variable is not configured."

    if not APP_PASSWORD:
        logger.error("Environment variable 'GMAIL_APP_PASSWORD' is missing.")
        return "Failed to send email: GMAIL_APP_PASSWORD environment variable is not configured."

    if not SMTP_SERVER:
        logger.error("Environment variable 'SMTP_SERVER' is missing.")
        return "Failed to send email: SMTP_SERVER environment variable is not configured."

    if not SMTP_PORT_RAW:
        logger.error("Environment variable 'SMTP_PORT' is missing.")
        return "Failed to send email: SMTP_PORT environment variable is not configured."

    try:
        SMTP_PORT = int(SMTP_PORT_RAW)
    except ValueError:
        logger.error(f"Invalid SMTP_PORT value: {SMTP_PORT_RAW}. Must be an integer.")
        return "Failed to send email: SMTP_PORT must be a valid integer configuration."

    # 2. Construct the message using EmailMessage
    msg = EmailMessage()
    msg["Subject"] = Subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(body)

    # 3. Establish a secure connection and send via dynamic server parameters
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to secure TLS encryption
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)  # Automatically handles headers and recipients
        
        logger.info("Outbound SMTP dynamic dispatch completed successfully.")
        return "Email sent successfully!"
    except Exception as e:
        logger.error(f"SMTP Dynamic Transmission error: {e}")
        return f"Failed to send email: {e}"
