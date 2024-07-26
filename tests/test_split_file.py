import pytest
from novel_ai_module_tools.split_file import get_star_index, split_file
import tempfile
import os


def test_get_star_index():
    # Test with *** in the second half
    assert get_star_index("Hello *** World") == -1
    assert get_star_index("Hello World***Test") == 11

    # Test with *** in the first half (should return -1)
    assert get_star_index("***Hello World") == -1

    # Test with no ***
    assert get_star_index("Hello World") == -1


def test_split_file():
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write("First half content Longer\n***\nSecond half content")
        temp_file_name = temp_file.name

    try:
        # Test with a file containing ***
        result = split_file(temp_file_name)
        assert result["first_half"] == "First half content Longer"
        assert result["second_half"] == "Second half content"
        assert result["no_stars"] == False
        assert (
            result["full_text"] == "First half content Longer\n***\nSecond half content"
        )

        # Test with a file not containing ***
        with open(temp_file_name, "w") as f:
            f.write("Content without stars")

        result = split_file(temp_file_name)
        assert result["full_text"] == "Content without stars"
        assert result["no_stars"] == True
        assert "first_half" not in result
        assert "second_half" not in result

        # Test with a non-existent file
        result = split_file("non_existent_file.txt")
        assert "ERROR" in result

    finally:
        # Clean up the temporary file
        os.unlink(temp_file_name)
