"""A Wi-Fi network name that tells a whole story in 32 characters.

The name is a fixed string, and it is audited by a row of
small named checks before it may be saved: it must exist,
fit inside 32 characters, hide no control characters, be a
single unbroken token, carry the two story words, and hold
letters instead of being marks or digits alone. A name with
a space in it is not one network name, so spaces are refused
outright. Any failing check reports to stderr and exits with
code 1 before anything is written. The output is fully
determined -- no input, no network, no randomness, no clock --
so repeated runs produce identical bytes.
"""

import sys
from pathlib import Path

ENTRY = "ItBurnedDown_ThePasswordDiedToo"
LIMIT = 32
DEST = Path("/output/entry.txt")


def fail(reason):
    print(f"invalid: {reason}", file=sys.stderr)
    raise SystemExit(1)


def check_exists(text):
    if not text or text.strip() == "":
        fail("entry is empty")


def check_short_enough(text):
    if len(text) > LIMIT:
        fail("entry is longer than 32 characters")


def check_free_of_controls(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        fail("entry contains control characters")


def check_single_token(text):
    # A network name on a phone's list is one unbroken token.
    if len(text.split()) != 1:
        fail("entry must be a single token")


def check_tells_the_story(text):
    if "Password" not in text or "Burned" not in text:
        fail("entry must contain Password and Burned")


def check_has_a_letter(text):
    if not any(ch.isalpha() for ch in text):
        fail("entry has no letters")


def check_not_just_marks(text):
    if not any(ch.isalnum() for ch in text):
        fail("entry is punctuation only")


def check_not_just_digits(text):
    if text.isdigit():
        fail("entry is digits only")


def check_no_spaces(text):
    if " " in text:
        fail("entry must not contain spaces")


def check_no_triple_hyphen(text):
    # Three hyphens in a row look like a broken separator, not a name.
    if "---" in text:
        fail("entry must not contain a triple hyphen")


CHECKS = (
    check_exists,
    check_short_enough,
    check_free_of_controls,
    check_single_token,
    check_tells_the_story,
    check_has_a_letter,
    check_not_just_marks,
    check_not_just_digits,
    check_no_spaces,
    check_no_triple_hyphen,
)


def validate(text):
    for check in CHECKS:
        check(text)


def main():
    validate(ENTRY)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
