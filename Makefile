migrations-check:
	python manage.py makemigrations --check --dry-run

test: migrations-check
	python manage.py test
