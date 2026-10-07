"""jed_redteam: adversarial search algorithm for guardrailed tool-using agents.

This package is where real development happens. The evaluation harness
requires a single flat attack.py with no local imports, so
`scripts/build_submission.py` bundles this package into submission/attack.py
before each build.
"""

from jed_redteam.attack import AttackAlgorithm

__all__ = ["AttackAlgorithm"]
