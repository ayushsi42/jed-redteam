# jed-redteam

Attack-search development for the Kaggle competition
[AI Agent Security — Multi-Step Tool Attacks](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks)
(the SDK's internal codename is **JED**: Replay-Based Security Benchmark for
Tool-Using AI Agents).

You write a search algorithm that finds multi-step tool-call chains which
break a tool-using LLM agent's security guardrails (exfiltration, destructive
writes, confused deputy, untrusted-to-action). See [`study.md`](study.md) for
the full study plan and links.

## Layout

```
src/jed_redteam/attack.py    real development happens here (proper package, importable, testable)
scripts/build_submission.py  bundles src/jed_redteam/attack.py -> submission/attack.py (flat, Kaggle-ready)
submission/attack.py         generated file — what actually gets pasted into a Kaggle notebook
tests/                       pytest unit tests for attack.py structure
docs/kaggle_submission_guide.md   exact steps + constraints for submitting via the Kaggle Notebook UI
vendor/                      local reference copies of the competition SDK source (gitignored, not our code)
study.md                     6-day study plan: scoring rubric, tool surface, search-strategy background
```

Kaggle's code-competition harness only accepts a single flat `attack.py`
with no local package imports — that's why development happens in a real
package under `src/` and gets flattened before each Kaggle push, instead of
editing `submission/attack.py` directly.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Local iteration loop

```bash
source venv/bin/activate

# after editing src/jed_redteam/attack.py:
python scripts/build_submission.py

pytest tests/ -q

cd submission
aicomp validate redteam attack.py
aicomp test redteam attack.py --budget-s 60 --agent deterministic   # fast loop, saves history
aicomp evaluate redteam attack.py --budget-s 60 --agent deterministic --env gym   # scorer-parity run
aicomp history
aicomp compare <run1> <run2>
```

## Submitting to Kaggle

CLI upload does not work for this competition (confirmed: `kaggle
competitions submit` returns `400 Bad Request`). It's a Code Competition —
submission happens from inside a Kaggle Notebook. See
[`docs/kaggle_submission_guide.md`](docs/kaggle_submission_guide.md) for the
exact steps and the real evaluation constraints (8750s budget, GPT-OSS +
Gemma agents, public/private guardrail split, 0–1000 normalized score).

## Deadline

2026-09-01 23:59 UTC.
