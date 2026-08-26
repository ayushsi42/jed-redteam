"""jed_redteam: attack-search development package for the JED red-team competition.

This package is where real development happens. Kaggle submissions must be a
single flat attack.py with no local imports, so `scripts/build_submission.py`
bundles this package into submission/attack.py before each Kaggle push.
"""

from jed_redteam.attack import AttackAlgorithm

__all__ = ["AttackAlgorithm"]
