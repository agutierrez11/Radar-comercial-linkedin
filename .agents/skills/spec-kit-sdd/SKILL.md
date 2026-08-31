---
name: spec-kit-sdd
description: Official GitHub Spec-Kit framework for Spec-Driven Development (SDD). Use when defining, planning, architecting, and executing complex software features with executable specifications, constitution guardrails, task breakdown, and convergence verification before writing code.
version: 1.0.0
---

# GitHub Spec Kit (Spec-Driven Development)

**Spec-Driven Development (SDD)** changes software engineering: specifications become executable blueprints, directly driving AI coding agents to generate correct, zero-assumption implementations.

## 🔄 The 7 Phases of SDD Workflow

```
[ 1. Constitution ] ──► Define immutable project rules, principles, and tech constraints.
         │
         ▼
[ 2. Specify ] ──────► Draft the functional specification (user stories, requirements).
         │
         ▼
[ 3. Clarify ] ──────► Resolve ambiguity, edge cases, and underspecified behaviors.
         │
         ▼
[ 4. Plan ] ─────────► Create technical architecture plan (components, schema, APIs).
         │
         ▼
[ 5. Tasks ] ────────► Break down implementation into atomic, ordered, testable tasks.
         │
         ▼
[ 6. Implement ] ────► Execute tasks sequentially with automated tests & live proof.
         │
         ▼
[ 7. Converge ] ─────► Verify compliance against the original spec and checklist.
```

## 🛠️ Included Templates and Directives

1. **`templates/spec-template.md`**: Standard functional specification.
2. **`templates/plan-template.md`**: Architectural blueprint and component diagrams.
3. **`templates/tasks-template.md`**: Task breakdown matrix.
4. **`templates/constitution-template.md`**: Governance and engineering standards.
5. **`templates/checklist-template.md`**: Definition of Done & QA verification.

## 🎯 How to Trigger in Antigravity

- Ask the agent: *"Aplica el flujo de Spec Kit para definir esta nueva feature"*
- Run: `specify init` or use the templates located in `spec-kit-sdd/templates/`
