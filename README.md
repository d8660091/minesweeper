# Minesweeper

A minesweeper game built with Django Channel and Vue

## Run locally
1. Create a python 3.6 virtualenv
2. Install dependencies

```shell
pip install -r requirements/dev.txt
```

3. Run local server

``` shell
python manage.py runserver
```

## Frontend
Vue app, game is rendered with mainly css.

## Backend
Django with channels.
Game data is stored in sqlite3, but can be easily changed to other databases if desired.
