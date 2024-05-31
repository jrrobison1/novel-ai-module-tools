# Find first occurence of the chapter marker "***" substring
# which occurs after the midway point of the input string
import os


def getStarIndex(input_text):
    print("String length: " + str(len(input_text)))
    midway_index = int(len(input_text) / 2)
    print("Midway index: " + str(midway_index))

    # Get index of first occurence of *** in second half:
    star_index = input_text.find("***", midway_index)
    print("Star index: " + str(star_index))

    return star_index


def splitFile(file_name):
    try:
        with open(file_name, "r") as input_file:
            input_text = input_file.read()
        input_file.close()

        # Get index of first occurence of *** in second half:
        star_index = getStarIndex(input_text)

        if star_index <= 0:
            return {"full_text": input_text, "no_stars": True}

        first_half = input_text[: star_index - 1]
        second_half = input_text[star_index + 1 :]

        ret_data = {
            "first_half": first_half,
            "second_half": second_half,
            "no_stars": False,
            "full_text": input_text,
        }

        return ret_data
    except:
        print("ERROR: " + file_name)
        return {"ERRROR": "ERROR"}
