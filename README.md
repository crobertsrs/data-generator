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
- Student ID
- Academic Year
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

## References / Data Sources

first_names.txt comes directly from the U.S. Social Security Association list of baby names 2020 https://www.ssa.gov/oact/babynames/limits.html and originally had the name yob2020.txt from the National data set.

last_names.txt was generated with the following call to the census api
`api.census.gov/data/2010/surname?get=NAME,COUNT&RANK=200:500`
it has the following structure:
`["NAME","COUNT","RANK"]`

lower_ed_schools.csv is derived from data from the Washington state Office of the Superintendent of Public Instruction (OSPI), but I didn't want to end up hosting a copy of that data in this repo, so I kept only what I needed. I took the 2021 enrollment report card, filtered for schools with names containing the words "elementary", "middle", and "high". Then I filtered to only include schools in the Seattle, Renton, and Highline school districts. Then I deleted all data except school and district names and deduplicated rows. Data from the WA OSPI can be found at https://www.k12.wa.us/data-reporting/data-portal

higher_ed_schools.csv is derived from the Postsecondary School Location - Current dataset that can be found on the NCES website or data.gov, but I didn't want to end up hosting a copy of that data in this repo, so I kept only what I needed. I kept only the name of the institution, deduplicated rows, then did a little manual cleaning to thin out some of the university systems with many locations. Data from data.gov can be found at https://catalog.data.gov/dataset/postsecondary-school-locations-current
