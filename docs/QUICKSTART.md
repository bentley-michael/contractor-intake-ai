```markdown

# QUICKSTART — Crawl Space & Foundation Repair Intake (Vapi) MVP

Steps to run the packaged product locally and import into n8n.

1) Create a client env

	- Copy `clients/example/.env.example` → `clients/<client>/.env` and fill the secret values.

2) Launch n8n with the client env

```powershell
.\products\contractor-intake-crawlspace-mvp\launcher\run-client.ps1 -Client <client>
```

3) Import the workflow into n8n

	- Preferred: import `products\contractor-intake-crawlspace-mvp\workflows\workflow.json`
	- If the import fails, use `products\contractor-intake-crawlspace-mvp\workflows\workflow.bundle.json` instead (array-wrapped export).

4) Google Sheets setup

	- Create a Google Sheet and add two tabs named `Leads` and `Spam`.
	- Paste both header lines (two header rows) into each sheet as expected by your team schema.


Service account / spreadsheet sharing

	- If the workflow uses a Google service account, share the target spreadsheet to the service account email (found in your service account JSON) and grant the service account Editor access. This is required for the n8n Google Sheets nodes to write rows.

Troubleshooting

- "Could not import file: does not contain valid JSON data"
  - Confirm you selected the correct file (`workflow.json` or `workflow.bundle.json`).
  - Try `workflow.bundle.json` (some n8n imports expect an array). 
  - Validate the JSON locally: `python -c "import json,sys; json.load(open('products/contractor-intake-crawlspace-mvp/workflows/workflow.json','r',encoding='utf-8')); print('OK')"`
  - Ensure files are saved as UTF-8 (no BOM) — edit in VS Code and re-save with UTF-8.

- PSReadLine / console paste crash
  - Avoid pasting large heredocs into an interactive terminal (PowerShell PSReadLine sometimes crashes). Edit files in VS Code instead and re-run the launcher.

If you need help with Google Sheets headers or sample .env values, open `products/contractor-intake-crawlspace-mvp/clients/example/.env.example`.

Verify env vars loaded

	- The launcher prints a small debug summary before starting n8n showing `Client` and `SHEET_ID` and masked secret values. Confirm the `SHEET_ID` shown matches your spreadsheet.
	- Alternatively, temporarily add a Client Config debug node in your n8n workflow to emit the env values to a log/console while troubleshooting.
