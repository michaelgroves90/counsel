import json
from datetime import UTC, datetime
from pathlib import Path

from counsel.sections import extract_references, parse_section

EIM = "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/"


def test_parses_fixture_data():
    data = load_fixture_data("eim23100.json")
    section = parse_section(data)
    assert section.section_id == "EIM23100"
    assert section.title == "Car benefit: meaning of car"
    assert section.url == f"{EIM}eim23100"
    assert section.breadcrumbs == ("EIM23000", "EIM23010")
    assert section.updated_at == datetime(2025, 12, 10, tzinfo=UTC)
    assert section.body_html.startswith("<h2>Section 115(1) ITEPA 2003</h2>")


def test_extracts_references_returns_ids_in_order():
    data = load_fixture_data("eim23100.json")
    section = parse_section(data)
    references = extract_references(section.body_html)
    assert references == (
        "EIM23115",
        "EIM23145",
        "EIM23150",
        "EIM22700",
        "EIM22300",
        "EIM23125",
        "EIM21615",
        "EIM23110",
    )


def test_extracts_references_ignores_links_outside_the_manuals():
    html = (
        '<a href="https://www.legislation.gov.uk/ukpga/2003/1/section/115">ITEPA s115</a>'
        f'<a href="{EIM}eim23150">EIM23150</a>'
    )
    assert extract_references(html) == ("EIM23150",)


def test_extracts_references_excludes_duplicates():
    html = (
        f'<a href="{EIM}eim23150">EIM23150</a>'
        f'<a href="{EIM}eim23450">EIM23450</a>'
        f'<a href="{EIM}eim23150">EIM23150</a>'
    )
    assert extract_references(html) == ("EIM23150", "EIM23450")


def test_extracts_references_id_comes_from_href_not_text():
    html = f'<a href="{EIM}eim23150">Some other text</a>'
    assert extract_references(html) == ("EIM23150",)


def test_extracts_reference_from_link_with_fragment():
    html = f'<a href="{EIM}eim23150#para2">EIM23150</a>'
    assert extract_references(html) == ("EIM23150",)


# helpers
def load_fixture_data(filename: str) -> dict:
    path = Path(__file__).parent / "fixtures" / filename
    return json.loads(path.read_text())
