# main.py
# Generates sample data based
import pandas as pd
import re
import datetime
import random


def generate_permrecs(number_of_cohorts, cohort_size, starting_year):

    number_of_students = number_of_cohorts * cohort_size

    # Data for Generators
    list_of_ids = [x for x in range(number_of_students)]

    # Generate first names with data in text files
    list_of_first_names = []
    with open('data/first_names.txt') as f:
        lines = f.readlines()
        list_of_first_names = [
            re.match(r"^(\w*(?=,))", x, re.MULTILINE)[0] for x in lines]
    random.shuffle(list_of_first_names)
    list_of_first_names = list_of_first_names[:number_of_students]

    # Generate last names with data in text files
    list_of_last_names = []
    with open('data/last_names.txt') as f:
        lines = f.readlines()
        list_of_last_names = [
            re.search(r'([A-Z]+)', x)[0].title() for x in lines]
    random.shuffle(list_of_last_names)
    list_of_last_names = list_of_last_names[:number_of_students]

    list_of_cohorts = [i+1 for i in range(cohort_size)
                       for x in range(number_of_cohorts)]

    # Generate dobs based on the starting year
    list_of_dobs = []
    for i in range(len(list_of_ids)):
        start_date = datetime.date(starting_year, 1, 1)

        list_of_dobs.append(
            start_date + datetime.timedelta(days=random.randrange(364)))

    # Create data frame
    data = {
        "Student ID": list_of_ids,
        "First Name": list_of_first_names,
        "Last Name": list_of_last_names,
        "Cohort": list_of_cohorts,
        "DOB": list_of_dobs,
    }
    df = pd.DataFrame(data)

    # Export
    df.to_csv('permrecs.csv', index=False)
    # print(df)


if __name__ == "__main__":
    generate_permrecs(3, 10, 2002)
