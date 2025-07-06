import os, smtplib, ssl
from email.message import EmailMessage
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Python ≥3.9

central = ZoneInfo("America/Chicago")
now     = datetime.now(timezone.utc).astimezone(central)
hour    = now.hour  # 24-hour clock, CDT

# map run time → window text
if   hour == 13:               # 1 PM reminder
    window = "between 11:00 AM and 1:00 PM"
elif hour == 19:               # 7 PM reminder
    window = "between 4:00 PM and 6:00 PM"
elif hour == 23:               # 11 PM reminder
    window = "between 9:00 PM and 11:00 PM"
else:
    window = "today"

msg = EmailMessage()
msg["From"]    = os.environ["SMTP_USER"]
msg["To"]      = os.environ["RECIPIENT"]
msg["Subject"] = "It’s time to attune your medication station!"

msg.set_content(
    f"""Polite reminder to take your medication {window}.

They are safe to take and will help you.

Please take them with a glass of water and try to remember water as you go through your day.

If you’re not able to take your medication when you receive this email, please set an alarm to go off in 45 minutes, then snooze that alarm each time until the medication is taken. Turn it off only once they have been taken.

It's okay to be scared of them, but we promise you are okay and safe to take them. Nobody is going to harm you.

We care about you and just want you to be safe, happy, and healthy.

Stay safe – don’t forget the medication!"""
)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
    smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
    smtp.send_message(msg)
