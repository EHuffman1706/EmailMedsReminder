import os, smtplib, ssl, json
from email.message import EmailMessage
from datetime import datetime, date, timezone, timedelta
from zoneinfo import ZoneInfo   # Python ≥3.9

# --- CONFIG ------------------------------------------------------------------
PATCH_START     = date(2025, 7, 7)   # first patch change
PATCH_INTERVAL  = 3                  # every 3 days
CENTRAL         = ZoneInfo("America/Chicago")
WINDOWS = {                          # Central Time → window text
    9:  "between 7:00 AM and 9:00 AM",
    13: "between 11:00 AM and 1:00 PM",
    16: "between 2:00 PM and 4:00 PM",
    21: "between 8:00 PM and 9:00 PM",
}
# -----------------------------------------------------------------------------

now_cdt = datetime.now(timezone.utc).astimezone(CENTRAL)
hour    = now_cdt.hour
today   = now_cdt.date()

window_text = WINDOWS.get(hour, "UNKNOWN WINDOW")

# --- extra blocks ------------------------------------------------------------
bp_block = ""
if hour == 13:
    bp_block = (
        "\nThis reminder is specifically for your blood-pressure medication. "
        "Taking it consistently will help keep your blood pressure within a safe range.\n"
    )

patch_block = ""
if hour == 9:
    days_since_start = (today - PATCH_START).days
    if days_since_start >= 0 and days_since_start % PATCH_INTERVAL == 0:
        patch_block = (
            "\n⏰ **Hormone patch reminder:**\n"
            "Please change your hormone patch today. Make sure the new patch is applied "
            "to a clean, dry area of skin and note the date for your next change.\n"
        )

# --- build and send ----------------------------------------------------------
msg = EmailMessage()
msg["From"]    = os.environ["SMTP_USER"]
msg["To"]      = os.environ["RECIPIENT"]
msg["Subject"] = "It’s time to attune your medication station!"

msg.set_content(
    f"""Polite reminder to take your medication {window_text}.

They are safe to take and will help you.{bp_block}

Please take them with a glass of water and try to remember water as you go through your day.

If you’re not able to take your medication when you receive this email, please set an alarm to go off in 45 minutes, then snooze that alarm each time until the medication is taken. Turn it off only once they have been taken.

It's okay to be scared of them, but we promise you are okay and safe to take them. Nobody is going to harm you.
{patch_block}
We care about you and just want you to be safe, happy, and healthy.

Stay safe – don’t forget the medication!"""
)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
# --- who gets the email ------------------------------------------------------
recipients = [addr.strip() for addr in os.environ["RECIPIENTS"].split(",")]

msg["To"] = ", ".join(recipients)        # visible list in header

# --- send it -----------------------------------------------------------------
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
    smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
    smtp.send_message(msg, to_addrs=recipients)
