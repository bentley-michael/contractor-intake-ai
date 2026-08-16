# Contractor Intake AI

A production-style lead intake automation for home-service contractors. The system receives structured call data from a Vapi voice agent, normalizes the payload in n8n, filters junk/spam events, writes qualified leads to Google Sheets, and sends operational alerts to Discord.

## Why this project exists

Contractors miss leads when calls arrive after hours, during jobs, or when office staff are overloaded. This workflow turns an AI-assisted phone conversation into a structured, routable lead record that can be acted on immediately.

## Architecture

```text
Caller
  ↓
Vapi voice agent
  ↓ POST /vapi/intake
n8n webhook
  ↓
Payload normalization
  ↓
Client/environment configuration
  ↓
Spam / junk decision
  ├─ Junk → Spam record
  └─ Qualified lead
       ├─ Google Sheets CRM row
       └─ Discord operational alert
```

## Core integration flow

1. **Webhook ingestion** — n8n exposes `POST /vapi/intake` for incoming call payloads.
2. **Normalization** — JavaScript nodes flatten and sanitize caller, contact, location, service, urgency, recording, transcript, and spam fields.
3. **Client configuration** — client name, sheet ID, Discord webhook URL, and junk-score threshold are loaded from environment variables.
4. **Junk filtering** — suspicious calls are routed separately using an explicit boolean/score threshold.
5. **Lead preparation** — qualified data is transformed into a predictable CRM schema.
6. **Persistence** — structured lead records are appended to Google Sheets.
7. **Operational alerting** — a formatted Discord webhook notification surfaces the lead immediately.

## Stack

- **Vapi** — AI voice intake
- **n8n** — workflow orchestration
- **JavaScript** — payload normalization and transformation inside n8n
- **REST / HTTP webhooks** — event ingestion and downstream notifications
- **Google Sheets API / n8n node** — lightweight CRM persistence
- **Discord webhooks** — operational alerts
- **PowerShell** — client-specific launcher and environment loading

## Engineering decisions demonstrated

### Normalize at the boundary
Incoming payloads are converted into a consistent internal schema before downstream routing. That reduces coupling between the voice provider payload and CRM/notification steps.

### Environment-based client configuration
The launcher loads client-specific values from `.env` files rather than committing secrets. Secret values printed for diagnostics are masked.

### Explicit spam routing
The workflow separates suspected junk calls from qualified leads using both a boolean junk flag and configurable score threshold.

### Separate persistence from alerting
The CRM write and Discord notification are independent downstream actions, making it easier to replace either destination without redesigning intake logic.

## Repository structure

```text
clients/
  example/              # example client environment/config

docs/
  QUICKSTART.md          # local setup and import notes

launcher/
  run-client.ps1         # loads client env and launches n8n

workflows/
  workflow.fixed.json    # recruiter-safe n8n workflow export
```

## Run locally

Prerequisites:

- n8n installed and available from PowerShell
- Google Sheets credentials configured in n8n
- a Vapi agent configured to send the expected payload
- a Discord webhook for alerts

From the repository root:

```powershell
Copy-Item .\clients\example\.env.example .\clients\example\.env
# Fill in the required values, then:
.\launcher\run-client.ps1 -Client example
```

Import `workflows/workflow.fixed.json` into n8n and configure the Google Sheets credential used by the workflow.

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for additional setup notes.

## Example lead fields

The workflow normalizes fields such as:

- caller name and phone number
- email
- address / city / state / ZIP
- service type and issue description
- urgency
- preferred contact method
- best time to call
- call summary
- recording and transcript URLs
- spam score / category / reason

## Security notes

- Client secrets are expected in local `.env` files and excluded from source control.
- The PowerShell launcher masks secret values in diagnostic output.
- Discord messages disable automatic mention parsing.
- This public repository is intended as a sanitized portfolio/reference implementation; production deployments should additionally enforce webhook authentication, access controls, credential rotation, and least-privilege service accounts.

## What this demonstrates

This project is evidence of practical API-integration work across webhook ingestion, payload normalization, environment configuration, conditional routing, SaaS persistence, notification APIs, and operational troubleshooting—not just a workflow screenshot.
