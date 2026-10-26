# Debugging note: IF node let bad secrets through

This is a short record of one real bug found while testing the sample n8n workflow in `examples/sample-intake-workflow.json`.

## What I was testing

The workflow checks a shared secret in the `x-webhook-secret` header. A request with a wrong or missing secret should get a 401 and stop. A request with the right secret should be routed as qualified, junk, or invalid.

I sent six test events to the webhook on a local n8n 2.35.7 instance.

## What went wrong

On the first run, a wrong secret and a missing secret both returned 200 with a qualified lead. The secret check was not blocking anything.

## Cause

The IF node named Secret valid? was using the older version 2 boolean condition format. It did not evaluate the `secretOk` flag the way I expected, so every request went down the true branch.

## Fix

I replaced the node with IF version 2.2 and set the condition to a boolean "is true" check on `secretOk`. After that, bad secrets went to the 401 response.

## Result after the fix

I reran all six cases and each one behaved as expected.

| Case | Expected | Got |
| --- | --- | --- |
| Valid secret, qualified lead | 200 qualified | 200 qualified |
| Valid secret, junk lead | 200 junk | 200 junk |
| Valid secret, invalid payload | 400 | 400 |
| Wrong secret | 401 | 401 |
| No secret | 401 | 401 |
| Empty body | 400 | 400 |

## What I took from it

- Test the rejection paths, not only the happy path.
- A gate node that fails open is worse than no gate, because it looks like protection.
- Rerun every case after changing a node type or version.

## Limits

The six cases were first run by hand with curl. They are now automated in `tests/test_sample_workflow.py` and run in GitHub Actions on every push. The tests cover the sample workflow only.
