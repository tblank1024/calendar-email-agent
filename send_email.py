#!/usr/bin/env python3
"""Send a plain-text email via Gmail SMTP using an app password.

Usage:
    python3 send_email.py "<subject>" < body.txt

Requires the GMAIL_APP_PASSWORD environment variable to be set to a
Gmail App Password for the SENDER account (requires 2-Step Verification
to be enabled on that account).
"""
import os
import smtplib
import sys
from email.mime.text import MIMEText

SENDER = "tblank1024@gmail.com"
RECIPIENTS = ["tjblank@hotmail.com", "tjblank@msn.com"]


def main():
    if len(sys.argv) != 2:
        print('Usage: send_email.py "<subject>" < body.txt', file=sys.stderr)
        sys.exit(1)

    subject = sys.argv[1]
    body = sys.stdin.read()

    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, password)
        server.sendmail(SENDER, RECIPIENTS, msg.as_string())

    print(f"Sent to {', '.join(RECIPIENTS)}")


if __name__ == "__main__":
    main()
