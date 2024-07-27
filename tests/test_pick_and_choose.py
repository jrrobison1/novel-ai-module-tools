import pytest
import re
from unittest.mock import Mock, mock_open, patch

# Mock matplotlib and PyQt5 before importing the module
with patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}):
    with patch("matplotlib.use") as mock_use:
        from novel_ai_module_tools.pick_and_choose import (
            get_score,
            get_file,
            MatplotlibCanvas,
            MainWindow,
            PRIMARY_PATTERN,
            SECONDARY_PATTERN,
        )

from PyQt5.QtWidgets import QApplication
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from novel_ai_module_tools.pick_and_choose import (
    get_score,
    get_file,
    MatplotlibCanvas,
    MainWindow,
    PRIMARY_PATTERN,
    SECONDARY_PATTERN,
)


# Mock QApplication to avoid creating a real Qt application
@pytest.fixture(scope="module")
def qapp():
    return Mock(spec=QApplication)


@pytest.fixture
def sample_text():
    return "This is the sample text. The quick brown fox jumps over the lazy dog. Another sentence here."


@pytest.fixture
def primary_pattern():
    return re.compile(PRIMARY_PATTERN, re.IGNORECASE)


@pytest.fixture
def secondary_pattern():
    return re.compile(SECONDARY_PATTERN, re.IGNORECASE)


def test_get_score(sample_text, primary_pattern, secondary_pattern):
    assert get_score(sample_text, primary_pattern) == pytest.approx(176.47, 0.01)
    assert get_score(sample_text, secondary_pattern) == pytest.approx(58.82, 0.01)
    assert get_score("Short text", primary_pattern) == 0  # Below threshold


def test_get_file():
    with patch("builtins.open", mock_open(read_data="Test content")) as mock_file:
        assert get_file("test.txt") == "Test content"
        mock_file.assert_called_once_with("test.txt", "r", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        with patch("builtins.open", side_effect=FileNotFoundError()):
            get_file("nonexistent.txt")

    with pytest.raises(IOError):
        with patch("builtins.open", side_effect=IOError()):
            get_file("error.txt")


@pytest.fixture
def matplotlib_canvas(qapp):
    with patch("novel_ai_module_tools.pick_and_choose.FigureCanvas"):
        return MatplotlibCanvas("Test section")


def test_matplotlib_canvas_init(matplotlib_canvas):
    assert isinstance(matplotlib_canvas.fig, Figure)
    assert isinstance(matplotlib_canvas.ax, Axes)


def test_matplotlib_canvas_plot(matplotlib_canvas):
    with patch.object(matplotlib_canvas, "draw") as mock_draw:
        matplotlib_canvas.plot("New section text")
        mock_draw.assert_called_once()


def test_matplotlib_canvas_get_paragraph_scores_figure():
    fig, ax = MatplotlibCanvas.get_paragraph_scores_figure("Test\nparagraph\ntext")
    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)


@pytest.fixture
def main_window(qapp):
    sections = ["Section 1", "Section 2"]
    current_full_text = "Section 1\n***\nSection 2"
    return MainWindow(sections, current_full_text, 1.0, 1.0, "output.txt")


def test_main_window_init(main_window):
    assert main_window.sections == ["Section 1", "Section 2"]
    assert main_window.current_full_text == "Section 1\n***\nSection 2"
    assert main_window.section_index == 0
    assert main_window.output_filename == "output.txt"


def test_main_window_get_section_with_tabs(main_window):
    assert main_window.get_section_with_tabs() == "\tSection 1"


def test_main_window_update_temp_full_text(main_window):
    main_window.update_temp_full_text()
    assert main_window.current_full_text == "Section 1\n***\nSection 2\n***\n"


def test_main_window_get_book_primary_score(main_window):
    assert isinstance(main_window.get_book_primary_score(), float)


def test_main_window_get_book_secondary_score(main_window):
    assert isinstance(main_window.get_book_secondary_score(), float)


def test_main_window_get_section_primary_score(main_window):
    assert isinstance(main_window.get_section_primary_score(), float)


def test_main_window_get_section_secondary_score(main_window):
    assert isinstance(main_window.get_section_secondary_score(), float)


def test_main_window_on_keep_button_clicked(main_window):
    with patch.object(main_window, "handle_button_click") as mock_handle:
        main_window.on_keep_button_clicked()
        assert main_window.sections[0] == main_window.text_area.toPlainText()
        mock_handle.assert_called_once()


def test_main_window_on_trash_button_clicked(main_window):
    with patch.object(main_window, "handle_button_click") as mock_handle:
        main_window.on_trash_button_clicked()
        assert main_window.sections[0] == "***"
        mock_handle.assert_called_once()


def test_main_window_handle_button_click(main_window):
    with patch.object(main_window, "update_temp_full_text"), patch.object(
        main_window.canvas, "plot"
    ), patch.object(main_window.text_area, "setText"):
        main_window.handle_button_click()
        assert main_window.section_index == 1


def test_main_window_close_event(main_window):
    mock_event = Mock()
    with patch("builtins.open", mock_open()) as mock_file:
        main_window.closeEvent(mock_event)
        mock_file.assert_called_once_with("output.txt", "w", encoding="utf-8")
        mock_event.accept.assert_called_once()


if __name__ == "__main__":
    pytest.main()
