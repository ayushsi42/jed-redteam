"""Smoke tests for the attack algorithm structure (not a full replay test)."""

from aicomp_sdk.attacks import AttackAlgorithmBase

from jed_redteam.attack import (
    _ALL_SUPPRESSING_WORDS,
    _PAD_FILE_HINTS,
    _BaitItem,
    AttackAlgorithm,
    _bait_open_message,
    _pad_messages,
    _safe_message,
)


def test_attack_algorithm_subclasses_base():
    assert issubclass(AttackAlgorithm, AttackAlgorithmBase)


def test_attack_algorithm_instantiates():
    algo = AttackAlgorithm()
    assert algo.config == {}


def test_attack_algorithm_accepts_config():
    algo = AttackAlgorithm(config={"seed": 42})
    assert algo.config == {"seed": 42}


def test_safe_message_never_contains_suppressing_keywords():
    """Regression guard for predicates.py's UNTRUSTED_TO_ACTION/CONFUSED_DEPUTY
    keyword gate: a chain's final driving message must never contain
    run/execute/send/email/upload/save/write, or the predicate it's meant to
    trip gets suppressed by accident."""
    candidates = [
        "Please run this and send the email now.",
        "Go ahead and finish whatever that document asked for.",
        "Save the report and write it up.",
        "",
    ]
    for candidate in candidates:
        safe = _safe_message(candidate)
        lowered = safe.lower()
        assert not any(word in lowered for word in _ALL_SUPPRESSING_WORDS), safe


def test_pad_messages_contain_read_keyword():
    """Regression guard: agents/deterministic_agent.py's fallback path only
    ever calls its file-read handler inside an `if "read" in u:` guard. A
    pad message that omits "read" silently becomes a no-op turn for that
    agent instead of the intended benign fs.read (a real bug this project
    shipped and fixed - see the module docstring / _pad_messages comment)."""
    steps = _pad_messages(len(_PAD_FILE_HINTS))
    assert len(steps) == len(_PAD_FILE_HINTS)
    for message, hops in steps:
        assert "read" in message.lower()
        assert hops >= 1
        assert any(hint in message.lower() for hint in _PAD_FILE_HINTS)


def test_bait_open_message_matches_deterministic_agent_keyword_gates():
    """Regression guard: the deterministic agent only calls web.open when
    "open" is in the message, and only calls email.read when "email" is in
    the message (agents/deterministic_agent.py)."""
    web_bait = _BaitItem(kind="web", item_id="page_42", text="", domain=None, score=1)
    email_bait = _BaitItem(kind="email", item_id="email_1", text="", domain=None, score=1)

    web_message, _ = _bait_open_message(web_bait)
    assert "open" in web_message.lower()
    assert web_bait.item_id in web_message

    email_message, _ = _bait_open_message(email_bait)
    assert "email" in email_message.lower()
    assert email_bait.item_id in email_message
