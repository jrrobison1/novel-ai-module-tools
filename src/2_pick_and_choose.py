#!/usr/bin/env python3

import re
import sys
from sys import argv
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

matplotlib.use("qt5agg")


def get_score(text, pattern):
    """Compute the score based on the pattern match count per 1000 words."""
    match_count = len(pattern.findall(text))
    word_count = len(text.split())
    if word_count < MATCH_WORD_COUND_THRESHOLD:
        return 0

    return (match_count * 1000) / word_count


def get_file(filename):
    """Read file content."""
    with open(filename) as f:
        return f.read()


PRIMARY_PATTERN = r"\sthe\s"  # Replace with your actual pattern
SECONDARY_PATTERN = r"\sanother\s"  # Replace with your actual pattern

primary_pattern = re.compile(PRIMARY_PATTERN, re.IGNORECASE)
secondary_pattern = re.compile(SECONDARY_PATTERN, re.IGNORECASE)


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, first_section, parent=None):
        self.fig, self.ax = self.get_paragraph_scores_figure(first_section)
        super().__init__(self.fig)
        self.setParent(parent)
        self.plot()

        self.setMinimumSize(550, 400)

    def plot(self, section_text=None):
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
    def get_paragraph_scores_figure(section_text):
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
    def __init__(
        self,
        sections,
        current_full_text,
        book_original_primary_score,
        book_original_secondary_score,
    ):
        super().__init__()
        self.sections = sections
        self.current_full_text = current_full_text
        self.section_index = 0

        self.setWindowTitle("Match Count")
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

    def on_keep_button_clicked(self):
        self.sections[self.section_index] = self.text_area.toPlainText()
        self.handle_button_click()

    def on_trash_button_clicked(self):
        self.sections[self.section_index] = "***"
        self.handle_button_click()

    def handle_button_click(self):
        self.section_index += 1
        self.update_temp_full_text()
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

    def get_section_with_tabs(self):
        paragraphs = self.sections[self.section_index].splitlines()
        section_with_tabs = "\n\n".join(f"\t{paragraph}" for paragraph in paragraphs)
        return f"\t{section_with_tabs.strip()}"

    def update_temp_full_text(self):
        self.current_full_text = ""
        for section in sections:
            if len(section.split()) > 1:
                self.current_full_text += (
                    section.strip()
                    .replace("*", "")
                    .replace("\t", "")
                    .replace("\n\n", "\n")
                    + "\n***\n"
                )

    def get_book_primary_score(self):
        return get_score(self.current_full_text, primary_pattern)

    def get_book_secondary_score(self):
        return get_score(self.current_full_text, secondary_pattern)

    def get_section_primary_score(self):
        return get_score(self.sections[self.section_index], primary_pattern)

    def get_section_secondary_score(self):
        return get_score(self.sections[self.section_index], secondary_pattern)


if __name__ == "__main__":
    filename = argv[1]
    file_text = get_file(filename)
    sections = file_text.split("***")

    current_full_text = file_text

    book_original_primary_score = get_score(file_text, primary_pattern)
    book_original_secondary_score = get_score(file_text, secondary_pattern)

    app = QApplication(sys.argv)
    window = MainWindow(
        sections,
        current_full_text,
        book_original_primary_score,
        book_original_secondary_score,
    )
    window.show()
    sys.exit(app.exec_())
