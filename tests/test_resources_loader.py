import pytest
from pathlib import Path
from collections import OrderedDict
from novel_ai_module_tools.resources_loader import (
    load_names,
    load_name_replacements,
    load_name_recognizers,
)


@pytest.fixture
def mock_names_directory(tmp_path):
    names_dir = tmp_path / "names"
    names_dir.mkdir()

    # Create mock files
    (names_dir / "first_names.txt").write_text("Alice\nBob\nCharlie")
    (names_dir / "last_names.txt").write_text("Smith\nJohnson\nWilliams")

    return names_dir


def test_load_names(mock_names_directory):
    result = load_names(mock_names_directory)

    assert isinstance(result, OrderedDict)
    assert set(result.keys()) == {"first_names", "last_names"}
    assert set(result["first_names"]) == {"Alice", "Bob", "Charlie"}
    assert set(result["last_names"]) == {"Smith", "Johnson", "Williams"}
    assert len(result["first_names"]) == 3
    assert len(result["last_names"]) == 3


@pytest.mark.parametrize("loader_func", [load_name_replacements, load_name_recognizers])
def test_load_name_functions(loader_func, monkeypatch):
    mock_load_names = lambda path: OrderedDict({"mock_names": ["Name1", "Name2"]})
    monkeypatch.setattr(
        "novel_ai_module_tools.resources_loader.load_names", mock_load_names
    )

    result = loader_func()

    assert isinstance(result, OrderedDict)
    assert "mock_names" in result
    assert result["mock_names"] == ["Name1", "Name2"]


def test_load_names_empty_directory(tmp_path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    result = load_names(empty_dir)

    assert isinstance(result, OrderedDict)
    assert len(result) == 0


def test_load_names_ignore_hidden_files(mock_names_directory):
    (mock_names_directory / ".hidden_file.txt").write_text("Hidden1\nHidden2")

    result = load_names(mock_names_directory)

    assert ".hidden_file" not in result
    assert len(result) == 2  # Only the two visible files should be loaded
