import secrets
import string
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

mail_domain = os.getenv('MAIL_DOMAIN')
smtp_port = os.getenv('SMTP_PORT')
mail_user = os.getenv('MAIL_USER')
mail_password = os.getenv('MAIL_PASSWORD')

def generate_temp_password(Length=10):
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(secrets.choice(chars) for _ in range(Length))


def send_temporary_password(email: str, password: str, name: str):
    msg = EmailMessage()
    msg['Subject'] = "dawaChat: Your Temporary Login Password"
    msg['From'] = "info@advernet.africa"
    msg['To'] = email
    # Plain text fallback (for email clients that don't support HTML)
    msg.set_content(f"""
Hi {name},

Here is your temporary password: {password}

Please login and change it immediately.
    """)

    # Add HTML version
    html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
      <h2 style="color: #333;">👋 Hello {name},</h2>
      <p style="font-size: 16px; color: #555;">
        You have been granted access to the dawaChat system. Below is your temporary password:
      </p>
      <p style="font-size: 18px; color: #000; font-weight: bold; background: #e8f0fe; padding: 10px 20px; border-radius: 5px; display: inline-block;">
        {password}
      </p>
      <p style="font-size: 16px; color: #555; margin-top: 20px;">
        Please login as soon as possible and change this password for your security.
      </p>
      <p style="font-size: 14px; color: #888; margin-top: 30px;">
        If you did not request this, please contact the system administrator.
      </p>
    </div>

    <!-- Footer -->
    <div style="max-width: 600px; margin: 30px auto 0 auto; text-align: center; color: #888; font-size: 13px;">
      <p style="margin-bottom: 5px;"><strong>dawaChat</strong></p>
      <p style="margin: 0;">A powerful tool to help doctors manage dosage information and prescriptions with ease.</p>
      <p style="margin: 5px 0;">📧 info@dawachat.ai</p>
      <p style="margin: 0;">📍 Nairobi, Kenya</p>
    </div>
  </body>
</html>
"""

    msg.add_alternative(html_content, subtype="html")

    
    with smtplib.SMTP(mail_domain, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(mail_user, mail_password)
        smtp.send_message(msg)