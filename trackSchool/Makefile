all:
	./manage.py syncdb
	./manage.py runserver

clean:
	rm 4xBDB
	rm -r courses/migrations/
	rm -r gradeGroup/migrations/
	./manage.py syncdb
	./manage.py schemamigration courses --initial
	./manage.py schemamigration gradeGroup --initial
	./manage.py migrate courses --fake
	./manage.py migrate gradeGroup --fake

start:
	./manage.py syncdb
	./manage.py schemamigration courses --initial
	./manage.py schemamigration gradeGroup --initial
	./manage.py migrate courses --fake
	./manage.py migrate gradeGroup --fake
	./manage.py syncdb


migrate:
	./manage.py schemamigration courses --auto
	./manage.py schemamigration gradeGroup --auto
	./manage.py migrate courses
	./manage.py migrate gradeGroup
	./manage.py syncdb

migratec:
	./manage.py schemamigration courses --auto
	./manage.py migrate courses
	./manage.py syncdb

migrateg:
	./manage.py schemamigration gradeGroup --auto
	./manage.py migrate gradeGroup
	./manage.py syncdb

test:
	./manage.py syncdb
	./manage.py loaddata ./courses/fixtures/initial_data.json
	./manage.py schemamigration courses --initial
	./manage.py schemamigration gradeGroup --initial
	./manage.py migrate courses --fake	
	./manage.py migrate gradeGroup --fake
