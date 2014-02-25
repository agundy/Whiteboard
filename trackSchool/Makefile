clean:
	rm 4xBDBs
	./manage.py syncdbd
	./manage.py schemamigration courses --initial
	./manage.py migrate courses --fake

migrate:
	./manage.py schemamigration courses --auto
	./manage.py migrate courses 
	./manage.py syncdb

run:
	./manage.py syncdb
	./manage.py runserver
