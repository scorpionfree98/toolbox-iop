import tempfile
import os

from toolbox_iop.json_tools import (
    load_json,
    save_normal_json,
    save_json_file,
    load_json_line,
    load_json_file,
    safety_json_loader,
)


def test_load_json_with_jsonl():
    test_data = [
        {"id": 1, "name": "item1"},
        {"id": 2, "name": "item2"},
        {"id": 3, "name": "item3"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for item in test_data:
            f.write(f"{item}\n")
        temp_file = f.name

    try:
        result = load_json(temp_file)
        assert len(result) == 3
        assert result[0] == {"id": 1, "name": "item1"}
        assert result[1] == {"id": 2, "name": "item2"}
        assert result[2] == {"id": 3, "name": "item3"}
    finally:
        os.unlink(temp_file)


def test_load_json_with_process_func():
    test_data = [{"id": i} for i in range(3)]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for item in test_data:
            f.write(f"{item}\n")
        temp_file = f.name

    try:
        result = load_json(temp_file, process_func=lambda x: {"id": x["id"] * 2})
        assert len(result) == 3
        assert result[0] == {"id": 0}
        assert result[1] == {"id": 2}
        assert result[2] == {"id": 4}
    finally:
        os.unlink(temp_file)


def test_save_normal_json():
    test_data = [
        {"id": 1, "name": "item1"},
        {"id": 2, "name": "item2"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        temp_file = f.name

    try:
        save_normal_json(test_data, temp_file)

        with open(temp_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 2
        loaded = load_json(temp_file)
        assert loaded == test_data
    finally:
        os.unlink(temp_file)


def test_save_json_file():
    test_data = {"id": 1, "name": "item1", "nested": {"key": "value"}}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_file = f.name

    try:
        save_json_file(test_data, temp_file)

        loaded = load_json_file(temp_file)
        assert loaded == test_data
    finally:
        os.unlink(temp_file)


def test_load_json_line():
    test_str = '{"id": 1, "name": "item1"}'
    result = load_json_line(test_str)
    assert result == {"id": 1, "name": "item1"}


def test_load_json_line_with_repair():
    test_str = "{'id': 1, 'name': 'item1'}"
    result = load_json_line(test_str, repair=True)
    assert result == {"id": 1, "name": "item1"}


def test_load_json_line_without_repair():
    test_str = '{"id": 1, "name": "item1"}'
    result = load_json_line(test_str, repair=False)
    assert result == {"id": 1, "name": "item1"}


def test_load_json_file():
    test_data = {"id": 1, "name": "item1", "list": [1, 2, 3]}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(str(test_data))
        temp_file = f.name

    try:
        result = load_json_file(temp_file)
        assert result == test_data
    finally:
        os.unlink(temp_file)


def test_safety_json_loader():
    test_str = '{"id": 1, "name": "item1"}'
    result = safety_json_loader(test_str)
    assert result == {"id": 1, "name": "item1"}


def test_safety_json_loader_with_index():
    test_str = '{"id": 1, "name": "item1"}'
    result = safety_json_loader(test_str, index=5)
    assert result == {"id": 1, "name": "item1"}


def test_safety_json_loader_with_invalid_json():
    test_str = "invalid json"
    result = safety_json_loader(test_str, index=10)
    assert result is None


def test_load_json_with_empty_lines():
    test_data = [
        {"id": 1, "name": "item1"},
        "",
        {"id": 2, "name": "item2"},
        "   ",
        {"id": 3, "name": "item3"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for item in test_data:
            f.write(f"{item}\n")
        temp_file = f.name

    try:
        result = load_json(temp_file)
        assert len(result) == 3
        assert result[0] == {"id": 1, "name": "item1"}
        assert result[1] == {"id": 2, "name": "item2"}
        assert result[2] == {"id": 3, "name": "item3"}
    finally:
        os.unlink(temp_file)


def test_load_json_with_unicode():
    test_data = [
        {"id": 1, "name": "测试"},
        {"id": 2, "name": "🚀"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for item in test_data:
            f.write(f"{item}\n")
        temp_file = f.name

    try:
        result = load_json(temp_file)
        assert len(result) == 2
        assert result[0] == {"id": 1, "name": "测试"}
        assert result[1] == {"id": 2, "name": "🚀"}
    finally:
        os.unlink(temp_file)
