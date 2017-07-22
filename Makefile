APP_LIST ?= mysite minesweeper

migrations-check:
	python manage.py makemigrations --check --dry-run

test: migrations-check
	@coverage run --source=. manage.py test -v2 $(APP_LIST)

ci: test
	@coverage report
