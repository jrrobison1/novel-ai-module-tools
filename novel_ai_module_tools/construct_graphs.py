import sys
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from matplotlib import pyplot


def get_working_directory() -> Path:
    """
    Get the working directory from command line arguments.

    Returns:
        Path: The working directory path.

    Raises:
        SystemExit: If no directory name is provided as a command line argument.
    """
    try:
        return Path(sys.argv[1])
    except IndexError:
        print("Please pass directory name")
        sys.exit(1)


def get_filenames(working_directory: Path) -> List[Path]:
    """
    Get a list of text file paths from the 'names_replaced/stitched' subdirectory.

    Args:
        working_directory (Path): The base working directory.

    Returns:
        List[Path]: A list of Path objects for text files in the specified directory.
    """
    stitched_directory = working_directory / "names_replaced" / "stitched"
    return [
        f
        for f in stitched_directory.iterdir()
        if f.is_file() and f.suffix == ".txt" and not f.name.startswith(".")
    ]


def gather_file_data(
    filenames: List[Path],
) -> Tuple[Dict[str, int], Dict[str, int], int]:
    """
    Gather data about books and authors from the given files.

    Args:
        filenames (List[Path]): A list of file paths to process.

    Returns:
        Tuple[Dict[str, int], Dict[str, int], int]: A tuple containing:
            - A dictionary of book names and their sizes.
            - A dictionary of author names and their total file sizes.
            - The total size of all files.
    """
    books: Dict[str, int] = {}
    authors: Dict[str, int] = {}
    total_file_size: int = 0

    for filename in filenames:
        parts = filename.stem.split("_")
        if len(parts) >= 3:
            author = parts[1].replace("-", " ")
            book = parts[2].replace("-", " ")
        else:
            # Handle cases where the filename doesn't match the expected format
            author = filename.stem.split("_")[0]  # Use the first part as author
            book = "_".join(filename.stem.split("_")[1:])  # Use the rest as book title

        file_size = filename.stat().st_size

        authors[author] = authors.get(author, 0) + file_size
        books[book] = books.get(book, 0) + file_size
        total_file_size += file_size

    return books, authors, total_file_size


def prepare_graph_data(
    data_dict: Dict[str, int], total_file_size: int
) -> Tuple[List[str], List[int]]:
    """
    Prepare data for graph creation by calculating percentages.

    Args:
        data_dict (Dict[str, int]): A dictionary of names and their sizes.
        total_file_size (int): The total size of all files.

    Returns:
        Tuple[List[str], List[int]]: A tuple containing:
            - A list of labels with names and percentages.
            - A list of corresponding sizes.
    """
    labels: List[str] = []
    sizes: List[int] = []
    for name, size in data_dict.items():
        percentage = (size / total_file_size) * 100
        labels.append(f"{name} ({percentage:.1f}%)")
        sizes.append(size)
    return labels, sizes


def create_pie_chart(
    sizes: List[int], labels: List[str], title: str, filename: str
) -> None:
    """
    Create and save a pie chart.

    Args:
        sizes (List[int]): A list of sizes for each slice of the pie.
        labels (List[str]): A list of labels for each slice of the pie.
        title (str): The title of the pie chart.
        filename (str): The filename to save the chart as.
    """
    fig, ax = pyplot.subplots()
    ax.pie(sizes, labels=labels)
    ax.set_title(title, fontweight="bold")
    fig.savefig(filename, bbox_inches="tight")
    pyplot.close(fig)


def main() -> None:
    """
    Main function to orchestrate the graph creation process.
    """
    working_directory = get_working_directory()
    filenames = get_filenames(working_directory)
    books, authors, total_file_size = gather_file_data(filenames)

    author_labels, author_sizes = prepare_graph_data(authors, total_file_size)
    create_pie_chart(author_sizes, author_labels, "Author Influences", "authors.png")

    book_labels, book_sizes = prepare_graph_data(books, total_file_size)
    create_pie_chart(book_sizes, book_labels, "Book Influences", "books.png")


if __name__ == "__main__":
    main()
