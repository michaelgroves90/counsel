import json
from datetime import UTC, datetime
from pathlib import Path

from counsel.sections import parse_section


def test_parses_fixture_data():
    data = load_fixture_data("eim23100.json")
    section = parse_section(data)
    assert section.section_id == "EIM23100"
    assert section.title == "Car benefit: meaning of car"
    assert section.url == "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim23100"
    assert section.breadcrumbs == ("EIM23000", "EIM23010")
    assert section.updated_at == datetime(2025, 12, 10, tzinfo=UTC)
    assert section.body_html.startswith("<h2>Section 115(1) ITEPA 2003</h2>")


# helpers
def load_fixture_data(filename: str) -> dict:
    path = Path(__file__).parent / "fixtures" / filename
    return json.loads(path.read_text())
    