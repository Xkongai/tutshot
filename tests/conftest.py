from pathlib import Path

import pytest

from tutshot import fonts

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures() -> Path:
    return FIXTURES


has_cjk_font = fonts.find_cjk() is not None
needs_cjk = pytest.mark.skipif(not has_cjk_font, reason="no CJK font installed (e.g. fonts-noto-cjk)")
