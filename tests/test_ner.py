import pytest
from pathlib import Path
from spacy.tokens import Doc
from novel_ai_module_tools.ner import (
    get_unique_entities,
    get_ner_write_file,
    perform_ner,
)


# Mock spaCy Doc for testing
class MockDoc:
    class MockEnt:
        def __init__(self, text, label_):
            self.text = text
            self.label_ = label_

    def __init__(self, ents):
        self.ents = [self.MockEnt(text, label) for text, label in ents]


def test_get_unique_entities():
    mock_doc = MockDoc(
        [
            ("John Doe", "PERSON"),
            ("Jane Smith", "PERSON"),
            ("New York", "GPE"),
            ("John Doe", "PERSON"),
        ]
    )

    result = get_unique_entities(mock_doc)
    assert result == {"John", "Doe", "Jane", "Smith"}


def test_get_ner_write_file(tmp_path):
    ner_directory = tmp_path / "ner_output"
    ner_directory.mkdir()
    file_name = Path("input/test_file.txt")
    strip_prefixes = ["input/"]

    result = get_ner_write_file(ner_directory, file_name, strip_prefixes)

    assert result.name == "ner_test_file.txt"
    assert result.parent == ner_directory


@pytest.fixture
def mock_resources(tmp_path):
    resource_dir = tmp_path / "resources"
    resource_dir.mkdir()
    (resource_dir / "ignore_names.txt").write_text("ignored\n")
    return resource_dir


def test_perform_ner(tmp_path, mock_resources, monkeypatch):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    ner_dir = tmp_path / "ner_output"
    ner_dir.mkdir()

    (input_dir / "test_file.txt").write_text("John Doe and Jane Smith are people.")

    # Mock spaCy and other dependencies
    class MockNER:
        def __call__(self, text):
            return MockDoc([("John Doe", "PERSON"), ("Jane Smith", "PERSON")])

    monkeypatch.setattr(
        "novel_ai_module_tools.ner.spacy.load", lambda *args, **kwargs: MockNER()
    )
    monkeypatch.setattr(
        "novel_ai_module_tools.ner.load_name_recognizers",
        lambda: {"FirstName": ["John", "Jane"]},
    )

    perform_ner([input_dir / "test_file.txt"], ner_dir, mock_resources, ["input/"])

    output_file = ner_dir / "ner_test_file.txt"
    assert output_file.exists()
    content = output_file.read_text().splitlines()
    assert "John|PERSON|FirstName" in content
    assert "Jane|PERSON|FirstName" in content
    assert "Doe|PERSON|" in content
    assert "Smith|PERSON|" in content
