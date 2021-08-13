# main.py
# Generates sample data based
import pandas as pd
import re
import datetime
import random
import csv


def generate_permrecs(number_of_cohorts, cohort_size, starting_year):

    number_of_students = number_of_cohorts * cohort_size

    # Lists of data to be generated then converted to pandas DF
    list_of_ids = []
    list_of_first_names = []
    list_of_last_names = []
    list_of_cohorts = []
    list_of_dobs = []

    # Data for Generators
    list_of_ids = [x for x in range(1,number_of_students+1)]

    # Generate first names with data in text files
    with open('data/first_names.txt') as f:
        lines = f.readlines()
        list_of_first_names = [
            re.match(r"^(\w*(?=,))", x, re.MULTILINE)[0] for x in lines]
    random.shuffle(list_of_first_names)
    list_of_first_names = list_of_first_names[:number_of_students]

    # Generate last names with data in text files
    with open('data/last_names.txt') as f:
        lines = f.readlines()
        list_of_last_names = [
            re.search(r'([A-Z]+)', x)[0].title() for x in lines]
    random.shuffle(list_of_last_names)
    list_of_last_names = list_of_last_names[:number_of_students]

    # Generate cohort numbers
    list_of_cohorts = [i+1 for i in range(cohort_size)
                       for x in range(number_of_cohorts)]

    # Generate dobs based on the starting year
    for i in list_of_cohorts:
        start_date = datetime.date(starting_year + i - 1, 1, 1)
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
    df.to_csv('output/permrecs.csv', index=False)
    return df
    # print(df)


def generate_enrollment(permrecs_df, starting_grade, rate_of_attrition):

    # Before generating data, define several lookup tables and methods 
    # for pseudorandomly choosing data options.

    # A simple grade to age lookup
    grade_age_lookup = {
        1: 6,
        2: 7,
        3: 8,
        4: 9,
        5: 10,
        6: 11,
        7: 12,
        8: 13,
        9: 14,
        10: 15,
        11: 16,
        12: 17,
        13: 18,
        14: 19,
        15: 20,
        16: 21,
        17: 22,
    }

    # A simple grade to age lookup
    grade_name_lookup = {
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "11",
        12: "12",
        13: "C1",
        14: "C2",
        15: "C3",
        16: "C4",
        17: "C5",
    }

    # Exit types
    list_of_exit_type_options = [
        "withdrawn",
        "graduated",
    ]

    # Exit Reasons
    list_of_exit_reason_options = [
        "Academic Performance",
        "Integrity",
        "Other Commitments",
        "Family Reasons",
        "Death/Illness (Student)",
        "Death/Illness (Other)",
        "Moved Away",
    ]

    # Lists of data used for randomly selecting schools
    list_of_elementary_school_options = []
    list_of_middle_school_options = []
    list_of_high_school_options = []

    with open('data/lower_schools.csv') as f:
        lines = csv.reader(f, delimiter=',', quotechar='"')
        for line in lines:
            if line[0] == "Seattle School District No. 1":
                if line[1].find("Elementary") > 0:
                    list_of_elementary_school_options.append(("Seattle", line[1]))
                elif line[1].find("Middle") > 0:
                    list_of_middle_school_options.append(("Seattle", line[1]))
                elif line[1].find("High") > 0:
                    list_of_high_school_options.append(("Seattle", line[1]))
            elif line[0] == "Highline School District":
                if line[1].find("Elementary") > 0:
                    list_of_elementary_school_options.append(("Highline", line[1]))
                elif line[1].find("Middle") > 0:
                    list_of_middle_school_options.append(("Highline", line[1]))
                elif line[1].find("High") > 0:
                    list_of_high_school_options.append(("Highline", line[1]))
            elif line[0] == "Renton School District":                
                if line[1].find("Elementary") > 0:
                    list_of_elementary_school_options.append(("Renton", line[1]))
                elif line[1].find("Middle") > 0:
                    list_of_middle_school_options.append(("Renton", line[1]))
                elif line[1].find("High") > 0:
                    list_of_high_school_options.append(("Renton", line[1]))
   
    list_of_higher_ed_school_options = []
    with open('data/higher_ed_schools.txt') as f:
        lines = f.readlines()
        list_of_higher_ed_school_options = [ line[:len(line)-1] for line in lines]
    random.shuffle(list_of_higher_ed_school_options)
    
    def get_random_school(grade):
        if grade >= 1 and grade <= 5:
            return list_of_elementary_school_options[random.randrange(0,len(list_of_elementary_school_options))]
        elif grade > 5 and grade <= 8:
            return list_of_middle_school_options[random.randrange(0,len(list_of_middle_school_options))]
        elif grade > 8 and grade <= 12:
            return list_of_high_school_options[random.randrange(0,len(list_of_high_school_options))]
        elif grade > 12 and grade <= 17:
            return ("University", list_of_higher_ed_school_options[random.randrange(0,len(list_of_higher_ed_school_options))])
        else:
            return ("grade out of bounds error", "grade should be between 1 and 17")

    # For each student, make enrollment records
    #   Determine year based on grade by adding to student's DOB the looked up age from grade 
    #   All students get at least one enrollment record with a randomly chosen school
    #   After each enrollment record, there is a change the student does not continue
    #   If the student does continue, make another record

    # Lists of data to be generated then converted to pandas DF
    list_of_enrollment_ids = []
    list_of_student_ids = []
    list_of_academic_years = []
    list_of_grades = []
    list_of_school_names = []
    list_of_school_districts = []
    list_of_exited_this_years = []
    list_of_exit_reasons = []
    list_of_exit_types = []

    with open('output/permrecs.csv') as f:
        csvreader_of_students = csv.reader(f, delimiter=',', quotechar='"')
        next(csvreader_of_students) # skip header
        for row_in_csvreader_of_students in csvreader_of_students:
            grade = starting_grade
            random_number_determining_attrition = 1
            while grade <= 17 and random_number_determining_attrition > rate_of_attrition:
        
                # Set Student ID
                list_of_student_ids.append(row_in_csvreader_of_students[0])

                # Set Academic Year
                academic_year_start = int(int(row_in_csvreader_of_students[4][:4]) + int(grade_age_lookup[grade]))
                academic_year_end = academic_year_start + 1
                list_of_academic_years.append(str(academic_year_start) + "-" + str(academic_year_end))

                # Set Grade
                list_of_grades.append(grade_name_lookup[grade])
            
                # Set School Name and District
                # Schools should be the same in the following ranges (inclusive) for simplicity:
                #   1-5: Elementary
                #   6-8: Middle
                #   9-12: High
                #   13-17: University

                list_of_grades_for_reselecting_schools = [starting_grade, 1, 6, 9, 13]

                if grade in list_of_grades_for_reselecting_schools:
                    random_district_school = get_random_school(grade)
                    list_of_school_districts.append(random_district_school[0])
                    list_of_school_names.append(random_district_school[1])

                else:
                    # If not at grade boundary, use same school as previous loop
                    list_of_school_districts.append(list_of_school_districts[len(list_of_school_districts)-1])
                    list_of_school_names.append(list_of_school_names[len(list_of_school_names)-1])

                # Calculate if exit
                # Exits is either graduation in grade 17 or randomly attrition
                random_number_determining_attrition = random.random()
                if grade == 17: 
                    list_of_exited_this_years.append(True)
                    list_of_exit_types.append("graduated")
                    list_of_exit_reasons.append("")
                elif random_number_determining_attrition <= rate_of_attrition:
                    list_of_exited_this_years.append(True)
                    list_of_exit_types.append("withdrawn")
                    list_of_exit_reasons.append(list_of_exit_reason_options[random.randint(0,len(list_of_exit_reason_options)-1)])
                else:
                    list_of_exited_this_years.append(False)
                    list_of_exit_types.append("")
                    list_of_exit_reasons.append("")
                
                # Prep for next grade
                grade += 1

    list_of_enrollment_ids = [x+1 for x in range(len(list_of_student_ids))]

    # Create data frame
    data = {
        "Enrollment ID": list_of_enrollment_ids,
        "Student ID": list_of_student_ids,
        "Academic Year": list_of_academic_years,
        "Grade": list_of_grades,
        "School Name": list_of_school_names,
        "School District": list_of_school_districts,
        "Exited This Year?": list_of_exited_this_years,
        "Exit Reason": list_of_exit_reasons,
        "Exit Type": list_of_exit_types,
    }
    df = pd.DataFrame(data)

    df.to_csv('output/enrollment.csv', index=False)
    return df


def generate_organizations():

    list_of_organization_ids = []
    list_of_organizations = []

    with open('data/organization_names.txt') as f:
        lines = f.readlines()
        list_of_organizations = [ line[:len(line)-1] for line in lines]
    random.shuffle(list_of_organizations)

    list_of_organization_ids = [x+1 for x in range(len(list_of_organizations))]
    
    # Create data frame
    data = {
        "Organization ID": list_of_organization_ids,
        "Organization Name": list_of_organizations,
    }
    df = pd.DataFrame(data)
    df.to_csv('output/organizations.csv', index=False)
    return df


def generate_internships(enrollment_records, organization_records, avg_number_of_applications_per_student, apps_per_student_stdv, rate_of_interviewed, rate_of_completion, rate_of_desired_career_path):
    
    # Before generating data, define lookups and filter dfs that will be used.

    # Generates internships for HS 3rd and 4th years, and all college years at the rates provided.
    list_of_grades_for_internships = ["11", "12", "C1", "C2", "C3", "C4", "C5"]

    careers_df = pd.read_csv('data/job_titles_and_career_paths.csv', header=0)  
    careers_df["2018 SOC Direct Match Title Intern"] = careers_df["2018 SOC Direct Match Title"] + " Intern"
    list_of_career_fields = careers_df["2018 SOC Major Group"].unique().tolist()
    list_of_internships = careers_df["2018 SOC Direct Match Title Intern"].unique().tolist()
    list_of_org_ids_from_organizations = organization_records["Organization ID"].tolist()

    enrollment_records_eligible_for_internships = enrollment_records[enrollment_records["Grade"].isin(list_of_grades_for_internships)]

    # Lists of data to be generated then converted to pandas DF
    list_of_internship_ids = []
    list_of_student_ids = []
    list_of_org_ids = []
    list_of_internship_names = []
    list_of_career_paths = []
    list_of_is_desired_career_paths = []
    list_of_interviewds = []
    list_of_accepteds = []
    list_of_completeds = []
    list_of_start_dates = []
    list_of_end_dates = []

    # To avoid iterrowing over the df, function creates some number of internships given a student-year (one row in df)
    # This is preemptively optimizing, but an interesting thing to try
    def generate_internships_for_one_student_year(student_id, academic_year):

        number_of_internships = max(0, int(random.gauss(avg_number_of_applications_per_student, apps_per_student_stdv)))
        if number_of_internships != 0: 
            index_of_completed_internship = random.randrange(0, number_of_internships)
        
        has_accepted_one_internship = False

        for i in range(number_of_internships):
            list_of_student_ids.append(student_id)
            list_of_org_ids.append(list_of_org_ids_from_organizations[random.randrange(0,len(list_of_org_ids_from_organizations))])
            list_of_internship_names.append(list_of_internships[random.randrange(0,len(list_of_internships))])
            list_of_career_paths.append(list_of_career_fields[random.randrange(0,len(list_of_career_fields))])
            
            is_desired_career_path = random.random()
            if is_desired_career_path <= rate_of_desired_career_path:
                list_of_is_desired_career_paths.append(True)
            else:
                list_of_is_desired_career_paths.append(False)

            is_interviewed = random.random()
            if is_interviewed <= rate_of_interviewed:
                list_of_interviewds.append(True)
            else:
                list_of_interviewds.append(False)

            if not has_accepted_one_internship and list_of_interviewds[len(list_of_interviewds)-1]:
                has_accepted_one_internship = True
                list_of_accepteds.append(True)
            else:
                list_of_accepteds.append(False)

            is_completed = random.random()
            if list_of_accepteds[len(list_of_accepteds)-1] and is_completed <= rate_of_completion:
                list_of_completeds.append(True)
            else:
                list_of_completeds.append(False)

            random_day_interval_start = random.randrange(1,30)
            start_date_base = datetime.date( int(academic_year[:4]), 1, 1)
            start_date = str(start_date_base + datetime.timedelta(days=random_day_interval_start))
            list_of_start_dates.append(start_date)

            random_day_interval_end = random.randrange(32,90)
            end_date_base = datetime.date( int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
            end_date = str(end_date_base + datetime.timedelta(days=random_day_interval_end))
            list_of_end_dates.append(end_date)

    [generate_internships_for_one_student_year(x, y) for x, y in zip(enrollment_records_eligible_for_internships['Student ID'], enrollment_records_eligible_for_internships['Academic Year'])]

    list_of_internship_ids = [x+1 for x in range(len(list_of_student_ids))]

    data = {
        "Internship ID": list_of_internship_ids,
        "Student ID": list_of_student_ids,
        "Organization ID": list_of_org_ids,
        "Internship Name": list_of_internship_names,
        "Career Path": list_of_career_paths,
        "Is Desired Career Path": list_of_is_desired_career_paths,
        "Interviewed?": list_of_interviewds,
        "Accepted?": list_of_accepteds,
        "Completed?": list_of_completeds,
        "Start Date": list_of_start_dates,
        "End Date": list_of_end_dates,
    }
    
    df = pd.DataFrame(data)
    df.to_csv('output/internships.csv', index=False)
    return df

    # print(enrollment_records_eligible_for_internships.head())

# This method assumes we are finding and collecting data about students even after they leave the program
def generate_career_experiences(enrollment_records, organization_records):

    # Parameters for data generation:
    career_experience_tenure_average_years = 2
    career_experience_tenure_stddev_years = 2
    rate_of_desired_career_paths = 0.5
    grade_first_eligible_for_career_experience = "9"
    max_year = int(enrollment_records["Academic Year"].max()[:4])

    # Prepare lookups and sources of data

    # Prepare data - Enrollment records
    enrollment_records_of_students_first_career_eligible_year = enrollment_records[enrollment_records["Grade"] == grade_first_eligible_for_career_experience]

    # Prepare data - Organization IDs
    list_of_org_ids_from_organizations = organization_records["Organization ID"].tolist()

    # Prepare data - Career Experience Names
    careers_df = pd.read_csv('data/job_titles_and_career_paths.csv', header=0)  
    list_of_career_experience_options = careers_df["2018 SOC Direct Match Title"].unique().tolist()

    # Prepare data - Career fields
    list_of_career_fields = careers_df["2018 SOC Major Group"].unique().tolist()

    # Lists of data to be generated then converted to pandas df
    list_of_career_experience_ids = []
    list_of_student_ids = []
    list_of_org_ids = []
    list_of_career_experience_names = []
    list_of_career_paths = []
    list_of_is_desired_career_paths = []
    list_of_start_dates = []
    list_of_end_dates = []

    # Generate data

    # To avoid iterrowing over the df, this function generates a career experience given a student id and academic year
    # Method should eventually be called using only each student's first eligible enrollment record (by year)
    def generate_career_experiences_for_one_student_year(student_id, academic_year, max_year):
        
        # max year in enrollments record is assumed to be "current" year
        # Given a student id and a year, jobs are generated with some number of days as the tenure (minimum of 365)
        # until "current year" is reached or exceeded for which "present" is used as end date.
        
        # Generate data - Max end date 
        max_date = datetime.date( int(max_year), 1, 1)

        # Set minimum start date based on student's first eligible academic year
        end_date = datetime.date( int(academic_year[:4]), random.randrange(1,12), 1)

        # Generate career experiences initializing end date with minimum:
        while end_date < max_date:

            # Generate data - Student ID
            list_of_student_ids.append(student_id)

            # Generate data - Organization ID
            list_of_org_ids.append(list_of_org_ids_from_organizations[random.randrange(0,len(list_of_org_ids_from_organizations))])

            # Generate data - Career Experience Name
            career_experience_name = list_of_career_experience_options[random.randrange(0,len(list_of_career_experience_options))] # will be used again
            list_of_career_experience_names.append(career_experience_name)

            # Generate data - Career field
            # filter by direct match title, get career field
            this_career_experience_df = careers_df[careers_df["2018 SOC Direct Match Title"] == career_experience_name]
            # print()
            # print(career_experience_name)
            # print(this_career_experience_df)
            # print(this_career_experience_df.index.tolist()[0])
            career_field_of_this_experience = this_career_experience_df.at[this_career_experience_df.index.tolist()[0],"2018 SOC Major Group"]
            list_of_career_paths.append(career_field_of_this_experience)

            # Generate data - Is desired career field?
            is_desired_career_path = random.random()
            if is_desired_career_path <= rate_of_desired_career_paths:
                list_of_is_desired_career_paths.append(True)
            else:
                list_of_is_desired_career_paths.append(False)

            # Generate data - Start Date
            # New jobs should start 1-30 days after the previous one ended
            start_date_days_after_last_job = random.randrange(1,30)
            delta_for_start_date_after_previous_end_date = datetime.timedelta(days=start_date_days_after_last_job)
            start_date = end_date + delta_for_start_date_after_previous_end_date
            list_of_start_dates.append(str(start_date))

            # Generate data - End Date
            career_experience_tenure = max(1, int(random.gauss(career_experience_tenure_average_years, career_experience_tenure_stddev_years)))
            career_experience_tenure_interval_delta = datetime.timedelta(days=career_experience_tenure*365)
            end_date = end_date + career_experience_tenure_interval_delta
            list_of_end_dates.append(str(end_date))

        # After all jobs have been made, replace final end date with "present"
        list_of_end_dates[len(list_of_end_dates)-1] = "present"

    # Call data generation function for each student's first eligible enrollment record
    [ generate_career_experiences_for_one_student_year(x, y, max_year) for x,y in zip(enrollment_records_of_students_first_career_eligible_year["Student ID"], enrollment_records_of_students_first_career_eligible_year["Academic Year"])]

    # Generate data - Career experience IDs
    list_of_career_experience_ids = [x+1 for x in range(len(list_of_student_ids))]


    # Convert lists to data frame and export
    data = {
        "Career Experience ID": list_of_career_experience_ids,
        "Student ID": list_of_student_ids,
        "Organization ID": list_of_org_ids,
        "Career Experience Name": list_of_career_experience_names,
        "Career Path": list_of_career_paths,
        "Is Desired Career Path": list_of_is_desired_career_paths,
        "Start Date": list_of_start_dates,
        "End Date": list_of_end_dates,
    }

    df = pd.DataFrame(data)
    df.to_csv('output/careers.csv', index=False)
    return df


if __name__ == "__main__":
    permrecs = generate_permrecs(3, 10, 2002)
    enrollment = generate_enrollment(permrecs, 5, 0.03)
    organizations = generate_organizations()
    internships = generate_internships(enrollment, organizations, 3, 1, 0.5, 0.5, 0.5)
    careers = generate_career_experiences(enrollment, organizations)


# TO DO
# Move all parameters to beginning of methods
# Add more comments
# Move str out of variables and into the list appends
# Rename source lists as "options"
# Change career field selector for internships to match career experience generator