# Minesweeper
[![Build Status](https://travis-ci.com/d8660091/minesweeper.svg?token=poM8cpAzssr1tR1xqCdN&branch=master)](https://travis-ci.com/d8660091/minesweeper)
[![Coverage Status](https://coveralls.io/repos/github/d8660091/minesweeper/badge.svg?t=RwWiOT)](https://coveralls.io/github/d8660091/minesweeper)

A minesweeper game built with Django Channel and Vue

## Run locally
1. Create a python 3.6 virtualenv
2. Install dependencies

```shell
pip install -r requirements/dev.txt
```

3. Run the dev server

``` shell
python manage.py runserver
```

## Test
Just run test

``` shell
tox
```

You can view the coverage report with

``` shell
coverage report
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

Rendered game 1:

![rendered-game][example-game]

Corresponding data 2 (-1 means mine):

![data][example-data]

Rendered game 2:

![rendered-game-2][example-game-2]

Corresponding data 2 (viewed by user, -2 means hidden):

![data][example-data-2]

[example-game]: http://i.imgur.com/7Lj4oZC.png
[example-data]: http://imgur.com/1aY4eXw.png
[example-game-2]: http://imgur.com/JNVKCjA.png
[example-data-2]: http://imgur.com/XhEpOhD.png
