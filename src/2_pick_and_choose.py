import re
import sys
from sys import argv
from typing import List, Tuple
from config import *
import logging
from matplotlib import pyplot
import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QTextEdit,
    QLabel,
    QGridLayout,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

matplotlib.use("qt5agg")


def get_score(text: str, pattern: re.Pattern) -> float:
    """
    Compute the score based on the pattern match count per 1000 words.

    Args:
        text (str): The text to analyze.
        pattern (re.Pattern): The regex pattern to match.

    Returns:
        float: The score, or 0 if the word count is below the threshold.
    """
    match_count = len(pattern.findall(text))
    word_count = len(text.split())
    if word_count < MATCH_WORD_COUND_THRESHOLD:
        return 0

    return (match_count * 1000) / word_count


def get_file(filename: str) -> str:
    """
    Read and return the content of a file.

    Args:
        filename (str): The path to the file to be read.

    Returns:
        str: The content of the file.
    """
    with open(filename) as f:
        return f.read()


PRIMARY_PATTERN = r"\sthe\s"  # Replace with your actual pattern
SECONDARY_PATTERN = r"\sanother\s"  # Replace with your actual pattern

primary_pattern = re.compile(PRIMARY_PATTERN, re.IGNORECASE)
secondary_pattern = re.compile(SECONDARY_PATTERN, re.IGNORECASE)


class MatplotlibCanvas(FigureCanvas):
    """
    A custom canvas for displaying matplotlib figures in a PyQt5 application.
    """

    def __init__(self, first_section: str, parent: QWidget = None):
        """
        Initialize the MatplotlibCanvas.

        Args:
            first_section (str): The initial text section to plot.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        self.fig: Figure
        self.ax: pyplot.Axes
        self.fig, self.ax = self.get_paragraph_scores_figure(first_section)
        super().__init__(self.fig)
        self.setParent(parent)
        self.plot()

        self.setMinimumSize(550, 400)

    def plot(self, section_text: str = None) -> None:
        """
        Plot or update the graph with new section text.

        Args:
            section_text (str, optional): The new section text to plot. If None, just redraws the existing plot.
        """
        if section_text is not None:
            self.ax.clear()
            paragraphs = section_text.splitlines()
            paragraph_scores = [
                get_score(paragraph, primary_pattern) for paragraph in paragraphs
            ]
            secondary_scores = [
                get_score(paragraph, secondary_pattern) for paragraph in paragraphs
            ]

            paragraph_range = list(range(0, len(paragraphs)))
            self.ax.plot(paragraph_range, paragraph_scores, label="primaries")
            self.ax.plot(paragraph_range, secondary_scores, label="secondaries")
            self.ax.set_xlabel("Paragraph number")
            self.ax.set_ylabel("Pattern matches per 1000 words")
            self.ax.legend(loc="best")

        self.draw()

    @staticmethod
    def get_paragraph_scores_figure(section_text: str) -> Tuple[Figure, pyplot.Axes]:
        """
        Create a figure with plots of primary and secondary scores for each paragraph.

        Args:
            section_text (str): The text section to analyze.

        Returns:
            Tuple[Figure, pyplot.Axes]: The created figure and its axes.
        """
        paragraphs = section_text.splitlines()
        paragraph_scores = []
        secondary_scores = []
        for paragraph in paragraphs:
            paragraph_scores.append(get_score(paragraph, primary_pattern))
            secondary_scores.append(get_score(paragraph, secondary_pattern))

        paragraph_range = list(range(0, len(paragraphs)))
        fig, ax = pyplot.subplots()
        ax.plot(paragraph_range, paragraph_scores, label="primaries")
        ax.plot(paragraph_range, secondary_scores, label="secondaries")
        ax.set_xlabel("Paragraph number")
        ax.set_ylabel("Pattern matches per 1000 words")
        ax.legend(loc="best")

        return fig, ax


class MainWindow(QMainWindow):
    """
    The main application window for the Pick and Choose tool.
    """

    def __init__(
        self,
        sections: List[str],
        current_full_text: str,
        book_original_primary_score: float,
        book_original_secondary_score: float,
        output_filename: str,
    ):
        """
        Initialize the MainWindow.

        Args:
            sections (List[str]): List of text sections to process.
            current_full_text (str): The current full text of the book.
            book_original_primary_score (float): The original primary score of the book.
            book_original_secondary_score (float): The original secondary score of the book.
            output_filename (str): The name of the file to write the output to.
        """
        super().__init__()
        self.sections: List[str] = sections
        self.current_full_text: str = current_full_text
        self.section_index: int = 0
        self.output_filename = output_filename

        self.setWindowTitle("Pick and Choose")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()

        header_label = QLabel("Section")
        header_label.setStyleSheet("font-size: 16px")

        self.primary_label = QLabel("Primary:")
        self.primary_label.setStyleSheet("font-size: 14px;")

        self.secondary_label = QLabel("Secondary:")
        self.secondary_label.setStyleSheet("font-size: 14px;")

        self.book_header_label = QLabel("Book")
        self.book_header_label.setStyleSheet("font-size: 16px")

        self.book_primary_label = QLabel("Primary:")
        self.book_primary_label.setStyleSheet("font-size: 14px;")

        self.book_secondary_label = QLabel("Secondary:")
        self.book_secondary_label.setStyleSheet("font-size: 14px;")

        book_primary_score = self.get_book_primary_score()
        self.book_primary_label.setText(
            f"Primary: {book_primary_score:.2f} ({(book_primary_score - book_original_primary_score):.2f})"
        )
        book_secondary_score = self.get_book_secondary_score()
        self.book_secondary_label.setText(
            f"Secondary: {book_secondary_score:.2f} ({(book_secondary_score - book_original_secondary_score):.2f})"
        )
        section_primary_score = self.get_section_primary_score()
        self.primary_label.setText(f"Primary: {section_primary_score:.2f}")
        section_secondary_score = self.get_section_secondary_score()
        self.secondary_label.setText(f"Secondary: {section_secondary_score:.2f}")

        label_layout = QVBoxLayout()
        label_layout.addWidget(header_label)
        label_layout.addWidget(self.primary_label)
        label_layout.addWidget(self.secondary_label)
        label_layout.addWidget(self.book_header_label)
        label_layout.addWidget(self.book_primary_label)
        label_layout.addWidget(self.book_secondary_label)

        label_container = QWidget()
        label_container.setLayout(label_layout)

        keep_button = QPushButton("Keep")
        trash_button = QPushButton("Trash")

        self.text_area = QTextEdit()
        self.text_area.setPlainText(self.get_section_with_tabs())
        self.text_area.setStyleSheet("font-size: 16px;")
        self.text_area.setMinimumSize(800, 500)
        self.text_area.setTabStopWidth(30)

        layout.addWidget(keep_button, 0, 1, alignment=Qt.AlignTop)
        layout.addWidget(trash_button, 1, 1, alignment=Qt.AlignTop)
        layout.addWidget(label_container, 2, 1, alignment=Qt.AlignBottom)
        layout.addWidget(self.text_area, 0, 0, 4, 1)

        self.canvas = MatplotlibCanvas(self.sections[self.section_index], self)
        layout.addWidget(self.canvas, 3, 1)

        central_widget.setLayout(layout)

        keep_button.clicked.connect(self.on_keep_button_clicked)
        trash_button.clicked.connect(self.on_trash_button_clicked)

    def on_keep_button_clicked(self) -> None:
        """Handle the 'Keep' button click event."""
        logger.info("Keep button clicked")
        logger.info(f"Section index: {self.section_index}")
        logger.info(f"Sections length: {len(self.sections)}")
        self.sections[self.section_index] = self.text_area.toPlainText()
        self.handle_button_click()

    def on_trash_button_clicked(self) -> None:
        """Handle the 'Trash' button click event."""
        logger.info("Trash button clicked")
        logger.info(f"Section index: {self.section_index}")
        logger.info(f"Sections length: {len(self.sections)}")
        self.sections[self.section_index] = "***"
        self.handle_button_click()

    def handle_button_click(self) -> None:
        """
        Common logic for handling button clicks (Keep or Trash).
        Updates scores, moves to the next section, and handles end-of-sections case.
        """
        logger.info("Handling button click")
        self.section_index += 1
        logger.info(f"Section index: {self.section_index}")
        self.update_temp_full_text()

        if self.section_index > len(self.sections) - 1:
            logger.info(f"End of sections; writing out to file: {self.output_filename}")
            logger.info(f"section_index: [{self.section_index}]")
            logger.info(f"len(sections - 1): [{len(self.sections) - 1}]")
            # Write file out
            with open(self.output_filename, "w") as f:
                f.write(self.current_full_text)
            f.close()
            QApplication.quit()
            exit(0)

        book_primary_score = self.get_book_primary_score()
        self.book_primary_label.setText(
            f"Primary: {book_primary_score:.2f} ({(book_primary_score - book_original_primary_score):.2f})"
        )
        book_secondary_score = self.get_book_secondary_score()
        self.book_secondary_label.setText(
            f"Secondary: {book_secondary_score:.2f} ({(book_secondary_score - book_original_secondary_score):.2f})"
        )
        section_primary_score = self.get_section_primary_score()
        self.primary_label.setText(f"Primary: {section_primary_score:.2f}")
        section_secondary_score = self.get_section_secondary_score()
        self.secondary_label.setText(f"Secondary: {section_secondary_score:.2f}")

        self.canvas.plot(self.sections[self.section_index])
        self.text_area.setText(self.get_section_with_tabs())

    def get_section_with_tabs(self) -> str:
        """
        Format the current section text with tabs for better readability.

        Returns:
            str: The formatted section text.
        """
        paragraphs = self.sections[self.section_index].splitlines()
        section_with_tabs = "\n\n".join(f"\t{paragraph}" for paragraph in paragraphs)
        return f"\t{section_with_tabs.strip()}"

    def update_temp_full_text(self) -> None:
        """Update the current full text based on kept sections."""
        self.current_full_text = ""
        for section in self.sections:
            if len(section.split()) > 1:
                self.current_full_text += (
                    section.strip()
                    .replace("*", "")
                    .replace("\t", "")
                    .replace("\n\n", "\n")
                    + "\n***\n"
                )

    def get_book_primary_score(self) -> float:
        """
        Calculate the primary score for the entire book.

        Returns:
            float: The primary score.
        """
        return get_score(self.current_full_text, primary_pattern)

    def get_book_secondary_score(self) -> float:
        """
        Calculate the secondary score for the entire book.

        Returns:
            float: The secondary score.
        """
        return get_score(self.current_full_text, secondary_pattern)

    def get_section_primary_score(self) -> float:
        """
        Calculate the primary score for the current section.

        Returns:
            float: The primary score.
        """
        return get_score(self.sections[self.section_index], primary_pattern)

    def get_section_secondary_score(self) -> float:
        """
        Calculate the secondary score for the current section.

        Returns:
            float: The secondary score.
        """
        return get_score(self.sections[self.section_index], secondary_pattern)

    def closeEvent(self, event) -> None:
        """
        Handle the window close event.
        Writes the current full text to a file before closing.

        Args:
            event: The close event.
        """
        logger.info(f"Closing the application, writing to: {self.output_filename}")
        # Write file out
        with open(self.output_filename, "w") as f:
            f.write(self.current_full_text)
        QApplication.quit()
        event.accept()


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python 2_pick_and_choose.py <input_filename> <output_filename>")
        sys.exit(1)

    input_filename: str = argv[1]
    output_filename: str = argv[2]
    file_text: str = get_file(input_filename)
    sections: List[str] = file_text.split("***")

    current_full_text: str = file_text

    book_original_primary_score: float = get_score(file_text, primary_pattern)
    book_original_secondary_score: float = get_score(file_text, secondary_pattern)

    app = QApplication(sys.argv)
    window = MainWindow(
        sections,
        current_full_text,
        book_original_primary_score,
        book_original_secondary_score,
        output_filename,
    )
    window.show()
    sys.exit(app.exec_())