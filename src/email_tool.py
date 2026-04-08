# src/email_tool.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from crewai.tools import tool

@tool("Send Email Alert")
def send_email_alert(to_email: str, subject: str, body: str) -> str:
    """
    Sends an email alert to the specified email address.
    Useful for notifying business owners or suppliers about low stock items.
    """
    sender_email = os.environ.get("GMAIL_USER")
    sender_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender_email or not sender_password:
        # Mock email sending if credentials aren't natively set up
        print(f"\n[MOCK EMAIL] To: {to_email}\nSubject: {subject}\nBody:\n{body}\n")
        return f"Simulated email sent successfully to {to_email} (Credentials not configured in .env)."

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Use Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()

        return f"Email successfully sent to {to_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
