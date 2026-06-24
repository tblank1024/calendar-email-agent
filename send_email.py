#!/usr/bin/env python3
"""Send an email via the Gmail API over HTTPS using OAuth2.

Usage:
    python3 send_email.py "<subject>" < body.txt

Requires these environment variables (OAuth2 client credentials with the
gmail.send scope, generated via get_refresh_token.py):
    GMAIL_CLIENT_ID
    GMAIL_CLIENT_SECRET
    GMAIL_REFRESH_TOKEN

Uses HTTPS to googleapis.com instead of raw SMTP, so it works in sandboxes
that block outbound SMTP (ports 25/465/587) but allow HTTPS egress to
Google APIs.

Sends as multipart/alternative (plain text + HTML <pre> block). Outlook /
Outlook.com convert plain-text emails to HTML for display and collapse
single line breaks within a "paragraph" (e.g. a run of lines not separated
by a line of dashes or a blank line gets joined onto one line). The <pre>
HTML part preserves line breaks exactly as written, regardless of that
conversion.
"""
import base64
import html
import json
import os
import sys
import urllib.parse
import urllib.request
from email import policy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER = "tblank1024@gmail.com"
RECIPIENTS = ["tjblank@hotmail.com", "tjblank@msn.com"]

TOKEN_URL = "https://oauth2.googleapis.com/token"
SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


def get_access_token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["GMAIL_CLIENT_ID"],
        "client_secret": os.environ["GMAIL_CLIENT_SECRET"],
        "refresh_token": os.environ["GMAIL_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["access_token"]


def main():
    if len(sys.argv) != 2:
        print('Usage: send_email.py "<subject>" < body.txt', file=sys.stderr)
        sys.exit(1)

    subject = sys.argv[1]
    body = sys.stdin.read()

    msg = MIMEMultipart("alternative", policy=policy.SMTP)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Importance"] = "high"
    msg["X-Priority"] = "1"
    msg["X-MSMail-Priority"] = "High"
    html_body = (
        '<pre style="font-family: Calibri, \'Segoe UI\', Helvetica, Arial, '
        'sans-serif; font-size: 15px; white-space: pre-wrap;">'
        f"{html.escape(body)}</pre>"
    )
    msg.attach(MIMEText(body, "plain", policy=policy.SMTP))
    msg.attach(MIMEText(html_body, "html", policy=policy.SMTP))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    access_token = get_access_token()
    req = urllib.request.Request(
        SEND_URL,
        data=json.dumps({"raw": raw}).encode(),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        json.load(resp)

    print(f"Sent to {', '.join(RECIPIENTS)}")


if __name__ == "__main__":
    main()
