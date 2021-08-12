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
    list_of_ids = [x for x in range(1,number_of_students+1)]

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

    # Generate cohort numbers
    list_of_cohorts = [i+1 for i in range(cohort_size)
                       for x in range(number_of_cohorts)]

    # Generate dobs based on the starting year
    list_of_dobs = []
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

    # For each student, generate 1 enrollment record per year
    # starting with the starting grade (academic years are auto calculated based on dobs)
    # students drop out of program at provided rate of attrition
    # Schools are pulled from spreadsheet

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

    # Read and shuffle schools

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

    # Establish empty lists to be used as columns
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
    
    # Generates internships for HS 3rd and 4th years, and all college years at the rates provided.
    list_of_grades_for_internships = ["11", "12", "C1", "C2", "C3", "C4", "C5"]

    careers_df = pd.read_csv('data/job_titles_and_career_paths.csv', header=0)  
    careers_df["2018 SOC Direct Match Title Intern"] = careers_df["2018 SOC Direct Match Title"] + " Intern"
    list_of_career_fields = careers_df["2018 SOC Major Group"].unique().tolist()
    list_of_internships = careers_df["2018 SOC Direct Match Title Intern"].unique().tolist()
    list_of_org_ids_from_organizations = organization_records["Organization ID"].tolist()

    enrollments_eligible_for_internships = enrollment_records[enrollment_records["Grade"].isin(list_of_grades_for_internships)]

    #print(enrollments_eligible_for_internships.head())

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
        # For each enrollment record with the correct grade, generate roughly avg_number_of_applications_per_student records
        #   Note that only one record can be accepted and completed
        
        #   - Add student ID
        #   - Choose random org ID
        #   - Choose random internship name
        #   - Select career path
        #   - interviewed 
        # random_number_determining_interviewed = random.random()
        #   - accepted 
        # random_number_determining_accepted = random.random()
        #   - completed 
        # random_number_determining_completed = random.random()
        #   - Start date: should be some time in June in that year 
        #  start_date = datetime.date( year[:-4] + i - 1, 1, 1)
        #   - End date: Should be 2-12 weeks long

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
            # print(start_date_base)
            start_date = str(start_date_base + datetime.timedelta(days=random_day_interval_start))
            list_of_start_dates.append(start_date)

            random_day_interval_end = random.randrange(32,90)
            end_date_base = datetime.date( int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
            end_date = str(end_date_base + datetime.timedelta(days=random_day_interval_end))
            list_of_end_dates.append(end_date)

    [generate_internships_for_one_student_year(x, y) for x, y in zip(enrollments_eligible_for_internships['Student ID'], enrollments_eligible_for_internships['Academic Year'])]

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

    # print(enrollments_eligible_for_internships.head())


if __name__ == "__main__":
    permrecs = generate_permrecs(3, 10, 2002)
    enrollment = generate_enrollment(permrecs, 5, 0.03)
    organizations = generate_organizations()
    internships = generate_internships(enrollment, organizations, 3, 1, 0.5, 0.5, 0.5)