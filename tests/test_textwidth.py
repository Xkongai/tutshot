from tutshot.textwidth import char_width, display_width, expand_tabs, has_wide, wrap_cells


def test_char_width():
    assert char_width("a") == 1
    assert char_width("你") == 2
    assert char_width("，") == 2  # fullwidth comma
    assert char_width("こ") == 2
    assert char_width("\u0301") == 0  # combining accent
    assert char_width("…") == 1


def test_display_width():
    assert display_width("hello") == 5
    assert display_width("你好，世界") == 10
    assert display_width('say "你好"') == 10
    assert has_wide("abc你") and not has_wide("abc")


def test_wrap_latin():
    assert wrap_cells("abcdefghij", 4) == ["abcd", "efgh", "ij"]
    assert wrap_cells("", 10) == [""]


def test_wrap_cjk_never_splits_wide_char():
    rows = wrap_cells("ab你好世界", 5)
    assert rows == ["ab你", "好世", "界"]
    assert all(display_width(r) <= 5 for r in rows)


def test_wrap_indent():
    rows = wrap_cells("abcdefgh", 4, indent=2)
    assert rows == ["abcd", "  ef", "  gh"]
    assert all(display_width(r) <= 4 for r in rows)


def test_wrap_mixed_respects_width():
    line = "输出: " + "数据" * 30 + " done"
    for cols in (7, 20, 41):
        assert all(display_width(r) <= cols for r in wrap_cells(line, cols))
        assert "".join(wrap_cells(line, cols)) == line


def test_expand_tabs():
    assert expand_tabs("a\tb") == "a   b"
    assert expand_tabs("你\tb") == "你  b"
