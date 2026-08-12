import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

def send_email_notification(to_email: str, subject: str, body: str) -> tuple[bool, str]:
    """
    Sends email notification via SMTP.
    If SMTP credentials are not configured, performs a silent mock send.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.info(f"[Mock Email Service] To: {to_email} | Subject: {subject} | Body: {body[:60]}...")
        return True, "Mock email logged (SMTP credentials not set in .env)."

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        return True, "Email sent successfully."
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False, f"Email delivery error: {str(e)}"
