# data-generator

A tool for generating example data at Rainier Scholars

## Goals

The goal of the data generator are to be able to produce at least the following files that will produce a few files that roughly approximate some of the data used at Rainier Scholars. Generated data is used in testing and prototyping.

**Permanent Records**
One record per student, contains the following information

- Student ID
- First Name
- Last Name
- Cohort
- DOB

**Enrollment Records**
One record per student per year, contains the following information:

- Enrollment ID
- Year
- Grade
- School Name
- School District
- Exited this year?
- Exit Reason
- Exit Type

**Internships**
0-6 records per student (2 in HS and up to 5 in college), contains the following information:

- Internship ID
- Internship Name
- Organization ID
- Start Date
- End Date
- Student ID

**Organizations**
One record per organization.

- Organization ID
- Organization Name

**Careers**
0-4 records per student starting in HS.

- Role ID
- Role Title
- Organization ID
- Start Date
- End Date

**Activities**
0-20 records per student starting in MS, contains the following information:

- Activity ID
- Activity Name
- Activity Type
- Title
- Student ID
- List of Grades Participated

## References

first_names.txt comes directly from the U.S. Social Security Association list of baby names 2020 https://www.ssa.gov/oact/babynames/limits.html and originally had the name yob2020.txt from the National data set.

last_names.txt was generated with the following call to the census api
`api.census.gov/data/2010/surname?get=NAME,COUNT&RANK=200:500`
it has the following structure:
`["NAME","COUNT","RANK"]`
