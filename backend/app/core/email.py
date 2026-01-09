import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_email(email_to: str, subject: str, html_content: str) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    message["To"] = email_to

    part = MIMEText(html_content, "html")
    message.attach(part)

    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    
    try:
        with smtplib.SMTP(**smtp_options) as server:
            if settings.SMTP_TLS:
                server.starttls()
            
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                
            server.sendmail(settings.EMAILS_FROM_EMAIL, email_to, message.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}") 
        # In production, use proper logging
