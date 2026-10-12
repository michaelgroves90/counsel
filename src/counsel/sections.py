from dataclasses import dataclass
from datetime import datetime


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
        body_html=data["details"]["body"]
)
    