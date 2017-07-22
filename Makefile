APP_LIST ?= mysite minesweeper

.PHONY: install test ci

install:
	pip install -r requirements/dev.txt
	npm install

migrations-check:
	python manage.py makemigrations --check --dry-run

test: migrations-check
	@coverage run --source=. manage.py test -v2 $(APP_LIST)

ci: test
	@coverage report
