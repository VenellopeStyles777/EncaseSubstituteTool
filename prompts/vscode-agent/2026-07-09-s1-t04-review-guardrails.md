# 2026-07-09 - S1-T04 Review Guardrails

Use these guardrails if the VS Code implementation agent asks how far to take the intake command.

```text
S1-T04 should compose existing pieces into JSON-friendly intake output.

Do:
- call segment discovery
- call/inject an EWF reader adapter
- return stable JSON-serializable output
- handle normal invalid input predictably
- test without real evidence
- document the command/callable

Do not:
- add SQLite persistence; that is S1-T05
- parse real EWF bytes
- require pyewf/libewf
- add filesystem parsing
- add UI
- create or commit real E01 evidence
```
