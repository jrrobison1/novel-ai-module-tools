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
    # file_names = ["Close_to_Shore__The_Terrifying_Shark_Attac_-_Michael_Capuzzo.txt", "MEG__Nightstalkers__5_-_Steve_Alten.txt", "Shark_Island_-_Chris_Jameson.txt", "Devil_Sharks_-_Chris_Jameson.txt", "Meg__A_Novel_of_Deep_Terror_-_Steve_Alten.txt", "The_Trench_-_Steve_Alten.txt", "Emperors_of_the_Deep__Sharks--The_Ocean's_-_William_McKeever.txt", "Megalodon_In_Paradise_-_Hunter_Shea.txt", "White_Shark_-_Benchley-Peter.txt", "Jaws__A_Novel_-_Peter_Benchley.txt", "Shark_Beach_-_Chris_Jameson.txt"]
    # for file_name in file_names:   
    try:
        with open(file_name, 'r') as input_file:
            input_text = input_file.read()
        input_file.close()

        # Get index of first occurence of *** in second half:
        star_index = getStarIndex(input_text)

        if star_index <= 0:
            return {"full_text": input_text,
                    "no_stars": True}

        first_half = input_text[:star_index - 1]
        second_half = input_text[star_index + 1:]

        ret_data = {
            "first_half": first_half,
            "second_half": second_half,
            "no_stars": False,
            "full_text": input_text
        }

        return ret_data
    except:
        print("ERROR: " + file_name)
        return {
            "ERRROR": "ERROR"
        }

            # first_half_file = open(os.path.join(write_dir, "1h_" + file_name), "w")
            # second_half_file = open(os.path.join(write_dir, "2h_" + file_name), "w")

            # first_half_file.write(first_half)
            # second_half_file.write(second_half)

            # input_file.close()
            # first_half_file.close()
            # second_half_file.close()

            # first_half_star_index = getStarIndex(first_half)
            # first_quarter = first_half[:first_half_star_index - 1]
            # second_quarter = first_half[first_half_star_index: len(first_half)]

            # second_half_star_index = getStarIndex(second_half)
            # third_quarter = second_half[:second_half_star_index - 1]
            # fourth_quarter = second_half[second_half_star_index: len(second_half)]

            # first_quarter_file = open("1_q" + file_name, "w")
            # second_quarter_file = open("2_q" + file_name, "w")
            # third_quarter_file = open("3_q" + file_name, "w")
            # fourth_quarter_file = open("4_q" + file_name, "w")



            # first_quarter_file.write(first_quarter)
            # second_quarter_file.write(second_quarter)
            # third_quarter_file.write(third_quarter)
            # fourth_quarter_file.write(fourth_quarter)