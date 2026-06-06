# Review-this-diff prompt

Goal:
Review the current diff as a senior ML/AI systems engineer and tutor.

Focus on:

- Correctness
- Architecture boundaries
- Simplicity
- Test coverage
- Hidden global state
- Unnecessary dependencies
- Data leakage or evaluation leakage
- Security/privacy risks
- Production-readiness concerns
- Whether the change is over-engineered for the current milestone
- Whether the implementation matches the approved plan

Instructions:

- Do not edit files.
- Start with the most important issues.
- Separate blocking issues from non-blocking suggestions.
- Be specific: reference files, functions, or lines where possible.
- Suggest concrete fixes.
- Explain why each issue matters so I can learn from it.

Output format:

1. Summary
2. Blocking issues
3. Non-blocking suggestions
4. Missing tests
5. Architecture/design notes
6. Questions/assumptions
7. Recommended next action