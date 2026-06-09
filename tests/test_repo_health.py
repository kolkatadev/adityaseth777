"""Unit tests for general repository health and hygiene."""

from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent


# ── Required files ──────────────────────────────────────────────────


class TestRequiredFiles:
    @pytest.mark.parametrize(
        "filename",
        ["README.md", "LICENSE", "index.html", "banner.png"],
    )
    def test_required_file_exists(self, filename):
        assert (ROOT_DIR / filename).is_file(), f"{filename} must exist"

    def test_no_unexpected_top_level_dotfiles(self):
        """Only .git (and test infra files) should be present as dotfiles."""
        dotfiles = [
            p.name
            for p in ROOT_DIR.iterdir()
            if p.name.startswith(".") and p.name != ".git"
        ]
        allowed = {".github", ".gitignore", ".gitattributes"}
        unexpected = set(dotfiles) - allowed
        assert not unexpected, f"Unexpected dotfiles at repo root: {unexpected}"


# ── LICENSE ─────────────────────────────────────────────────────────


class TestLicense:
    def test_license_exists(self):
        assert (ROOT_DIR / "LICENSE").is_file()

    def test_license_is_not_empty(self):
        content = (ROOT_DIR / "LICENSE").read_text(encoding="utf-8")
        assert len(content.strip()) > 0

    def test_license_mentions_copyright(self):
        content = (ROOT_DIR / "LICENSE").read_text(encoding="utf-8").lower()
        assert "copyright" in content or "license" in content or "permission" in content


# ── File encodings ──────────────────────────────────────────────────


class TestEncodings:
    @pytest.mark.parametrize("filename", ["README.md", "index.html", "LICENSE"])
    def test_text_files_are_valid_utf8(self, filename):
        path = ROOT_DIR / filename
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"{filename} is not valid UTF-8")
