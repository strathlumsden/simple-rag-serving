# Refactor-with-constraints prompt

Goal:
Refactor the following area of the codebase:

[FILES / COMPONENT]

Problem:
[DESCRIBE WHAT FEELS MESSY OR HARD TO EXTEND]

Desired outcome:
[DESCRIBE TARGET SHAPE]

Learning goal:
I want to understand the architectural reason for this refactor, not just get cleaner code.

Constraints:
- Preserve existing behavior.
- Keep public schemas/interfaces backward-compatible unless explicitly approved.
- Do not add new dependencies.
- Keep the diff focused.
- Update tests if needed.
- Follow AGENTS.md.
- Do not combine this refactor with new features.

Workflow:
First inspect the relevant files and propose a refactor plan.
Do not edit until I approve the plan.

In the plan, include:

1. What will move where.
2. What behavior should remain unchanged.
3. What tests protect the refactor.
4. Risks.
5. Rollback strategy.
6. Why this improves the architecture.
7. What tradeoff this introduces.

Verification:
Run:

uv run ruff check .
uv run ruff format --check .
uv run pytest

After implementation, summarize:

1. Files changed.
2. What changed structurally.
3. Why behavior should be unchanged.
4. Tests run and results.
5. What I should inspect in the diff.