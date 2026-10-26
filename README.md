# Contractor Intake Automation

This repository documents a voice-intake and lead-routing prototype for home-service contractors. It is a sanitized portfolio case study. It is not a downloadable copy of the working n8n workflow, and it is not a record of a commercial deployment.

## At a glance

| | |
| --- | --- |
| **Business problem** | Contractors miss calls while crews are on jobs. A missed call can mean a lost estimate. |
| **What connects to what** | Vapi voice agent, webhook, n8n, Google Sheets, Discord. |
| **My contribution** | Sole author of this repository. It documents the lead schema, routing rules, and failure handling. The n8n workflow itself stays private. |
| **How it is tested** | The sample workflow in `examples/` was run in a local n8n 2.35.7 with six test events. Results are listed below. Six webhook tests in `tests/` run against the sample workflow in n8n, and GitHub Actions runs them on every push. |
| **Status** | Prototype and ongoing development. No client results are claimed here. |
| **Limitations** | The importable workflow is a simplified fictional sample, not the private build. The Google Sheets and Discord nodes are disabled in it. The tests cover the sample workflow only, not the Vapi, Google Sheets, or Discord steps. The shared secret in the sample is a placeholder in code. Retries and error alerts are described in the architecture notes and are not in the sample. |

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

## Sample workflow you can import

`examples/sample-intake-workflow.json` is a fictional, credential-free n8n workflow with the same shape as the case study. In n8n, use Import from file.

It checks a shared secret in the `x-webhook-secret` header, normalizes the call payload into the lead schema, and routes the result to qualified, junk, or invalid. The Google Sheets and Discord nodes are in place but disabled, because they need accounts. With them off, the qualified path returns the normalized lead as JSON.

Test run in n8n 2.35.7, sending events to the webhook:

| Case | Result |
| --- | --- |
| Valid call with a service request | 200, routed qualified, phone and email normalized |
| No service and sales call wording | 200, routed junk with a reason |
| Missing event id | 400, routed invalid with a reason |
| Wrong secret | 401 |
| No secret header | 401 |
| Empty body | 400 |

The first run showed an IF node letting bad secrets through. I switched it to the current condition format and reran all six cases. The full note is in [docs/DEBUGGING_NOTES.md](docs/DEBUGGING_NOTES.md).

### Run the tests

Import and publish the sample workflow in n8n, start n8n, then run:

```
pip install -r requirements-dev.txt
pytest -v tests
```

The tests send the six cases above to `http://127.0.0.1:5678/webhook/sample-intake`. They skip if nothing is listening. Set `WEBHOOK_URL` or `WEBHOOK_SECRET` to point them somewhere else. The workflow in `.github/workflows/ci.yml` does the same steps on every push.

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

The repository includes a simplified fictional sample workflow for evaluation. It does not include the private production n8n workflow, voice-agent prompt, client configuration, launcher, production webhook addresses, credentials, or production provisioning steps. Those stay private while the project is in development.

## Work with me

I build focused automations that connect intake forms, voice systems, CRMs, spreadsheets, inboxes, and team alerts.

- Portfolio: [bentley-michael.github.io](https://bentley-michael.github.io/)
- Email: [mnbentley@outlook.com](mailto:mnbentley@outlook.com)
