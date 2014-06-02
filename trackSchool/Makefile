all:
	./manage.py syncdb
	./manage.py runserver

local:
	./manage.py syncdb
	./manage.py runserver 0.0.0.0:8000

clean:
	rm 4xBDB || echo "No Database"
	rm -r courses/migrations/ || echo "No Directory"
	rm -r gradeGroup/migrations/ || echo "No Directory"
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
	./manage.py schemamigration courses --auto || echo "No courses migrations needed."
	./manage.py schemamigration gradeGroup --auto || echo "No gradeGroup changes needed."
	./manage.py migrate courses
	./manage.py migrate gradeGroup
	./manage.py syncdb

migratec:
	./manage.py schemamigration courses --auto  || echo "No courses migrations needed."
	./manage.py migrate courses
	./manage.py syncdb

migrateg:
	./manage.py schemamigration gradeGroup --auto || echo "No gradeGroup changes needed."
	./manage.py migrate gradeGroup
	./manage.py syncdb

test:
	./manage.py syncdb
	./manage.py loaddata ./courses/fixtures/initial_data.json
	./manage.py schemamigration courses --initial
	./manage.py schemamigration gradeGroup --initial
	./manage.py migrate courses --fake	
	./manage.py migrate gradeGroup --fake
