import pytest
import tempfile
import os
import time


def test_ujson_performance():
    from toolbox_iop.json_tools import load_json, save_normal_json

    test_data = [{"id": i, "name": f"item_{i}", "value": i * 2.5} for i in range(1000)]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for item in test_data:
            f.write(f"{item}\n")
        temp_file = f.name

    try:
        start_time = time.time()
        result = load_json(temp_file)
        end_time = time.time()

        assert len(result) == 1000
        assert result[0] == {"id": 0, "name": "item_0", "value": 0.0}
        assert result[999] == {"id": 999, "name": "item_999", "value": 2497.5}

        print(f"\nLoaded 1000 JSON lines in {end_time - start_time:.4f} seconds")
        print(f"Performance: {1000 / (end_time - start_time):.2f} lines/second")
    finally:
        os.unlink(temp_file)


def test_ujson_dumps_performance():
    from toolbox_iop.json_tools import json

    test_data = [{"id": i, "name": f"item_{i}", "value": i * 2.5} for i in range(1000)]

    start_time = time.time()
    result = json.dumps(test_data, ensure_ascii=False)
    end_time = time.time()

    assert isinstance(result, str)
    assert len(result) > 0

    print(f"\nSerialized 1000 JSON objects in {end_time - start_time:.4f} seconds")
    print(f"Performance: {1000 / (end_time - start_time):.2f} objects/second")


def test_ujson_loads_performance():
    from toolbox_iop.json_tools import json

    test_str = '{"id": 1, "name": "test", "value": 42.5}'

    iterations = 10000
    start_time = time.time()
    for _ in range(iterations):
        result = json.loads(test_str)
    end_time = time.time()

    assert result == {"id": 1, "name": "test", "value": 42.5}

    print(f"\nParsed {iterations} JSON strings in {end_time - start_time:.4f} seconds")
    print(f"Performance: {iterations / (end_time - start_time):.2f} parses/second")


def test_ujson_unicode_performance():
    from toolbox_iop.json_tools import load_json

    test_data = [{"id": i, "name": f"测试_{i}", "emoji": "🚀"} for i in range(500)]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for item in test_data:
            f.write(f"{item}\n")
        temp_file = f.name

    try:
        start_time = time.time()
        result = load_json(temp_file)
        end_time = time.time()

        assert len(result) == 500
        assert result[0] == {"id": 0, "name": "测试_0", "emoji": "🚀"}

        print(f"\nLoaded 500 Unicode JSON lines in {end_time - start_time:.4f} seconds")
        print(f"Performance: {500 / (end_time - start_time):.2f} lines/second")
    finally:
        os.unlink(temp_file)
