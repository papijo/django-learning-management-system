import smtplib
import os

try:
    server = smtplib.SMTP(
        os.environ.get("SMTP_EMAIL_EMAIL_URL"), os.environ.get("SMTP_EMAIL_EMAIL_PORT")
    )
    server.starttls()
    server.login(
        os.environ.get("SMTP_EMAIL_SENDER"), os.environ.get("SMTP_EMAIL_PASSWORD")
    )
    server.quit()
except Exception as e:
    print(f"SMTP Connection Error: {e}")
