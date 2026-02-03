import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

# Load config from .env
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

async def test_connection():
    print(f"Testing connection to {settings.MAIL_SERVER}...")
    print(f"User: {settings.MAIL_USERNAME}")
    
    if not settings.MAIL_PASSWORD or "app_password" in settings.MAIL_PASSWORD:
         print("Error: Password looks like a placeholder. Please check .env file.")
         return

    try:
        # FastMail doesn't have a direct 'test_login' method exposed easily without sending, 
        # but initializing it checks basic config. 
        # Ideally we would send a test email, but we don't know who to send to.
        # So we will try a simpler SMTP login check using python's built-in smtplib
        # to strictly verify credentials.
        import smtplib
        
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        print("SUCCESS! Login successful. Your App Password is working correctly.")
        server.quit()
        
    except smtplib.SMTPAuthenticationError:
        print("FAILED: Authentication Error. Username or App Password is incorrect.")
    except Exception as e:
        print(f"FAILED: Connection Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
