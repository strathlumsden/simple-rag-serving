# Tool-decision prompt

Goal:
Help me decide whether to use [TOOL] for [FEATURE].

Project context:
[BRIEFLY DESCRIBE PROJECT AND CURRENT STAGE]

Current simple alternative:
[DESCRIBE CURRENT OR STANDARD-LIBRARY APPROACH]

Compare options:
- [OPTION 1]
- [OPTION 2]
- [OPTION 3]

Evaluate each option on:

1. Fit for this project stage.
2. Simplicity.
3. Learning value.
4. Production readiness.
5. Operational burden.
6. Testing implications.
7. Lock-in risk.
8. Performance/scalability.
9. Community/maintenance maturity.
10. What we can defer.

Output:

1. Recommendation for current milestone.
2. Recommendation for production/mature version.
3. What interface we should design so we can swap later.
4. What not to install yet.
5. Questions I should answer before deciding.

Constraints:
- Do not edit files.
- Do not install packages.
- Focus on tradeoffs and decision quality.