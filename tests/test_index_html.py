"""Unit tests for index.html — the landing page redirect."""

import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "index.html"

EXPECTED_REDIRECT_URL = "https://adityaseth.in/"


@pytest.fixture
def html():
    return INDEX_PATH.read_text(encoding="utf-8")


@pytest.fixture
def soup(html):
    return BeautifulSoup(html, "html5lib")


# ── File-level checks ──────────────────────────────────────────────


class TestFileIntegrity:
    def test_index_html_exists(self):
        assert INDEX_PATH.is_file(), "index.html must exist at the repo root"

    def test_file_is_not_empty(self, html):
        assert len(html.strip()) > 0


# ── DOCTYPE & root element ──────────────────────────────────────────


class TestDocumentStructure:
    def test_has_doctype(self, html):
        assert html.strip().lower().startswith("<!doctype html>")

    def test_html_tag_present(self, soup):
        assert soup.find("html") is not None

    def test_html_lang_attribute(self, soup):
        html_tag = soup.find("html")
        assert html_tag is not None
        assert html_tag.get("lang") == "en", "html lang should be 'en'"

    def test_head_tag_present(self, soup):
        assert soup.find("head") is not None

    def test_body_tag_present(self, soup):
        assert soup.find("body") is not None


# ── Meta tags ───────────────────────────────────────────────────────


class TestMetaTags:
    def test_meta_refresh_present(self, soup):
        meta = soup.find("meta", attrs={"http-equiv": "refresh"})
        assert meta is not None, "meta refresh tag must be present"

    def test_meta_refresh_url(self, soup):
        meta = soup.find("meta", attrs={"http-equiv": "refresh"})
        content = meta["content"]
        assert EXPECTED_REDIRECT_URL in content, (
            f"meta refresh should redirect to {EXPECTED_REDIRECT_URL}"
        )

    def test_meta_refresh_delay_is_zero(self, soup):
        meta = soup.find("meta", attrs={"http-equiv": "refresh"})
        content = meta["content"]
        delay = content.split(";")[0].strip()
        assert delay == "0", "redirect delay should be 0 seconds"

    def test_viewport_meta_present(self, soup):
        meta = soup.find("meta", attrs={"name": "viewport"})
        assert meta is not None, "viewport meta tag must be present"

    def test_viewport_includes_width(self, soup):
        meta = soup.find("meta", attrs={"name": "viewport"})
        assert "width=device-width" in meta["content"]


# ── Title ───────────────────────────────────────────────────────────


class TestTitle:
    def test_title_tag_present(self, soup):
        assert soup.find("title") is not None

    def test_title_not_empty(self, soup):
        title = soup.find("title")
        assert title.string is not None and len(title.string.strip()) > 0
