4xB  |   Blackboard, But Better
===============================

Academic Management System to supplement RPI's LMS system. We felt that LMS didn't not supply all of the functionality need for students and groups on campus. Below are some of the features we would like to implement.

Summer Goals
------------
- Ability to add assignments for a course

- Have ability to integrate with other calenders.

- Get adding grades and assignments working well

- Track grades and allow for weighting of assignment groups on final grade

- Add a priority picker for homework to help decide what to work on

- Get a REST API set up to all for mobile development

- Begin working on classes and group functionality


Core Functionality:
-------------------
-Track School related assignments

-Integrate w/ Google Calender

-Manage Class Grades

-Prioritize by grade(impact on class standing)

-Recommend best time to do homework(consider sleep/early classes)

-Actively remind to input assignments


Getting Started:
----------------
To get a working development environment
```bash
pip install -r requirements.txt
cd trackSchool
make start
```

To get a development environment with some test data already in the database, instead invoke
```bash
make test
```
