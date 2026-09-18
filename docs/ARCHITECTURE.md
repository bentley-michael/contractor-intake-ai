# Architecture notes

## System boundary

The automation starts after the voice platform finishes or updates a call. It accepts a structured event, converts it into a stable internal record, applies routing rules, and sends the result to the contractor's operating tools.

## Data flow

| Stage | Responsibility | Failure handling |
| --- | --- | --- |
| Intake | Receive the call event over HTTPS | Reject unauthenticated or malformed requests |
| Normalize | Map provider fields to the lead schema | Preserve the raw event ID for investigation |
| Qualify | Separate useful leads from junk or incomplete calls | Record the route and reason |
| Persist | Append the lead to the selected CRM or sheet | Retry transient failures and alert on final failure |
| Notify | Send a short message to the operating team | Keep notification failure separate from lead storage |

## Lead contract

The internal record keeps only the fields needed for follow-up:

- event and call identifiers
- caller name and contact details
- service location
- requested service and problem summary
- urgency and preferred contact time
- qualification status and reason

Recording and transcript links are optional. A production deployment should apply a retention policy and avoid copying sensitive call content into alerts.

## Design choices

**Normalize once.** Provider-specific field names are handled at the boundary so downstream steps use one predictable schema.

**Store before alerting.** A notification outage should not lose the lead. Persistence and team alerts remain separate operations.

**Make routing explainable.** Junk and incomplete events carry a reason instead of disappearing silently.

**Keep client configuration out of source control.** Credentials, destinations, thresholds, phone numbers, and webhook addresses are supplied at deployment time.

## Production safeguards

- verify webhook signatures or a shared secret
- restrict service-account access to the required destination
- mask contact details in logs
- use bounded retries and an error queue
- alert on repeated delivery failures
- rotate credentials and webhook URLs
- define retention rules for recordings and transcripts

The working n8n export and provisioning instructions are deliberately excluded from this public case study.
