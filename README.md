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
Connect to backend with

``` javascript
webSocketBridge.listen(`/minesweeper/stream/${session-id}`)
```

Vue app, game is rendered with mainly css.

## Backend
Django with channels.
Game data is stored in sqlite3, but can be easily changed to other databases if desired.

## Map

Rendered game:

![rendered-game][example-game]

Corresponding data:

![data][example-data]

[example-game]: http://i.imgur.com/7Lj4oZC.png
[example-data]: http://imgur.com/1aY4eXw.png
