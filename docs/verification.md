# Verification

Run from the repository root.

## Compile and behavior tests

These are the same compile and unit-test commands used by [CircleCI](../.circleci/config.yml):

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests
```

On Windows PowerShell, set the import path for the test command explicitly:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

The behavior suite checks the public contract around:

- slot cleanup without invented availability;
- handoff for ineligible or uncertain qualification;
- handoff for empty availability or an unoffered choice;
- exact selected-slot confirmation before a `Booking` value is created;
- changing a selection without carrying the old confirmation forward;
- invalid state transitions.

CircleCI also verifies that the public documentation/proof files expected by the repository remain present.
