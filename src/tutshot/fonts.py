"""Find usable fonts on Linux, macOS and Windows without any extra dependency.

Three roles are resolved:

* ``mono`` – Latin terminal text (JetBrains Mono, Cascadia, Menlo, Consolas, DejaVu, ...)
* ``cjk``  – Chinese / Japanese / Korean glyphs (Noto Sans CJK, Source Han, PingFang, YaHei, ...)
* ``ui``   – window title and captions (Inter, Segoe UI, Helvetica, DejaVu Sans, ...)

Each role can be forced with an environment variable: ``TUTSHOT_MONO_FONT``,
``TUTSHOT_CJK_FONT`` and ``TUTSHOT_UI_FONT`` (a path to a .ttf/.otf/.ttc file).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

FONT_EXTS = {".ttf", ".otf", ".ttc", ".otc"}
CJK_INSTALL_HINT = (
    "no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` "
    "(Debian/Ubuntu), `sudo dnf install google-noto-sans-cjk-fonts` (Fedora), "
    "`brew install --cask font-noto-sans-cjk` (macOS), or set TUTSHOT_CJK_FONT=/path/to/font.ttc"
)


@dataclass(frozen=True)
class FontFace:
    """A loadable font face: file + collection index + optional variable-font instance."""

    path: str
    index: int = 0
    variation: str | None = None  # e.g. "Bold" for variable fonts
    fake_bold: bool = False  # no real bold found: draw with a thin stroke instead

    def load(self, size: int) -> ImageFont.FreeTypeFont:
        return _load(self.path, self.index, self.variation, size)

    @property
    def name(self) -> str:
        try:
            family, style = _load(self.path, self.index, self.variation, 16).getname()
            return f"{family} {style}".strip()
        except OSError:
            return Path(self.path).stem


@dataclass(frozen=True)
class FontPair:
    regular: FontFace
    bold: FontFace

    @property
    def name(self) -> str:
        return self.regular.name.replace(" Regular", "")

    def face(self, bold: bool) -> FontFace:
        return self.bold if bold else self.regular


@lru_cache(maxsize=256)
def _load(path: str, index: int, variation: str | None, size: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(path, size, index=index)
    if variation:
        try:
            font.set_variation_by_name(variation)
        except (OSError, ValueError, AttributeError):
            pass
    return font


def font_dirs() -> list[Path]:
    home = Path.home()
    dirs: list[Path] = []
    if sys.platform == "darwin":
        dirs += [
            Path("/System/Library/Fonts"),
            Path("/System/Library/Fonts/Supplemental"),
            Path("/Library/Fonts"),
            home / "Library/Fonts",
            Path("/opt/homebrew/share/fonts"),
        ]
    elif os.name == "nt":
        windir = os.environ.get("WINDIR", r"C:\Windows")
        dirs.append(Path(windir) / "Fonts")
        local = os.environ.get("LOCALAPPDATA")
        if local:
            dirs.append(Path(local) / "Microsoft/Windows/Fonts")
    dirs += [
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
        home / ".local/share/fonts",
        home / ".fonts",
    ]
    extra = os.environ.get("TUTSHOT_FONT_DIRS")
    if extra:
        dirs = [Path(p) for p in extra.split(os.pathsep) if p] + dirs
    seen, out = set(), []
    for d in dirs:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


@lru_cache(maxsize=1)
def font_index() -> dict[str, str]:
    """Map lower-cased file name -> absolute path for every font file we can see."""
    index: dict[str, str] = {}
    for root in font_dirs():
        if not root.is_dir():
            continue
        for dirpath, _dirs, files in os.walk(root):
            for fn in sorted(files):
                if Path(fn).suffix.lower() in FONT_EXTS:
                    index.setdefault(fn.lower(), os.path.join(dirpath, fn))
    return index


# (regular file, bold file or None, variable-font?) in order of preference.
MONO_CANDIDATES: list[tuple[str, str | None, bool]] = [
    ("jetbrainsmono-regular.ttf", "jetbrainsmono-bold.ttf", False),
    ("jetbrainsmono-variablefont_wght.ttf", None, True),
    ("jetbrainsmono[wght].ttf", None, True),
    ("jetbrainsmononl-regular.ttf", "jetbrainsmononl-bold.ttf", False),
    ("cascadiamono.ttf", None, True),
    ("cascadiacode.ttf", None, True),
    ("cascadiamono-regular.ttf", "cascadiamono-bold.ttf", False),
    ("sf-mono-regular.otf", "sf-mono-bold.otf", False),
    ("menlo.ttc", None, False),
    ("consola.ttf", "consolab.ttf", False),
    ("notosansmono-regular.ttf", "notosansmono-bold.ttf", False),
    ("notosansmono[wdth,wght].ttf", None, True),
    ("notosansmono-variablefont_wdth,wght.ttf", None, True),
    ("dejavusansmono.ttf", "dejavusansmono-bold.ttf", False),
    ("liberationmono-regular.ttf", "liberationmono-bold.ttf", False),
    ("ubuntumono-r.ttf", "ubuntumono-b.ttf", False),
    ("sourcecodepro-regular.ttf", "sourcecodepro-bold.ttf", False),
    ("sourcecodepro-regular.otf", "sourcecodepro-bold.otf", False),
    ("monaco.ttf", None, False),
    ("cour.ttf", "courbd.ttf", False),
]

UI_CANDIDATES: list[tuple[str, str | None, bool]] = [
    ("inter-variablefont_opsz,wght.ttf", None, True),
    ("inter[opsz,wght].ttf", None, True),
    ("inter-variablefont_slnt,wght.ttf", None, True),
    ("inter-regular.ttf", "inter-semibold.ttf", False),
    ("inter-regular.otf", "inter-semibold.otf", False),
    ("segoeui.ttf", "seguisb.ttf", False),
    ("sfns.ttf", None, True),
    ("helveticaneue.ttc", None, False),
    ("helvetica.ttc", None, False),
    ("notosans-regular.ttf", "notosans-semibold.ttf", False),
    ("dejavusans.ttf", "dejavusans-bold.ttf", False),
    ("liberationsans-regular.ttf", "liberationsans-bold.ttf", False),
    ("ubuntu-r.ttf", "ubuntu-m.ttf", False),
    ("arial.ttf", "arialbd.ttf", False),
]

# CJK regular / bold files. For collections the best face is chosen by family name.
CJK_CANDIDATES: list[tuple[str, str | None]] = [
    ("notosanscjk-regular.ttc", "notosanscjk-bold.ttc"),
    ("notosanscjksc-regular.otf", "notosanscjksc-bold.otf"),
    ("notosansmonocjksc-regular.otf", "notosansmonocjksc-bold.otf"),
    ("notosanscjk-regular.otc", "notosanscjk-bold.otc"),
    ("notosanssc-regular.otf", "notosanssc-bold.otf"),
    ("notosanssc-regular.ttf", "notosanssc-bold.ttf"),
    ("notosanssc[wght].ttf", None),
    ("notosanssc-variablefont_wght.ttf", None),
    ("sourcehansans.ttc", None),
    ("sourcehansans-regular.ttc", "sourcehansans-bold.ttc"),
    ("sourcehanssanssc-regular.otf", "sourcehanssanssc-bold.otf"),
    ("sourcehansanssc-regular.otf", "sourcehansanssc-bold.otf"),
    ("pingfang.ttc", None),
    ("hiragino sans gb.ttc", None),
    ("msyh.ttc", "msyhbd.ttc"),
    ("msyh.ttf", "msyhbd.ttf"),
    ("yugothm.ttc", "yugothb.ttc"),
    ("wqy-microhei.ttc", None),
    ("wqy-zenhei.ttc", None),
    ("droidsansfallbackfull.ttf", None),
    ("songti.ttc", None),
    ("stheiti medium.ttc", None),
    ("simsun.ttc", None),
    ("notosansjp-regular.otf", "notosansjp-bold.otf"),
    ("notosansjp[wght].ttf", None),
    ("notosansjp-variablefont_wght.ttf", None),
]

# Preferred faces inside CJK collections (monospaced first so columns line up).
CJK_FAMILY_PREFERENCE = [
    "noto sans mono cjk sc",
    "noto sans cjk sc",
    "source han sans sc",
    "source han sans cn",
    "pingfang sc",
    "microsoft yahei",
    "wenquanyi micro hei mono",
    "wenquanyi micro hei",
    "wenquanyi zen hei mono",
    "noto sans mono cjk jp",
    "noto sans cjk jp",
]


def _collection_index(path: str) -> int:
    if Path(path).suffix.lower() not in {".ttc", ".otc"}:
        return 0
    best, best_rank = 0, len(CJK_FAMILY_PREFERENCE)
    for i in range(32):
        try:
            family = ImageFont.truetype(path, 16, index=i).getname()[0].lower()
        except OSError:
            break
        rank = next((r for r, f in enumerate(CJK_FAMILY_PREFERENCE) if family.startswith(f)), None)
        if rank is not None and rank < best_rank:
            best, best_rank = i, rank
    return best


def _variable_bold(path: str, weight: str) -> str | None:
    try:
        names = ImageFont.truetype(path, 16).get_variation_names()
    except (OSError, ValueError, AttributeError):
        return None
    names = [n.decode() if isinstance(n, bytes) else n for n in names]
    for want in (weight, "Bold", "SemiBold", "Medium"):
        if want in names:
            return want
    return None


def _pair_from(path: str, bold_path: str | None, variable: bool, bold_weight: str = "Bold") -> FontPair:
    index = _collection_index(path)
    if variable:
        bold_var = _variable_bold(path, bold_weight)
        regular = FontFace(path, index, "Regular" if bold_var else None)
        if bold_var:
            return FontPair(regular, FontFace(path, index, bold_var))
        return FontPair(regular, FontFace(path, index, None, fake_bold=True))
    regular = FontFace(path, index)
    if bold_path:
        return FontPair(regular, FontFace(bold_path, _collection_index(bold_path)))
    # Collections such as Menlo.ttc / Helvetica.ttc carry a bold face at another index.
    if Path(path).suffix.lower() in {".ttc", ".otc"}:
        for i in range(1, 16):
            try:
                style = ImageFont.truetype(path, 16, index=i).getname()[1].lower()
            except OSError:
                break
            if style == "bold":
                return FontPair(regular, FontFace(path, i))
    return FontPair(regular, FontFace(path, index, fake_bold=True))


def _from_env(var: str, bold_weight: str = "Bold") -> FontPair | None:
    value = os.environ.get(var)
    if not value:
        return None
    if not Path(value).is_file():
        raise FileNotFoundError(f"{var} points to a missing file: {value}")
    variable = _variable_bold(value, bold_weight) is not None
    return _pair_from(value, None if variable else _sibling_bold(Path(value)), variable, bold_weight)


def _sibling_bold(path: Path) -> str | None:
    """Guess the bold file next to a regular one (Foo-Regular.ttf -> Foo-Bold.ttf, Foo.ttf -> Foo-Bold.ttf)."""
    stem, ext = path.stem, path.suffix
    names = {stem.replace("Regular", "Bold"), stem.replace("-Regular", "-Bold"), f"{stem}-Bold", f"{stem}bd", f"{stem}b"}
    names.discard(stem)
    for name in sorted(names):
        candidate = path.with_name(name + ext)
        if candidate.is_file():
            return str(candidate)
    return None


def _find(candidates, bold_weight: str) -> FontPair | None:
    idx = font_index()
    for reg, bold, variable in candidates:
        path = idx.get(reg)
        if path:
            bold_path = idx.get(bold) if bold else None
            return _pair_from(path, bold_path, variable, bold_weight)
    return None


@lru_cache(maxsize=1)
def find_mono() -> FontPair | None:
    return _from_env("TUTSHOT_MONO_FONT") or _find(MONO_CANDIDATES, "Bold")


@lru_cache(maxsize=1)
def find_ui() -> FontPair | None:
    return _from_env("TUTSHOT_UI_FONT", "SemiBold") or _find(UI_CANDIDATES, "SemiBold")


@lru_cache(maxsize=1)
def find_cjk() -> FontPair | None:
    env = _from_env("TUTSHOT_CJK_FONT")
    if env:
        return env
    idx = font_index()
    for reg, bold in CJK_CANDIDATES:
        path = idx.get(reg)
        if path:
            bold_path = idx.get(bold) if bold else None
            variable = bold is None and _variable_bold(path, "Bold") is not None
            return _pair_from(path, bold_path, variable)
    return None


def clear_cache() -> None:
    """Forget discovered fonts (useful in tests that change environment variables)."""
    for fn in (font_index, find_mono, find_ui, find_cjk):
        fn.cache_clear()
