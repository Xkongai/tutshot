"""Display-width helpers: East Asian wide characters take two terminal columns."""

from __future__ import annotations

import unicodedata

TAB_SIZE = 4


def char_width(ch: str) -> int:
    """Number of terminal columns a single character occupies (0, 1 or 2)."""
    if not ch:
        return 0
    if unicodedata.combining(ch) or ch in "\u200b\u200c\u200d\ufe0f":
        return 0
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 2
    return 1


def is_wide(ch: str) -> bool:
    return char_width(ch) == 2


def display_width(text: str) -> int:
    """Total terminal columns of ``text`` (CJK counts as 2)."""
    return sum(char_width(ch) for ch in text)


def has_wide(text: str) -> bool:
    return any(is_wide(ch) for ch in text)


def expand_tabs(line: str, tab: int = TAB_SIZE) -> str:
    out, col = [], 0
    for ch in line:
        if ch == "\t":
            n = tab - (col % tab)
            out.append(" " * n)
            col += n
        else:
            out.append(ch)
            col += char_width(ch)
    return "".join(out)


def wrap_cells(line: str, cols: int, indent: int = 0) -> list[str]:
    """Hard-wrap ``line`` so that no row exceeds ``cols`` display columns.

    Wrapping is character based, like a real terminal. A wide character never
    gets split across rows: if it does not fit, it moves to the next row.
    Continuation rows are prefixed with ``indent`` spaces.
    """
    if cols < 2:
        raise ValueError("cols must be >= 2")
    indent = max(0, min(indent, cols // 2))
    line = expand_tabs(line)
    rows: list[str] = []
    cur: list[str] = []
    n = 0
    for ch in line:
        w = char_width(ch)
        if n + w > cols and cur:
            rows.append("".join(cur))
            cur = [" " * indent] if indent else []
            n = indent
        cur.append(ch)
        n += w
    rows.append("".join(cur))
    return rows
