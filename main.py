# main.py
# Generates sample data based
import pandas as pd
import re
import datetime
import random
import csv


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
    return df
    # print(df)


def generate_enrollment(permrecs_df, starting_grade, rate_of_attrition):

    # For each student, generate 1 enrollment record per year
    # starting with the starting grade (academic years are auto calculated based on dobs)
    # students drop out of program at provided rate of attrition
    # Schools are pulled from spreadsheet

    # A simple grade to age lookup
    grade_age_lookup = {
        "pre-K": 4,
        "K": 5,
        "1": 6,
        "2": 7,
        "3": 8,
        "4": 9,
        "5": 10,
        "6": 11,
        "7": 12,
        "8": 13,
        "9": 14,
        "10": 15,
        "11": 16,
        "12": 17,
        "C1": 18,
        "C2": 19,
        "C3": 20,
        "C4": 21,
        "C5": 22,
    }

    # Exit types
    list_of_exit_types = [
        "withdrawn",
        "graduated",
    ]

    # Exit Reasons
    list_of_exit_reasons = [
        "Academic Performance",
        "Integrity",
        "Other Commitments",
        "Family Reasons",
        "Death/Illness (Student)",
        "Death/Illness (Other)",
        "Moved Away",
    ]

    # Read and filter schools from csv
    list_of_lower_schools = []
    with open('data/lower_schools.csv') as f:
        lines = csv.reader(f, delimiter=',', quotechar='"')
        for line in lines:
            if line[0] == "Seattle School District No. 1":
                list_of_lower_schools.append(("Seattle", line[1]))
            if line[0] == "Highline School District":
                list_of_lower_schools.append(("Highline", line[1]))
            if line[0] == "Renton School District":
                list_of_lower_schools.append(("Renton", line[1]))
    random.shuffle(list_of_lower_schools)

    list_of_higher_ed_schools = []
    with open('data/higher_ed_schools.txt') as f:
        lines = f.readlines()
        list_of_higher_ed_schools = [ line[:len(line)-1] for line in lines]
    random.shuffle(list_of_higher_ed_schools)

    

if __name__ == "__main__":
    permrecs = generate_permrecs(3, 10, 2002)
    enrollment = generate(enrollment(permrecs, 5, ))
