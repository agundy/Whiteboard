all:
	./manage.py syncdb --settings=trackSchool.settings.dev
	python manage.py runserver --settings=trackSchool.settings.dev

local:
	./manage.py syncdb --settings=trackSchool.settings.dev
	./manage.py runserver --settings=trackSchool.settings.dev 0.0.0.0:8000

clean:
	rm WhiteboardDB || echo "No Database"
	rm -r courses/migrations/ || echo "No Directory"
	./manage.py syncdb --settings=trackSchool.settings.dev
	./manage.py schemamigration courses --initial --settings=trackSchool.settings.dev
	./manage.py migrate courses --fake --settings=trackSchool.settings.dev

start:
	./manage.py syncdb --settings=trackSchool.settings.dev
	./manage.py schemamigration courses --initial --settings=trackSchool.settings.dev
	./manage.py migrate courses --fake --settings=trackSchool.settings.dev
	./manage.py syncdb --settings=trackSchool.settings.dev

migrate:
	./manage.py schemamigration courses --auto --settings=trackSchool.settings.dev || echo "No courses migrations needed."
	./manage.py migrate courses --settings=trackSchool.settings.dev
	./manage.py syncdb --settings=trackSchool.settings.dev

migratec:
	./manage.py schemamigration courses --auto --settings=trackSchool.settings.dev || echo "No courses migrations needed."
	./manage.py migrate courses --settings=trackSchool.settings.dev
	./manage.py syncdb --settings=trackSchool.settings.dev

test-data:
	./manage.py syncdb --settings=trackSchool.settings.dev
	./manage.py loaddata ./courses/fixtures/initial_data.json
	./manage.py schemamigration courses --initial
	./manage.py migrate courses --fake --settings=trackSchool.settings.dev

test:
	./manage.py test --settings=trackSchool.settings.dev