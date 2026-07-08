# Generic Agent Runtime Adapter

A playbook has three parts:

- trigger: when to use it.
- portability notes: what to adapt.
- instructions: the operational procedure.

Minimum runtime capabilities:

- Read and edit files.
- Run shell commands or equivalent validation.
- Preserve a task log or durable notes.
- Ask for explicit approval before gated actions.

If the runtime lacks a capability, treat that as a blocker and report the
missing tool instead of pretending the action happened.
