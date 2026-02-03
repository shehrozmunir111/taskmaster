"""
Notification Service - Handles real email notifications.
"""

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
from pathlib import Path

# Email setup configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_welcome_email(email_to: str, name: str):
    """
    Sends a real welcome email using SMTP.
    """
    if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
        print("Email credentials not set in .env. Skipping email.")
        return

    html_content = f"""
    <html>
        <body>
            <h1>Welcome to TaskMaster, {name}!</h1>
            <p>We are excited to have you on board.</p>
            <p>Get started by creating your first Project Board.</p>
            <br>
            <p>Best regards,</p>
            <p>The TaskMaster Team</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to TaskMaster!",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )

    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        print(f"Email successfully sent to {email_to}")
    except Exception as e:
        print(f"Failed to send email: {e}")
