from app.states.validation_state import (
    _block_to_inspector_fields,
    _chunks_to_blocks,
    _chunks_to_heading_tree,
    _chunks_to_json_lines,
    _chunks_to_markdown_lines,
    _chunks_to_tables,
    _normalize_kind,
)


def test_normalize_kind_passes_through_known_kind():
    assert _normalize_kind("heading") == "heading"


def test_normalize_kind_defaults_unknown_kind_to_unknown():
    assert _normalize_kind("unknown-xyz") == "unknown"


def test_chunks_to_markdown_lines_empty_input_returns_empty_list():
    assert _chunks_to_markdown_lines([]) == []


def test_chunks_to_json_lines_empty_input_returns_empty_list():
    assert _chunks_to_json_lines([]) == []


def test_chunks_to_blocks_empty_input_returns_empty_list():
    assert _chunks_to_blocks([]) == []


def test_chunks_to_tables_empty_input_returns_empty_list():
    assert _chunks_to_tables([]) == []


def test_chunks_to_heading_tree_empty_input_returns_empty_list():
    assert _chunks_to_heading_tree([]) == []


def _sample_chunks():
    return [
        {
            "block_id": "BLK-1",
            "kind": "heading",
            "text": "제1장 총칙",
            "page": 1,
            "order": 1,
            "level": 1,
            "confidence": 0.98,
        },
        {
            "block_id": "BLK-2",
            "kind": "paragraph",
            "text": "본문 문단입니다.",
            "page": 1,
            "order": 2,
            "level": 1,
            "confidence": 0.95,
        },
        {
            "block_id": "BLK-3",
            "kind": "table",
            "text": "[표 1] 예산 배분",
            "page": 2,
            "order": 3,
            "level": 1,
            "confidence": 0.7,
        },
    ]


def test_chunks_to_blocks_maps_every_chunk_with_normalized_kind_and_label():
    blocks = _chunks_to_blocks(_sample_chunks())

    assert [b["block_id"] for b in blocks] == ["BLK-1", "BLK-2", "BLK-3"]
    assert blocks[0]["kind"] == "heading"
    assert blocks[0]["label"] == "Heading"
    assert blocks[2]["kind"] == "table"


def test_chunks_to_tables_filters_only_table_kind():
    tables = _chunks_to_tables(_sample_chunks())

    assert len(tables) == 1
    assert tables[0]["block_id"] == "BLK-3"
    assert tables[0]["caption"] == "[표 1] 예산 배분"


def test_chunks_to_heading_tree_filters_only_heading_kind():
    headings = _chunks_to_heading_tree(_sample_chunks())

    assert len(headings) == 1
    assert headings[0]["block_id"] == "BLK-1"
    assert headings[0]["level"] == 1
    assert headings[0]["status"] == "확정"


def test_chunks_to_markdown_lines_splits_text_and_appends_blank_separator():
    lines = _chunks_to_markdown_lines([_sample_chunks()[1]])

    texts = [line["text"] for line in lines]
    assert texts == ["본문 문단입니다.", ""]
    assert lines[0]["kind"] == "body"
    assert lines[1]["kind"] == "blank"


def test_chunks_to_json_lines_produces_valid_pretty_printed_json():
    import json

    lines = _chunks_to_json_lines(_sample_chunks())
    rebuilt = "\n".join(line["text"] for line in lines)

    assert json.loads(rebuilt) == _sample_chunks()


def test_block_to_inspector_fields_maps_five_labeled_values():
    block = _chunks_to_blocks(_sample_chunks())[0]

    fields = _block_to_inspector_fields(block)

    by_label = {f["label"]: f["value"] for f in fields}
    assert by_label["Block ID"] == "BLK-1"
    assert by_label["Kind"] == "heading"
    assert by_label["Page"] == "1"
