import re
from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup

MANUAL_LINK = re.compile(
    r"^(?:(?:https?://)?www\.gov\.uk)?/hmrc-internal-manuals/[^/?#]+/([^/?#]+)"
)


@dataclass(frozen=True)
class Section:
    section_id: str
    title: str
    url: str
    breadcrumbs: tuple[str, ...]
    updated_at: datetime
    body_html: str


def parse_section(data: dict) -> Section:
    return Section(
        section_id=data["details"]["section_id"],
        title=data["title"],
        url=f"https://www.gov.uk{data['base_path']}",
        breadcrumbs=tuple(b["section_id"] for b in data["details"]["breadcrumbs"]),
        updated_at=datetime.fromisoformat(data["public_updated_at"]),
        body_html=data["details"]["body"],
    )


def extract_references(body_html: str) -> tuple[str, ...]:
    soup = BeautifulSoup(body_html, "html.parser")
    ids = (
        m.group(1).upper()
        for a in soup.find_all("a", href=True)
        if (m := MANUAL_LINK.match(a["href"]))
    )
    return tuple(dict.fromkeys(ids))
