all:
	python ./manage.py syncdb --settings=trackSchool.settings.dev
	python manage.py runserver --settings=trackSchool.settings.dev

local:
	python ./manage.py syncdb --settings=trackSchool.settings.dev
	python ./manage.py runserver --settings=trackSchool.settings.dev 0.0.0.0:8000

clean:
	rm WhiteboardDB || echo "No Database"
	rm -r courses/migrations/ || echo "No Directory"
	python ./manage.py syncdb --settings=trackSchool.settings.dev
	python ./manage.py schemamigration courses --initial --settings=trackSchool.settings.dev
	python ./manage.py migrate courses --fake --settings=trackSchool.settings.dev

start:
	python ./manage.py syncdb --settings=trackSchool.settings.dev
	python ./manage.py schemamigration courses --initial --settings=trackSchool.settings.dev
	python ./manage.py migrate courses --fake --settings=trackSchool.settings.dev
	python ./manage.py syncdb --settings=trackSchool.settings.dev

migrate:
	python ./manage.py schemamigration courses --auto --settings=trackSchool.settings.dev || echo "No courses migrations needed."
	python ./manage.py migrate courses --settings=trackSchool.settings.dev
	python ./manage.py syncdb --settings=trackSchool.settings.dev

migratec:
	python ./manage.py schemamigration courses --auto --settings=trackSchool.settings.dev || echo "No courses migrations needed."
	python ./manage.py migrate courses --settings=trackSchool.settings.dev
	python ./manage.py syncdb --settings=trackSchool.settings.dev

test:
	python ./manage.py syncdb --settings=trackSchool.settings.dev
	python ./manage.py loaddata ./courses/fixtures/initial_data.json
	python ./manage.py schemamigration courses --initial
	python ./manage.py migrate courses --fake --settings=trackSchool.settings.dev
