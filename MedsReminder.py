import os, smtplib, ssl
from email.message import EmailMessage
from datetime import datetime, timezone

# ---------- build the email ----------
msg = EmailMessage()
msg["From"] = os.environ["SMTP_USER"]
msg["To"]   = os.environ["RECIPIENT"]
msg["Subject"] = "It’s time to attune your medication station!"

msg.set_content(
    """Polite reminder to take your medication before 11 AM.

They are safe to take and will help you.

Please take them with a glass of water and try to remember water as you go through your day.

If you are not able to take your medication when you receive this email, please set an alarm to go off in 45 minutes, then snooze that alarm each time until the medication is taken. Turn it off only once they have been taken.

We care about you and just want you to be safe, happy, and healthy.

Stay safe – don’t forget the medication!"""
)

# ---------- send it ----------
ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
    smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
    smtp.send_message(msg)
