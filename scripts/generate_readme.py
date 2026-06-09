#!/usr/bin/env python3
"""Generate README.md from config.json using shared utility functions.

Eliminates duplicated badge, icon, and link patterns by driving them
from a single data file (config.json) through reusable helpers.
"""

import json
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Shared utilities — each replaces a repeated Markdown/HTML pattern
# ---------------------------------------------------------------------------


def shields_badge(
    label: str,
    value: str,
    logo: Optional[str] = None,
    color: str = "informational",
    logo_base64: Optional[str] = None,
) -> str:
    """Return a Shields.io badge in Markdown image syntax.

    Replaces 14+ hand-written ``![](https://img.shields.io/badge/…)`` lines.
    """
    base = f"https://img.shields.io/badge/{label}-{value}-informational?style=flat"
    if logo:
        base += f"&logo={logo}&logoColor=white"
    elif logo_base64:
        base += f"&logo=data:image/png;base64,{logo_base64}&logoColor=white"
    base += f"&color={color}"
    return f"![]({base})"


def social_link(
    url: str,
    alt: str,
    icon_url: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> str:
    """Return an HTML social-media link with an icon image.

    Replaces 11 near-identical ``<a href=…><img …>`` blocks.
    """
    size_attrs = ""
    if width and height:
        size_attrs = f' width="{width}" height="{height}"'
    return f'<a href="{url}" alt="{alt}"><img{size_attrs} src="{icon_url}">'


def tech_icon(icon_type: str, name: str) -> str:
    """Return an icons8 ``<img>`` tag for a tech-stack icon.

    Replaces 11 manually written ``<img src="https://img.icons8.com/…">`` tags.
    """
    return f'<img src="https://img.icons8.com/{icon_type}/48/000000/{name}.png">'


def github_stats_card(
    username: str,
    theme: str = "radical",
    bg_color: str = "000000",
    border_color: str = "808080",
) -> str:
    """Return a GitHub stats card ``<img>`` tag."""
    base = "https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api"
    params = (
        f"?username={username}&show_icons=true&locale=en&langs_count=20"
        f"&count_private=true&theme={theme}&layout=compact"
        f"&hide_border=false&bg_color={bg_color}&border_color={border_color}"
    )
    return f'<img src="{base}{params}" width=49% height=100%/>'


def github_streak_card(username: str, theme: str = "highcontrast") -> str:
    """Return a GitHub streak stats ``<img>`` tag."""
    base = "https://github-readme-streak-stats.herokuapp.com"
    params = f"?user={username}&theme={theme}&date_format=M%20j%5B%2C%20Y%5D"
    return f'<img src="{base}{params}" alt="{username}" width=49% height=100%/>'


def github_top_langs_card(
    username: str,
    theme: str = "highcontrast",
    excluded_repos: Optional[list[str]] = None,
) -> str:
    """Return a GitHub top-languages card ``<img>`` tag."""
    base = "https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/top-langs"
    exclude = ",".join(excluded_repos) if excluded_repos else ""
    params = (
        f"?username={username}&langs_count=12&exclude_repo={exclude}"
        f"&show_icons=true&theme={theme}&locale=en&layout=compact"
    )
    return f'<img align="center" src="{base}{params}" alt="{username}" />'


def leetcode_card(username: str) -> str:
    """Return a LeetCode stats card ``<img>`` tag."""
    return f'<img src="https://leetcard.jacoblin.cool/{username}?ext=contest">'


# ---------------------------------------------------------------------------
# README assembly
# ---------------------------------------------------------------------------


def build_readme(cfg: dict) -> str:
    """Assemble the full README.md from *cfg* data and the helpers above."""
    username = cfg["username"]
    lines: list[str] = []

    # Banner + heading
    lines.append("<img src=\"./banner.png\">")
    lines.append("")
    lines.append(f"# {cfg['greeting']}")
    lines.append(
        f"## Click here to visit my website -> [({cfg.get('website_display', cfg['website'])})]({cfg['website']})"
    )
    lines.append("")

    # Profile badges
    lines.append(
        f"![ ](https://komarev.com/ghpvc/?username={username}&color=blue)"
    )
    lines.append("</a>")
    lines.append(
        f'<a href="https://github.com/{username}?tab=followers">'
        f'<img src="https://img.shields.io/github/followers/{username}'
        f'?label=Followers&style=social" alt="GitHub Badge"></a>'
    )
    lines.append(
        f'<a href ="https://metrics.lecoq.io/insights/{username}">'
        f'<img src="https://img.shields.io/badge/-informational?'
        f'&label=GitHub+Metrics&style=social"/></a>'
    )
    lines.append("</p>")
    lines.append("")
    lines.append("")

    # Bio code block
    bio = cfg["bio"]
    lines.append("```python")
    for key, val in bio.items():
        lines.append(f'{key} = {json.dumps(val)}')
    lines.append("```")

    # Commented-out gif (preserve original)
    lines.append(
        '<!-- <div align=center>\n  \n'
        f'[![coding speed x 1000](/images/187495.gif)](https://github.com/{username})\n'
        '</div> !-->'
    )
    lines.append("")

    # Spotify
    lines.append("  ")
    lines.append("### Wanna listen to what I am listening to ? :)  ")
    lines.append("")
    uid = cfg["spotify_uid"]
    lines.append("<div align=center> ")
    lines.append("  ")
    lines.append(
        f"![https://spotify-github-profile.vercel.app/api/view.svg?uid={uid}"
        f"&redirect=true](https://spotify-github-profile.vercel.app/api/view.svg"
        f"?uid={uid}&cover_image=true&theme=natemoo-re&show_offline=false"
        f"&background_color=121212&interchange=true&bar_color=53b14f&bar_color_cover=false)"
    )
    lines.append("  ")
    lines.append("</div>")
    lines.append("")
    lines.append("")
    lines.append("")

    # Workspace
    lines.append("## \U0001f4bb My workspace")
    lines.append("")
    for b in cfg["workspace_badges"]:
        lines.append(
            shields_badge(
                b["label"],
                b["value"],
                logo=b.get("logo"),
                color=b["color"],
                logo_base64=b.get("logo_base64"),
            )
        )
    lines.append("")

    # Tech stack
    lines.append("### Tech Stack:")
    lines.append('<div align=center>  ')
    lines.append("")
    for icon in cfg["tech_stack"]:
        lines.append(tech_icon(icon["type"], icon["name"]))
    lines.append("")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append("")

    # Social links
    lines.append("### Connect with me:")
    lines.append("<div align=center>")
    lines.append("")
    parts: list[str] = []
    for i, link in enumerate(cfg["social_links"]):
        s = social_link(
            link["url"],
            link["alt"],
            link["icon_url"],
            width=link.get("width"),
            height=link.get("height"),
        )
        # First two links get " &nbsp;" separators
        if i < 2:
            s += " &nbsp;"
        parts.append(s)
    lines.append("\n".join(parts))
    lines.append("")
    lines.append("")
    lines.append("  </div>")
    lines.append("")

    # Explored OS
    lines.append("## \U0001f4bb My explored OS's :)")
    lines.append("")
    for b in cfg["os_badges"]:
        lines.append(
            shields_badge(b["label"], b["value"], logo=b["logo"], color=b["color"])
        )
    lines.append("")

    # LeetCode
    lines.append("### LeetCode Stats :")
    lines.append('<div align="center">')
    lines.append("")
    lc = cfg["leetcode_username"]
    lines.append(f'<a href="https://leetcode.com/{lc}/">{leetcode_card(lc)}')
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append("")

    # GitHub statistics
    stats = cfg["stats"]
    lines.append("### Statistics :  ")
    lines.append('<div align="center">')
    lines.append(f'   <a href="https://github.com/{username}">')
    lines.append(" ")
    lines.append(
        "   "
        + github_stats_card(
            username,
            theme=stats["github_stats_theme"],
            bg_color=stats["github_stats_bg"],
            border_color=stats["github_stats_border"],
        )
    )
    lines.append("   </a>")
    lines.append(f'   <a href="https://github.com/{username}">')
    lines.append(
        "   " + github_streak_card(username, theme=stats["streak_theme"])
    )
    lines.append("   <br/>")
    lines.append("   </a>")
    lines.append("</div>")
    lines.append(" ")
    lines.append("<div align=center> ")
    lines.append(
        "<p>"
        + github_top_langs_card(
            username,
            theme=stats["top_langs_theme"],
            excluded_repos=stats.get("excluded_repos"),
        )
        + "</p>"
    )
    lines.append("")
    lines.append("</div>")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    config_path = repo_root / "config.json"

    if not config_path.exists():
        print(f"Error: {config_path} not found", file=sys.stderr)
        sys.exit(1)

    cfg = json.loads(config_path.read_text())
    readme = build_readme(cfg)
    readme_path = repo_root / "README.md"
    readme_path.write_text(readme)
    print(f"Generated {readme_path}")


if __name__ == "__main__":
    main()
