import smtplib
from email.message import EmailMessage
from django.conf import settings

def send_verification_email(email, verification_code):
    """Sends an email with a verification code using smtplib."""
    
    # Email message details
    subject = "Verify Your Email"
    body = f"Your verification code: {verification_code}"
    
    # Create email
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = email

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
        return True  # Email sent successfully
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
