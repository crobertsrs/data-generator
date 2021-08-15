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
- Student ID
- Organization ID
- Internship Name
- Internship Career Path
- Is Desired Career Path?
- Interviewed?
- Accepted?
- Completed?
- Start Date
- End Date

**Organizations**
One record per organization.

- Organization ID
- Organization Name

**Careers**
These records are meant to track student careers. Each row has the following information:

- Career Experience ID
- Student ID
- Organization ID
- Career Experience Name
- Career Path
- Is Desired Career Path
- Start Date
- End Date

The rough idea is that starting in 9th grade, we might keep track of the career experiences students are engaging in. Even if they end up not continuing in our program, it can be helpful to know whether or not they are working in their desired field. Though we don't currently collect information in this manner, one could imagine an organization using public tools like LinkedIn, asking alumni, or reaching out to organizational partners to see where students are in their careers. 

For simplicity, this version of the data generator starts giving students career experiences in 9th grade. Each experience lasts a few years, then within 1 month they start a new one. The rate at which any one experience is within their desired career path is randomly chosen. Though that doesn't really reflect reality, it is helpful for testing later.

**Activities**
For simplicity, example activities were scraped from a public website of the University of Michigan (see details below).

0-20 records per student starting in MS, contains the following information:

- Activity ID
- Student ID
- Activity Name
- Activity Type
- List of Grades Participated

## References / Data Sources

first_names.txt comes directly from the U.S. Social Security Association list of baby names 2020 https://www.ssa.gov/oact/babynames/limits.html and originally had the name yob2020.txt from the National data set.

last_names.txt was generated with the following call to the census api
`api.census.gov/data/2010/surname?get=NAME,COUNT&RANK=200:500`
it has the following structure:
`["NAME","COUNT","RANK"]`

lower_ed_schools.csv is derived from data from the Washington state Office of the Superintendent of Public Instruction (OSPI), but I didn't want to end up hosting a copy of that data in this repo, so I kept only what I needed. I took the 2021 enrollment report card, filtered for schools with names containing the words "elementary", "middle", and "high". Then I filtered to only include schools in the Seattle, Renton, and Highline school districts. Then I deleted all data except school and district names and deduplicated rows. Data from the WA OSPI can be found at https://www.k12.wa.us/data-reporting/data-portal

higher_ed_schools.csv is derived from the Postsecondary School Location - Current dataset that can be found on the NCES website or data.gov, but I didn't want to end up hosting a copy of that data in this repo, so I kept only what I needed. I kept only the name of the institution, deduplicated rows, then did a little manual cleaning to thin out some of the university systems with many locations. Data from data.gov can be found at https://catalog.data.gov/dataset/postsecondary-school-locations-current

organization_names.txt was generated with https://randommer.io/random-business-names 

job_titles_and_career_paths.csv is the direct match file from the U.S. Bureau of Labor Statistics' 2018 Standard Occupational Classification System modified to include the major and minor groups found in the 2018 SOC Structure https://www.bls.gov/soc/2018/#materials 


student_organizations.txt and student_organization_types.txt were both retrieved from the University of Michigan list of student organizations using api calls that the site appears to be making. The types file is the response, copied with the browser's devtools, from the following call that the website itself makes:
```
https://maizepages.umich.edu/api/discovery/organization/category?take=100&orderByField=name&ids%5B0%5D=16550&ids%5B1%5D=3648&ids%5B2%5D=3649&ids%5B3%5D=3650&ids%5B4%5D=3651&ids%5B5%5D=3652&ids%5B6%5D=3653&ids%5B7%5D=3654&ids%5B8%5D=3655&ids%5B9%5D=3656&ids%5B10%5D=3657&ids%5B11%5D=3658&ids%5B12%5D=3659&ids%5B13%5D=3660&ids%5B14%5D=3693&ids%5B15%5D=4212&ids%5B16%5D=4568&ids%5B17%5D=8247&ids%5B18%5D=8248&ids%5B19%5D=8249&ids%5B20%5D=8250
```
The call for getting information about each organization that the site makes is:
```
https://maizepages.umich.edu/api/discovery/search/organizations?orderBy[0]=UpperName asc&top=10&filter=&query=&skip=10
```
The script get_student_orgs.py makes a bunch of requests to get the list of student organizations, then the parse_student_orgs.py script tidies them up into a dictionary of organization types with organization names in each category (there are duplicates). This is meant to emulate the real world data in which the organization names and types are entered by staff in a not necessarily uniform way. The `requests` and `json` modules were used to scrape and parse the list of student organizations. 

