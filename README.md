# Daily Calendar Email Agent

Sends Tom a daily summary of his upcoming calendar events (today,
tomorrow, day after) to tjblank@hotmail.com and tjblank@msn.com, every
day at ~3:00 AM America/Los_Angeles, fully cloud-hosted via Claude Code
on the web (no local machine required).

## How it works

- **Reading the calendar**: done by the agent itself via the connected
  Google Calendar MCP integration (already authorized to your Claude
  account — no extra setup).
- **Sending the email**: the Gmail MCP connector can only create drafts,
  not send. So `send_email.py` sends via Gmail SMTP using an **App
  Password**, stored as an environment secret.

## One-time setup

1. **Push this repo to GitHub** (or your preferred git host) and connect
   it as the repo for a Claude Code on the web environment.

2. **Generate a Gmail App Password** for tblank1024@gmail.com:
   - Enable 2-Step Verification on the account if not already on:
     https://myaccount.google.com/security
   - Create an App Password: https://myaccount.google.com/apppasswords
   - Choose "Mail" / "Other", name it e.g. "calendar-agent".
   - Copy the 16-character password.

3. **Add the secret to the environment**:
   - In the Claude Code on the web environment settings, add an
     environment variable/secret named `GMAIL_APP_PASSWORD` with the
     value from step 2.

4. **Create a scheduled trigger**:
   - In Claude Code on the web, create a trigger that runs daily at
     3:00 AM America/Los_Angeles (convert to UTC for the cron schedule —
     account for PST/PDT, currently UTC-7 in summer).
   - Use the prompt in `daily_calendar_agent_prompt.md` as the trigger's
     prompt (update the `/path/to/calendar-email-agent/` path to wherever
     this repo is checked out in the environment).

## Files

- `send_email.py` — sends a plain-text email via Gmail SMTP using
  `GMAIL_APP_PASSWORD`.
- `daily_calendar_agent_prompt.md` — the full instructions for the
  scheduled agent run (calendar fetch, formatting, dedup/tagging rules,
  and the send step).

## Testing send_email.py manually

```
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
echo "Test body" | python3 send_email.py "Test subject"
```
