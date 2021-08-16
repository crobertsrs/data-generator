# main.py
# Generates sample data based
import pandas as pd
import re
import datetime
import random
import csv
import json



def generate_permrecs():
    # VARIABLE PARAMETERS FOR GENERATION
    
    # Variable paramters - One cohort is admitted per year, this is the total number of cohorts to accept.
    # starting_year + number of cohorts will equal the largest/most recent year a cohort was admitted.
    number_of_cohorts = 3

    # Variable paramters - Number of students in each cohort
    cohort_size = 10

    # Variable paramters - The year in which the first cohort was admitted
    starting_year = 2002

    # Variable paramters - For convenience, total number of students in the program
    number_of_students = number_of_cohorts * cohort_size


    # PREPARE LOOKUPS, SOURCES OF DATA, AND CONTAINERS

    # Prepare - Lists of data to be generated then converted to pandas DF
    list_of_ids = []
    list_of_first_names = []
    list_of_last_names = []
    list_of_cohorts = []
    list_of_dobs = []

    # Prepare - Data for Generators
    list_of_ids = [x for x in range(1,number_of_students+1)]


    # GENERATE DATA

    # Generate data - Generate first names with data in text files
    with open('data/first_names.txt') as f:
        lines = f.readlines()
        list_of_first_names = [
            re.match(r"^(\w*(?=,))", x, re.MULTILINE)[0] for x in lines]
    random.shuffle(list_of_first_names)
    list_of_first_names = list_of_first_names[:number_of_students]

    # Generate data - Generate last names with data in text files
    with open('data/last_names.txt') as f:
        lines = f.readlines()
        list_of_last_names = [
            re.search(r'([A-Z]+)', x)[0].title() for x in lines]
    random.shuffle(list_of_last_names)
    list_of_last_names = list_of_last_names[:number_of_students]

    # Generate data - Generate cohort numbers
    list_of_cohorts = [i+1 for i in range(cohort_size)
                       for x in range(number_of_cohorts)]

    # Generate data - Generate dobs based on the starting year
    for i in list_of_cohorts:
        start_date = datetime.date(starting_year + i - 1, 1, 1)
        list_of_dobs.append(
            start_date + datetime.timedelta(days=random.randrange(364)))


    # EXPORT AS DATAFRAME AND CSV

    # Export - Create data frame
    data = {
        "Student ID": list_of_ids,
        "First Name": list_of_first_names,
        "Last Name": list_of_last_names,
        "Cohort": list_of_cohorts,
        "DOB": list_of_dobs,
    }
    df = pd.DataFrame(data)

    # Export - Export CSV and return DataFrame
    df.to_csv('output/permrecs.csv', index=False)
    return df


def generate_enrollment(permrecs_df):
    # VARIABLE PARAMETERS FOR GENERATION
    
    # Variable paramters - The grade a student should be in in their first year
    starting_grade = 5

    # Variable paramters - Rate at which students should leave the program fro randomly selected reasons
    rate_of_attrition = 0.03


    # PREPARE LOOKUPS, SOURCES OF DATA, AND CONTAINERS

    # Prepare - Lists of data to be generated then converted to pandas DF
    list_of_enrollment_ids = []
    list_of_student_ids = []
    list_of_academic_years = []
    list_of_grades = []
    list_of_school_names = []
    list_of_school_districts = []
    list_of_exited_this_years = []
    list_of_exit_reasons = []
    list_of_exit_types = []

    # Prepare - Lists of options that will be randomly chosen for data
    list_of_elementary_school_options = []
    list_of_middle_school_options = []
    list_of_high_school_options = []
    list_of_higher_ed_school_options = []

    # Prepare - Grade number to age lookup
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

    # Prepare - Grade number to grade name lookup
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

    # Prepare - Exit Reasons
    list_of_exit_reason_options = [
        "Academic Performance",
        "Integrity",
        "Other Commitments",
        "Family Reasons",
        "Death/Illness (Student)",
        "Death/Illness (Other)",
        "Moved Away",
    ]

    # Prepare - Make lists of elementary, middle, and high school options
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
   
    # Prepare - Make list of higher ed school options
    with open('data/higher_ed_schools.txt') as f:
        lines = f.readlines()
        list_of_higher_ed_school_options = [ line[:len(line)-1] for line in lines]
    random.shuffle(list_of_higher_ed_school_options)
    
    # Prepare - Method for randomly getting a school based on a grade
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


    # GENERATE DATA

    # Generate data - For each student, create enrollment records starting in starting_grade up through "C5" with the same potential attrition each year
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
                academic_year_start = int(row_in_csvreader_of_students[4][:4]) + int(grade_age_lookup[grade])
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

    # Generate data - Create primary keys based on the number of records
    list_of_enrollment_ids = [x+1 for x in range(len(list_of_student_ids))]


    # EXPORT AS DATAFRAME AND CSV

    # Export - Create data frame
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

    # Export - Export CSV and return DataFrame
    df.to_csv('output/enrollment.csv', index=False)
    return df


def generate_organizations():

    # VARIABLE PARAMETERS FOR GENERATION
    shuffle_organizations = False
    
    # PREPARE LOOKUPS, SOURCES OF DATA, AND CONTAINERS

    # Prepare - Lists of data to be generated then converted to pandas DF
    list_of_organization_ids = []
    list_of_organization_names = []


    # GENERATE DATA

    # Generate Data - List of organization names
    with open('data/organization_names.txt') as f:
        lines = f.readlines()
        list_of_organization_names = [ line[:len(line)-1] for line in lines]
    if shuffle_organizations:
        random.shuffle(list_of_organization_names)

    # Generate Data - List of organization ids based on number of names
    list_of_organization_ids = [x+1 for x in range(len(list_of_organization_names))]


    # EXPORT AS DATAFRAME AND CSV

    # Export - Create data frame
    data = {
        "Organization ID": list_of_organization_ids,
        "Organization Name": list_of_organization_names,
    }
    df = pd.DataFrame(data)

    # Export - Export CSV and return DataFrame
    df.to_csv('output/organizations.csv', index=False)
    return df


def generate_internships(enrollment_records, organization_records):
    # VARIABLE PARAMETERS FOR GENERATION
    
    # Variable paramters - Average and standard deviation of number of applications a student should have each year
    avg_number_of_applications_per_student = 3
    apps_per_student_stdv = 1

    # Variable paramters - Rates at which students should interview and complete internships they applied for
    rate_of_interviewed = 0.5
    rate_of_completion = 0.5

    # Variable paramters - Rate at which an internship is a student's desired career path
    rate_of_desired_career_path = 0.5


    # PREPARE LOOKUPS, SOURCES OF DATA, AND CONTAINERS

    # Prepare - Lists of data to be generated then converted to pandas DF
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

    # Prepare - Grades during which students apply for internships
    list_of_grades_for_internships = ["11", "12", "C1", "C2", "C3", "C4", "C5"]

    # Prepare - Create possible internships and career fields using the career options data
    careers_df = pd.read_csv('data/job_titles_and_career_paths.csv', header=0)  
    careers_df["2018 SOC Direct Match Title Intern"] = careers_df["2018 SOC Direct Match Title"] + " Intern"
    list_of_career_field_options = careers_df["2018 SOC Major Group"].unique().tolist()
    list_of_internship_options = careers_df["2018 SOC Direct Match Title Intern"].unique().tolist()

    # Prepare - List of organization IDs from previously generated data
    list_of_org_id_options = organization_records["Organization ID"].tolist()

    # Prepare - Subset of enrollment records including only grades during which students apply for internships
    enrollment_records_eligible_for_internships = enrollment_records[enrollment_records["Grade"].isin(list_of_grades_for_internships)]


    # GENERATE DATA

    # Generate Data - Method that handles creation of internship records given a student and year
    # Method approach was used to avoid iterrowing over the df
    def generate_internships_for_one_student_year(student_id, academic_year):

        number_of_internships = max(0, int(random.gauss(avg_number_of_applications_per_student, apps_per_student_stdv)))
        if number_of_internships != 0: 
            index_of_completed_internship = random.randrange(0, number_of_internships)

        has_accepted_one_internship = False

        for i in range(number_of_internships):
            list_of_student_ids.append(student_id)
            list_of_org_ids.append(list_of_org_id_options[random.randrange(0,len(list_of_org_id_options))])
            list_of_internship_names.append(list_of_internship_options[random.randrange(0,len(list_of_internship_options))])
            list_of_career_paths.append(list_of_career_field_options[random.randrange(0,len(list_of_career_field_options))])
            
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
            start_date = start_date_base + datetime.timedelta(days=random_day_interval_start)
            list_of_start_dates.append(str(start_date))

            random_day_interval_end = random.randrange(32,90)
            end_date_base = datetime.date( start_date.year, start_date.month, start_date.day)
            end_date = str(end_date_base + datetime.timedelta(days=random_day_interval_end))
            list_of_end_dates.append(end_date)

    # Generate Data - Use list comprehension to call the method with student IDs and academic years
    [generate_internships_for_one_student_year(x, y) for x, y in zip(enrollment_records_eligible_for_internships['Student ID'], enrollment_records_eligible_for_internships['Academic Year'])]

    # Generate Data - Create primary keys using number of records created
    list_of_internship_ids = [x+1 for x in range(len(list_of_student_ids))]
    
    
    # EXPORT AS DATAFRAME AND CSV

    # Export - Create data frame
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

    # Export - Export CSV and return DataFrame
    df.to_csv('output/internships.csv', index=False)
    return df


def generate_career_experiences(enrollment_records, organization_records):

    # VARIABLE PARAMETERS FOR GENERATION
    
    # Variable paramters - Average and standard deviation of how long a student should stay in any one career experience
    career_experience_tenure_average_years = 2
    career_experience_tenure_stddev_years = 2

    # Variable paramters - Rate at which any particular career experience should be a student's desired career path
    rate_of_desired_career_paths = 0.5

    # Variable paramters - Grade in which students should start having career experiences
    grade_first_eligible_for_career_experience = "9"
    

    # PREPARE LOOKUPS, SOURCES OF DATA, AND CONTAINERS

    # Prepare - Lists of data to be generated then converted to pandas DF
    list_of_career_experience_ids = []
    list_of_student_ids = []
    list_of_org_ids = []
    list_of_career_experience_names = []
    list_of_career_paths = []
    list_of_is_desired_career_paths = []
    list_of_start_dates = []
    list_of_end_dates = []

    # Prepare data - Enrollment records
    enrollment_records_of_students_first_career_eligible_year = enrollment_records[enrollment_records["Grade"] == grade_first_eligible_for_career_experience]

    # Prepare - Max year is the "current" year after which we should not have info for students
    max_year = int(enrollment_records["Academic Year"].max()[:4])

    # Prepare data - Organization IDs
    list_of_org_id_options = organization_records["Organization ID"].tolist()

    # Prepare data - Career Experience Names
    careers_df = pd.read_csv('data/job_titles_and_career_paths.csv', header=0)  
    list_of_career_experience_options = careers_df["2018 SOC Direct Match Title"].unique().tolist()

    # Prepare data - Career fields
    list_of_career_fields = careers_df["2018 SOC Major Group"].unique().tolist()


    # GENERATE DATA

    # Generate Data - Method that handles creation of career experiences given a student id, their first academic year, and the final year we should have data for
    # Method approach was used to avoid iterrowing over the df
    def generate_career_experiences_for_one_student_year(student_id, academic_year, max_year):
        
        # max year in enrollments record is assumed to be "current" year after which we should not have data
        # Given a student id and a year, jobs are generated with some number of days as the tenure (minimum of 365)
        # until "current year" is reached or exceeded for which "present" is used as end date.
        
        # Generate data - Max end date 
        max_date = datetime.date( max_year, 1, 1)

        # Set minimum start date based on student's first eligible academic year
        end_date = datetime.date( int(academic_year[:4]), random.randrange(1,12), 1)

        # Generate career experiences initializing end date with minimum:
        while end_date < max_date:

            # Generate data - Student ID
            list_of_student_ids.append(student_id)

            # Generate data - Organization ID
            list_of_org_ids.append(list_of_org_id_options[random.randrange(0,len(list_of_org_id_options))])

            # Generate data - Career Experience Name
            career_experience_name = list_of_career_experience_options[random.randrange(0,len(list_of_career_experience_options))] # will be used again
            list_of_career_experience_names.append(career_experience_name)

            # Generate data - Career field
            # filter by direct match title, get career field
            this_career_experience_df = careers_df[careers_df["2018 SOC Direct Match Title"] == career_experience_name]
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


    # EXPORT AS DATAFRAME AND CSV

    # Export - Create data frame
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

    # Export - Export CSV and return DataFrame
    df.to_csv('output/careers.csv', index=False)
    return df


def generate_activities(permanent_records, enrollment_records):    
    # VARIABLE PARAMETERS FOR GENERATION
    
    # Variable paramters - On average, most student will have 3 activities at a time
    avg_activities_at_a_time = 3
    stddev_activities = 2

    # Variable paramters - Grades that are typically school thresholds during which a student would get all new activities
    grades_that_trigger_activity_rerolling = ["9", "C1"]


    # PREPARE LOOKUPS, SOURCES OF DATA, AND CONTAINERS

    # Prepare - Lists of data to be generated then converted to pandas DF
    list_of_student_ids = []
    list_of_activity_ids = []
    list_of_activity_names = []
    list_of_activity_types = []
    list_of_grades_participated = []

    # Prepare - During data generation, a student will have a set of "current" activities that may change slightly year to year
    list_of_students_current_activities = []

    # Prepare - Load activity options
    dataframe_of_activity_options = pd.read_csv('data/student_organizations.csv')
    list_of_tuples_of_activity_type_and_name = [(x,y) for x, y in zip(dataframe_of_activity_options["Type"], dataframe_of_activity_options["Name"])]

    # Prepare - Get student ID's from permrecs
    list_of_studentids_from_permrecs = permanent_records["Student ID"].tolist()

    # Prepare - For each ID, subset enrollment records for each student and create a tuple to later be used
    list_of_studentID_grade_tuples = []
    for id in list_of_studentids_from_permrecs:
        this_students_enrollment_records = enrollment_records[enrollment_records["Student ID"] == str(id)]
        this_students_grades = this_students_enrollment_records["Grade"].tolist()
        list_of_studentID_grade_tuples.append((id, this_students_grades))


    # GENERATE DATA

    # Generate Data - Loop through students ang generate activity records
    # Each student will have their own base number of activities (some students tend to have more activities and some less)
    # For each grade we have about the student, make sure they have within 1 or the base number of activities
    for studentid_grade in list_of_studentID_grade_tuples:

        # Set this student's number of activities (this student will always have that number plus or minus 1)
        base_number_of_activities = int(random.gauss(avg_activities_at_a_time, stddev_activities))

        for grade in studentid_grade[1]:
            modifier = random.randint(-1,1)
            number_of_activities_for_this_student_this_year = max(0, base_number_of_activities + modifier)

            # To simulate getting new activities at new schools, clear the list when crossing major grade boundaries
            if grade in grades_that_trigger_activity_rerolling:
                list_of_students_current_activities = []

            while number_of_activities_for_this_student_this_year > len(list_of_students_current_activities):

                # Randomly choose an activity and type
                random_activity_and_type = list_of_tuples_of_activity_type_and_name[random.randrange(len(list_of_tuples_of_activity_type_and_name))]
                activity_type = random_activity_and_type[0]
                activity_name = random_activity_and_type[1]

                # Add random activity with random type as tuple to list_of_students_current_activities
                list_of_students_current_activities.append((activity_type, activity_name))

            while number_of_activities_for_this_student_this_year < len(list_of_students_current_activities): 

                #remove random item from list_of_students_current_activities
                index_to_remove = random.randrange(0,len(list_of_students_current_activities))
                del list_of_students_current_activities[index_to_remove]

            # by this point, the student's list of current activities should have the correct number
            # create the records
            for activity in list_of_students_current_activities:
                list_of_student_ids.append(studentid_grade[0])
                list_of_activity_names.append(activity[1])
                list_of_activity_types.append(activity[0])
                list_of_grades_participated.append(grade)

    # Generate data - Primary keys based on number of records
    list_of_activity_ids = [x+1 for x in range(len(list_of_student_ids))]


    # EXPORT AS DATAFRAME AND CSV

    # Export - Create data frame
    data = {
        "Activity ID": list_of_activity_ids,
        "Student ID": list_of_student_ids,
        "Activity Name": list_of_activity_names,
        "Activity Type": list_of_activity_types,
        "grades_participated": list_of_grades_participated,
    }
    df = pd.DataFrame(data)

    # Export - Export CSV and return DataFrame
    df.to_csv('output/activities.csv', index=False)
    return df



if __name__ == "__main__":
    permrecs = generate_permrecs()
    enrollment = generate_enrollment(permrecs)
    organizations = generate_organizations()
    internships = generate_internships(enrollment, organizations)
    careers = generate_career_experiences(enrollment, organizations)
    activities = generate_activities(permrecs, enrollment)


# TO DO
# Add more comments
# Change career field selector for internships to match career experience generator
# Make enrollments use existing df and not the csv
# Each activites entry should have a list of grades participated instead of multiple records for the same activity per student


# Notes to move to readme

# Enrollment 
    # For each student, make enrollment records
    #   Determine year based on grade by adding to student's DOB the looked up age from grade 
    #   All students get at least one enrollment record with a randomly chosen school
    #   After each enrollment record, there is a change the student does not continue
    #   If the student does continue, make another record

# Activities
    # For each student, generate activities that cover the time they are in the program.
    # Some students tend to have more, some tend to have less
    # Given a student, get the number of years they are in the program
    #   - Choose how many activities we are going to give them
    #   - Each year, give them that many activities +- 1
    #   - If they need to gain or lose an activity, pick one at random
    #   - Set grade boundaries for completely redoing activities