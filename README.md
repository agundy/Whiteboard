Whiteboard
===

Whiteboard helps keep track of your homework and grades for your classes and allows groups to keep track of members grades for membership requirements.

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

A Student login is available with 
Username: test@rpi.edu
Password: password

A Admin account can be accessed with
Username: admin
Password: password

Core Functionality:
-------------------
- Track School related assignments

- Integrate w/ Google Calender

- Manage Class Grades

- Prioritize by grade(impact on class standing)

- Recommend best time to do homework(consider sleep/early classes)

- Actively remind to input assignments

Summer Goals
------------
- ~~Ability to add assignments for a course with due dates and points~~

- Have ability to integrate with other calenders.

- ~~Get adding grades and assignments working like tests and other assignments~~

- Track grades and allow for weighting of assignment groups on final grade

- Add a priority picker for homework to help decide what to work on

- Get a REST API set up to all for mobile development

- ~~Begin working on classes and group functionality~~
