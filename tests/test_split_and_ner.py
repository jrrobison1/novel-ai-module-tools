import pytest
from novel_ai_module_tools.split_and_ner import (
    create_directories,
    process_single_file,
    process_files,
)
from novel_ai_module_tools.config import (
    SPLITS_FIRST_HALF_PREFIX,
    SPLITS_SECOND_HALF_PREFIX,
)


@pytest.fixture
def temp_directory(tmp_path):
    return tmp_path


def test_create_directories(temp_directory):
    names_replaced, splits, ner = create_directories(temp_directory)

    assert names_replaced.exists()
    assert splits.exists()
    assert ner.exists()

    assert names_replaced == temp_directory / "names_replaced"
    assert splits == temp_directory / "names_replaced" / "splits"
    assert ner == temp_directory / "names_replaced" / "ner"


def test_process_single_file_no_splits(temp_directory, mocker):
    splits_dir = temp_directory / "splits"
    splits_dir.mkdir()

    mock_split_file = mocker.patch("novel_ai_module_tools.split_and_ner.split_file")
    mock_split_file.return_value = {"no_stars": True, "full_text": "Test content"}

    result = process_single_file("test.txt", temp_directory, splits_dir)

    assert result == splits_dir / "nosplits_test.txt"
    assert result.read_text() == "Test content"


def test_process_single_file_with_splits(temp_directory, mocker):
    splits_dir = temp_directory / "splits"
    splits_dir.mkdir()

    mock_split_file = mocker.patch("novel_ai_module_tools.split_and_ner.split_file")
    mock_split_file.return_value = {
        "no_stars": False,
        "first_half": "First half",
        "second_half": "Second half",
    }

    mocker.patch(
        "numpy.random.choice",
        return_value=splits_dir / f"{SPLITS_FIRST_HALF_PREFIX}test.txt",
    )

    result = process_single_file("test.txt", temp_directory, splits_dir)

    assert result == splits_dir / f"{SPLITS_FIRST_HALF_PREFIX}test.txt"
    assert (
        splits_dir / f"{SPLITS_FIRST_HALF_PREFIX}test.txt"
    ).read_text() == "First half"
    assert (
        splits_dir / f"{SPLITS_SECOND_HALF_PREFIX}test.txt"
    ).read_text() == "Second half"


@pytest.mark.parametrize(
    "file_names", [["test1.txt", "test2.txt"], ["single_file.txt"], []]
)
def test_process_files(temp_directory, mocker, file_names):
    mock_create_directories = mocker.patch(
        "novel_ai_module_tools.split_and_ner.create_directories"
    )
    mock_create_directories.return_value = (
        temp_directory / "names_replaced",
        temp_directory / "names_replaced" / "splits",
        temp_directory / "names_replaced" / "ner",
    )
    mock_process_single_file = mocker.patch(
        "novel_ai_module_tools.split_and_ner.process_single_file"
    )
    mock_perform_ner = mocker.patch("novel_ai_module_tools.split_and_ner.perform_ner")

    for file_name in file_names:
        (temp_directory / file_name).touch()

    process_files(str(temp_directory))

    assert mock_process_single_file.call_count == len(file_names)
    assert mock_perform_ner.call_count == 1
