"""Recognize a small allowlist of literal Linux Bash submission actions.

This parser does not run or reject ordinary shell commands. It only distinguishes
a submission action from an ordinary action whose output might print the marker.
"""
from __future__ import annotations

import re
import shlex


SUBMISSION_MARKER = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"


def _literal_syntax(source: str) -> bool:
    # None of the allowed literal words need shell expansion or these escapes.
    if "$" in source or "`" in source or re.search(r"\\[;&|<>()\n]", source):
        return False
    quote = None
    index = 0
    while index < len(source):
        char = source[index]
        if quote == "'":
            if char == "'":
                quote = None
            elif char in ";&|<>()\n":
                return False
        elif char == "\\":
            index += 1
        elif quote == '"':
            if char == '"':
                quote = None
            elif char in ";&|<>()\n":
                return False
        elif char in "'\"":
            quote = char
        index += 1
    return quote is None


def is_submission_action(command: str) -> bool:
    """Accept only ``echo MARKER`` or ``cd /work && echo MARKER``.

    Literal words can be quoted/escaped, and one trailing semicolon is allowed.
    Blank leading/trailing lines and continuation newlines after ``&&`` are safe;
    a newline between ordinary words remains a command boundary. This is a
    conservative allowlist, not a general Bash parser.
    """
    if not isinstance(command, str):
        return False
    source = command.replace("\r\n", "\n")
    if "\r" in source or not _literal_syntax(source):
        return False
    lexer = shlex.shlex(source, posix=True, punctuation_chars=";&|<>()")
    lexer.whitespace = " \t"
    lexer.whitespace_split = False
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        return False
    while tokens and tokens[0] == "\n":
        tokens.pop(0)
    while tokens and tokens[-1] == "\n":
        tokens.pop()
    if tokens and tokens[-1] == ";":
        tokens.pop()
    if tokens == ["echo", SUBMISSION_MARKER]:
        return True
    if tokens[:3] != ["cd", "/work", "&&"]:
        return False
    tail = tokens[3:]
    while tail and tail[0] == "\n":
        tail.pop(0)
    return tail == ["echo", SUBMISSION_MARKER]


def non_submission_notice(command: str, output: str) -> str:
    """Explain marker output from an ordinary action without blocking that action."""
    if is_submission_action(command) or not any(
        line.strip() == SUBMISSION_MARKER for line in output.splitlines()
    ):
        return ""
    return f"not submitted, run echo {SUBMISSION_MARKER} to submit"
