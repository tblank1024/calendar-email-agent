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
  not send, and the cloud sandbox blocks raw outbound SMTP (ports 25/465/587).
  So `send_email.py` sends via the **Gmail API over HTTPS** (which is
  allowed, since `googleapis.com` is already reachable for Calendar),
  authenticated with an OAuth2 refresh token stored as environment secrets.

## One-time setup

1. **Push this repo to GitHub** (or your preferred git host) and connect
   it as the repo for a Claude Code on the web environment.

2. **Generate OAuth2 credentials** with the `gmail.send` scope:
   - Run `get_refresh_token.py` (in `calendar-summary/`, or recreate it
     with the `gmail.send` and `calendar.readonly` scopes) locally. It
     opens a browser to sign in as tblank1024@gmail.com and prints a
     `client_id`, `client_secret`, and `refresh_token`.
   - Note: if the Google Cloud OAuth consent screen is in "Testing" mode,
     refresh tokens for sensitive scopes like `gmail.send` expire after 7
     days. Set the consent screen to "In production" for a long-lived
     token.

3. **Add the secrets to the environment**:
   - In the Claude Code on the web environment settings, add environment
     variables/secrets:
     - `GMAIL_CLIENT_ID`
     - `GMAIL_CLIENT_SECRET`
     - `GMAIL_REFRESH_TOKEN`

4. **Create a scheduled trigger**:
   - In Claude Code on the web, create a trigger that runs daily at
     3:00 AM America/Los_Angeles (convert to UTC for the cron schedule —
     account for PST/PDT, currently UTC-7 in summer).
   - Use the prompt in `daily_calendar_agent_prompt.md` as the trigger's
     prompt (update the `/path/to/calendar-email-agent/` path to wherever
     this repo is checked out in the environment).

## Files

- `send_email.py` — sends a plain-text email via the Gmail API (HTTPS)
  using `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, and `GMAIL_REFRESH_TOKEN`.
- `daily_calendar_agent_prompt.md` — the full instructions for the
  scheduled agent run (calendar fetch, formatting, dedup/tagging rules,
  and the send step).

## Testing send_email.py manually

```
export GMAIL_CLIENT_ID="..."
export GMAIL_CLIENT_SECRET="..."
export GMAIL_REFRESH_TOKEN="..."
echo "Test body" | python3 send_email.py "Test subject"
```
