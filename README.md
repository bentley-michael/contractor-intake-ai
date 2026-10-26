# Contractor Intake Automation

This repository documents a voice-intake and lead-routing prototype for home-service contractors. It is a sanitized portfolio case study. It is not a downloadable copy of the working n8n workflow, and it is not a record of a commercial deployment.

## At a glance

| | |
| --- | --- |
| **Business problem** | Contractors miss calls while crews are on jobs. A missed call can mean a lost estimate. |
| **What connects to what** | Vapi voice agent, webhook, n8n, Google Sheets, Discord. |
| **My contribution** | Sole author of this repository. It documents the lead schema, routing rules, and failure handling. The n8n workflow itself stays private. |
| **How it is tested** | The public repo has no automated tests. It includes one fictional event that shows the data contract. |
| **Status** | Prototype and ongoing development. No client results are claimed here. |
| **Limitations** | The importable workflow is not public, so a reader cannot run it. No automated test suite. Webhook authentication, retries, and error alerts are described as production safeguards in the architecture notes. They are not demonstrated in public code. |

## The problem

Contractors often miss calls while crews are on jobs or after the office closes. A missed call can mean a lost inspection or estimate. The system captures the caller's request, structures the useful details, separates obvious junk, records the lead, and alerts the team.

## What the system does

1. A voice agent collects the caller's contact details, location, service need, and urgency.
2. A webhook sends the call result to n8n.
3. The workflow normalizes inconsistent fields into one lead schema.
4. Spam and incomplete events follow a separate route.
5. Qualified leads are written to Google Sheets.
6. Discord receives a short operational alert so someone can respond.

```text
Voice intake -> webhook -> normalize -> qualify -> record + alert
```

## Implementation notes

- n8n handles orchestration and routing.
- Vapi supplies the structured call result.
- Google Sheets serves as the lightweight lead register.
- Discord provides immediate team notification.
- Client-specific values and credentials stay outside the workflow export.
- Production deployments require webhook authentication, restricted credentials, logging, and error alerts.

The architecture notes explain the boundaries and failure handling without publishing the deployable workflow: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

A fictional event is included to show the data contract: [`examples/sample-intake-event.json`](examples/sample-intake-event.json).

## What is intentionally not public

The repository does not include the importable n8n workflow, voice-agent prompt, client configuration, launcher, webhook addresses, credentials, or production provisioning steps. Those stay private while the project is in development.

## Work with me

I build focused automations that connect intake forms, voice systems, CRMs, spreadsheets, inboxes, and team alerts.

- Portfolio: [bentley-michael.github.io](https://bentley-michael.github.io/)
- Email: [mnbentley@outlook.com](mailto:mnbentley@outlook.com)
