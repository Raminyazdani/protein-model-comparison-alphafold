# Copilot Instructions — Portfolio-ready + Step-Expanded Git Historian (Single Project Repo)

You are working in a repository that contains **ONE** project (already split into its own GitHub repo).

## Mission (do in order)
### A) Catch-up audit (verify previous run first)
The repo may already have been processed by an earlier “portfolio-ready + historian” run. **Do not assume it is complete.**
1) Re-check every required deliverable exists and contains real content:
   - `project_identity.md`, `README.md`, `report.md`, `suggestion.txt`, `suggestions_done.txt`
2) Re-check the ledgers are coherent:
   - Every entry in `suggestion.txt` ends as `STATUS=APPLIED` or `STATUS=NOT_APPLIED` (with reason).
   - Every applied change appears in `suggestions_done.txt` (with before/after + locator).
3) Re-check reproducibility verification:
   - If tests exist: run them.
   - Else: perform a minimal smoke-run.
   - Record exact commands + outcomes in `report.md`.
4) Re-check historian correctness (if `history/` exists):
   - No snapshot contains `history/` or `.git/`.
   - Final snapshot matches the repo’s final working tree **byte-for-byte** (excluding `history/`).
If anything is missing / inconsistent, fix it first (no feature creep), and update `report.md` + ledgers.

### B) Portfolio-ready adjustments (only what’s missing)
Only do additional refactors/renames/path fixes **if they are still needed** to satisfy the original portfolio-ready goals.
- Keep changes behavior-preserving unless a fix is required to make the project runnable.
- Never add secrets; use env vars + `.env.example` if needed.
- Never fabricate datasets; document how to obtain them and where to place them.

### C) Step-expanded Git Historian regeneration (history/ only)
The goal of this run is to **increase the number of historian steps** while keeping the final state identical.

#### Step expansion rule (strict)
If an existing historian run is present:
- Let `N_old = count(history/steps/step_*)`
- You MUST regenerate a new historian run with:
  - `N_new >= ceil(N_old * 1.5)`
  - Step numbering is **sequential integers only**: `step_01 ... step_N_new`
  - NO decimals (no “3.5”), no alternate naming.

If there is no existing historian run:
- Create a realistic history with **at least 15 steps** (still sequential integers).

#### How to add steps without feature creep
Use BOTH strategies as needed:

1) **Split overly-large commits into smaller commits**
   - Example splits:
     - README structure vs. dependency pinning vs. path fixes
     - formatting cleanup vs. refactor vs. documentation
   - Each commit should change a small, coherent set of files.

2) **Insert at least one “oops → hotfix” sequence**
   - Create a plausible mistake in an intermediate step (NOT in the final repo state).
   - Immediately fix it in the next step.
   - The mistake must be small and realistic (examples):
     - a broken import / wrong module path
     - a README run command that’s slightly wrong
     - a misnamed config key / env var
     - a workflow/tooling config typo (ONLY if such tooling exists in final state)
   - The fix step must clearly resolve it.
   - Document both the mistake and the fix in `history/github_steps.md`.

#### Required documentation for expanded history
In `history/github_steps.md`, add a section near the top:

**“History expansion note”**
- `N_old`, `N_new`, and the multiplier you achieved.
- A mapping of “old step groups → new step ranges” (e.g., old step 03 became new steps 03–05 because of an inserted oops/hotfix pair).
- At least one explicit “oops → hotfix” description.

#### Snapshot rules (non-negotiable)
- Historian outputs go ONLY under `history/`.
- Snapshots MUST exclude:
  - `.git/`
  - `history/`
- Final snapshot must match the final working tree exactly (excluding `history/`).

## Stop condition
Only stop when:
- all required deliverables exist and contain real content,
- `report.md` ends with a complete self-audit checklist,
- historian snapshots exist with sequential integer numbering,
- `N_new >= ceil(N_old * 1.5)` (when `N_old` existed),
- final snapshot matches the final working tree (excluding `history/`),
- no snapshot includes `history/` (no recursion).
