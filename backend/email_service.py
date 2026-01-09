"""
Email service for sending newsletters and transactional emails.
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List, Dict, Optional
from datetime import datetime
import secrets

# Email configuration from environment variables
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
FROM_NAME = os.getenv("FROM_NAME", "Newsletter Cultural Chile")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Initialize Jinja2 environment
template_env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send an email using SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")
        return False


def send_confirmation_email(to_email: str, confirmation_token: str) -> bool:
    """
    Send subscription confirmation email.
    
    Args:
        to_email: Subscriber email
        confirmation_token: Confirmation token
        
    Returns:
        bool: True if sent successfully
    """
    template = template_env.get_template('confirmation.html')
    confirmation_url = f"{BASE_URL}/confirm/{confirmation_token}"
    
    html_content = template.render(
        confirmation_url=confirmation_url,
        email=to_email
    )
    
    return send_email(
        to_email=to_email,
        subject="Confirma tu suscripción a Newsletter Cultural Chile",
        html_content=html_content
    )


def send_newsletter(
    to_email: str,
    subject: str,
    events: List[Dict],
    newsletter_id: int,
    subscriber_id: int
) -> bool:
    """
    Send newsletter email.
    
    Args:
        to_email: Subscriber email
        subject: Newsletter subject
        events: List of event dictionaries
        newsletter_id: Newsletter ID for tracking
        subscriber_id: Subscriber ID for tracking
        
    Returns:
        bool: True if sent successfully
    """
    template = template_env.get_template('newsletter.html')
    
    # Generate tracking token
    tracking_token = secrets.token_urlsafe(16)
    tracking_pixel_url = f"{BASE_URL}/track/open/{newsletter_id}/{subscriber_id}/{tracking_token}.gif"
    
    html_content = template.render(
        events=events,
        tracking_pixel_url=tracking_pixel_url,
        unsubscribe_url=f"{BASE_URL}/unsubscribe?email={to_email}",
        current_year=datetime.now().year
    )
    
    return send_email(
        to_email=to_email,
        subject=subject,
        html_content=html_content
    )


def send_batch_newsletters(
    subscribers: List[Dict],
    subject: str,
    events: List[Dict],
    newsletter_id: int,
    delay_seconds: float = 0.5
) -> Dict[str, int]:
    """
    Send newsletter to multiple subscribers with rate limiting.
    
    Args:
        subscribers: List of subscriber dictionaries with 'id' and 'email'
        subject: Newsletter subject
        events: List of events to include
        newsletter_id: Newsletter ID
        delay_seconds: Delay between emails (rate limiting)
        
    Returns:
        dict: Statistics with 'sent' and 'failed' counts
    """
    import time
    
    stats = {"sent": 0, "failed": 0}
    
    for subscriber in subscribers:
        success = send_newsletter(
            to_email=subscriber['email'],
            subject=subject,
            events=events,
            newsletter_id=newsletter_id,
            subscriber_id=subscriber['id']
        )
        
        if success:
            stats["sent"] += 1
        else:
            stats["failed"] += 1
        
        # Rate limiting
        time.sleep(delay_seconds)
    
    return stats
