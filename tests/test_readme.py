"""Unit tests for README.md — the GitHub profile page."""

import re
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
README_PATH = ROOT_DIR / "README.md"


@pytest.fixture
def readme():
    return README_PATH.read_text(encoding="utf-8")


# ── File-level checks ──────────────────────────────────────────────


class TestFileIntegrity:
    def test_readme_exists(self):
        assert README_PATH.is_file(), "README.md must exist at the repo root"

    def test_readme_is_not_empty(self, readme):
        assert len(readme.strip()) > 0

    def test_readme_is_reasonable_size(self, readme):
        assert len(readme) < 50_000, "README should not be excessively large"


# ── Required sections / headings ────────────────────────────────────


class TestStructure:
    def test_has_top_level_heading(self, readme):
        assert re.search(r"^#\s+", readme, re.MULTILINE), (
            "README should contain at least one top-level heading"
        )

    def test_has_tech_stack_section(self, readme):
        assert "tech stack" in readme.lower(), (
            "README should contain a 'Tech Stack' section"
        )

    def test_has_connect_section(self, readme):
        assert "connect with me" in readme.lower(), (
            "README should contain a 'Connect with me' section"
        )

    def test_has_workspace_section(self, readme):
        assert "workspace" in readme.lower(), (
            "README should contain a workspace section"
        )


# ── Links & badges ─────────────────────────────────────────────────


class TestLinksAndBadges:
    def test_contains_profile_link(self, readme):
        assert "adityaseth.in" in readme, (
            "README should link to the personal website"
        )

    def test_has_github_badge(self, readme):
        assert "img.shields.io" in readme, "README should include shield badges"

    def test_linkedin_link_present(self, readme):
        assert "linkedin.com" in readme.lower()

    def test_email_present(self, readme):
        assert re.search(r"mailto:", readme), (
            "README should include a mailto link"
        )


# ── Code block ──────────────────────────────────────────────────────


class TestCodeBlock:
    def test_python_code_block_present(self, readme):
        assert "```python" in readme, (
            "README should contain a Python code block"
        )

    def test_code_block_has_name(self, readme):
        assert 'Name = "Aditya Seth"' in readme

    def test_code_block_has_languages(self, readme):
        assert "Languages" in readme


# ── Images ──────────────────────────────────────────────────────────


class TestImages:
    def test_banner_image_referenced(self, readme):
        assert "banner.png" in readme, "README should reference the banner image"

    def test_banner_file_exists(self):
        banner = ROOT_DIR / "banner.png"
        assert banner.is_file(), "banner.png must exist at the repo root"

    def test_banner_is_not_empty(self):
        banner = ROOT_DIR / "banner.png"
        assert banner.stat().st_size > 0
