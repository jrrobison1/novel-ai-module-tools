from pathlib import Path

import pytest

from novel_ai_module_tools.construct_graphs import (
    gather_file_data,
    get_filenames,
    prepare_graph_data,
)


@pytest.fixture
def mock_working_directory(tmp_path):
    stitched_dir = tmp_path / "names_replaced" / "stitched"
    stitched_dir.mkdir(parents=True)
    (stitched_dir / "Author1_Book1.txt").write_text("Content1")
    (stitched_dir / "Author2_Book2.txt").write_text("Content2")
    (stitched_dir / ".hidden_file.txt").write_text("Hidden")
    return tmp_path


def test_get_filenames(mock_working_directory):
    filenames = get_filenames(mock_working_directory)
    assert len(filenames) == 2
    assert all(f.suffix == ".txt" for f in filenames)
    assert not any(f.name.startswith(".") for f in filenames)


def test_gather_file_data(mock_working_directory):
    filenames = get_filenames(mock_working_directory)
    books, authors, total_size = gather_file_data(filenames)

    assert len(books) == 2
    assert len(authors) == 2
    assert total_size == 16  # "Content1" and "Content2" are 8 bytes each

    assert "Book1" in books and "Book2" in books
    assert "Author1" in authors and "Author2" in authors


def test_prepare_graph_data():
    data_dict = {"Item1": 50, "Item2": 30, "Item3": 20}
    total_size = 100

    labels, sizes = prepare_graph_data(data_dict, total_size)

    assert len(labels) == 3
    assert len(sizes) == 3
    assert all(isinstance(size, int) for size in sizes)
    assert all("%" in label for label in labels)
