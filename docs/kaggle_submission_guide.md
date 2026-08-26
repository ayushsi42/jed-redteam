# How to submit on Kaggle (Code Competition)

This competition scores submissions by running your `attack.py` inside a
Kaggle Notebook rerun (`KAGGLE_IS_COMPETITION_RERUN`), driven by
`kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py`. You never touch
the gateway file — Kaggle owns it. You only provide `attack.py`.

CLI file upload (`kaggle competitions submit`) does NOT work for this
competition — confirmed, it returns `400 Bad Request`. You must submit from
inside a Kaggle Notebook using the "Submit to Competition" button.

## Steps

1. Go to the competition page → **Code** tab → **New Notebook**
   (or fork an existing public starter notebook, e.g. search "attack.py
   starter" in the Code tab).
2. Add the competition as a data source if it isn't already attached
   (Notebook editor → **Add Input** → search the competition name — this
   attaches `aicomp_sdk` and `kaggle_evaluation` as read-only inputs).
3. In the first cell, install the SDK (pin the version you tested locally):

```python
!pip install -q aicomp-sdk==3.1.2
```

4. First run `python scripts/build_submission.py` locally to regenerate
   `submission/attack.py` from `src/jed_redteam/attack.py` (the real
   development file). Then, in the next notebook cell, write it out with
   `%%writefile` — paste the full contents of `submission/attack.py` after
   the `%%writefile` line:

```python
%%writefile attack.py
# <<< PASTE THE FULL CONTENTS OF submission/attack.py BELOW THIS LINE >>>
```

5. Validate it inside the notebook (same as local):

```python
!aicomp validate redteam attack.py
```

6. (Optional but recommended) Run a short local-style test inside the
   notebook to sanity check before using a submission slot:

```python
!aicomp test redteam attack.py --budget-s 60 --agent deterministic
```

7. Click **Save Version** → **Save & Run All (Commit)**. Once the commit
   finishes successfully, go to the notebook's output page and click
   **Submit to Competition**. This is what actually triggers
   `KAGGLE_IS_COMPETITION_RERUN=1` and runs your attack against the real
   gateway (GPT-OSS + Gemma agents, full ~2.4h budget, public + private
   guardrail split).

## Notes specific to this competition (learned from the SDK source)

- Real evaluation budget is **8750 seconds (~2.4 hours)** total
  (`DEFAULT_BUDGET_S` in `jed_attack_gateway.py`), not the 60s used for local
  smoke tests.
- Your attack is replayed against **two agents**: GPT-OSS and Gemma.
- Each agent is scored against **two guardrails**: the public
  `OptimalGuardrail` (visible score) and a private guardrail (private
  leaderboard only).
- `submission.csv` output format (written automatically by the gateway, you
  don't write this yourself):
  ```
  Id,Score
  gpt_oss_public,0.05
  gpt_oss_private,0.02
  gemma_public,0.05
  gemma_private,0.02
  ```
- Final leaderboard score is a **normalized attack score, 0–1000**.
- Do not register hooks or try to introspect the compromised-env internals —
  the SDK docstring in the starter `attack.py` explicitly warns
  "compromised-env hooks are a harness-owned concern, not a submission API."

## What we already verified locally (2026-08-26)

- `aicomp-sdk==3.1.2` installs cleanly from PyPI into `venv/`.
- `aicomp validate redteam attack.py` → passes on the untouched starter
  template.
- `aicomp test redteam attack.py --budget-s 60 --agent deterministic` →
  runs end-to-end, 0 findings (expected — stub logic).
- `aicomp evaluate redteam attack.py --budget-s 60 --agent deterministic --env gym`
  → runs end-to-end, Attack Score 0.00, writes `evaluation_artifacts/score.txt`
  and `report.json` (this mirrors Kaggle's scoring path most closely).
- Direct CLI submission (`kaggle competitions submit`) is blocked (400) —
  must go through a Notebook.
