"""Smoke tests for the attack algorithm structure (not a full replay test)."""

from aicomp_sdk.attacks import AttackAlgorithmBase

from jed_redteam.attack import AttackAlgorithm


def test_attack_algorithm_subclasses_base():
    assert issubclass(AttackAlgorithm, AttackAlgorithmBase)


def test_attack_algorithm_instantiates():
    algo = AttackAlgorithm()
    assert algo.config == {}


def test_attack_algorithm_accepts_config():
    algo = AttackAlgorithm(config={"seed": 42})
    assert algo.config == {"seed": 42}
