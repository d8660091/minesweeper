# Minesweeper
[![Build Status](https://travis-ci.com/d8660091/minesweeper.svg?token=poM8cpAzssr1tR1xqCdN&branch=master)](https://travis-ci.com/d8660091/minesweeper)
[![Coverage Status](https://coveralls.io/repos/github/d8660091/minesweeper/badge.svg?t=RwWiOT)](https://coveralls.io/github/d8660091/minesweeper)

### minesweeper.xudeng.io

A multiplayer online minesweeper game built with Django Channel and Vue. It can be accessed from 159.203.53.11 if DNS does not work yet.

## Introduction

### Vue
Vue is used for rendering the game graphics. But the priority for frontend is not high since it's much more important to guarantee bug-free backend, so webpack with live reloading is not set.

### Database
Sqlite3 is used for prototyping. Postgres or Mysql may be used for production.

### Django Channel and Websocket
Websocket is used to provide a stable, low-latency, bi-directional connection. Users can play the game in browser without noticing the game core is on the backend. Django Channel is responsible for handling the requests from frontend, for example, when user click a tile and send the action to server, django channel returns the new game data to the user. It also notify frontend when game data changes.

## Run locally
1. Create a python 3.6 virtualenv
2. Install dependencies

```shell
pip install -r requirements/dev.txt
bower install
```

3. Create tables:

``` shell
python manage.py migrate

```

4. Run the dev server

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

## Deploy
Make sure you have migrated data and collected static files, the path ./static is used for storing static files.

``` shell
docker-compose up
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

Tile 0:
![tile -0][tile-0]

Tile -1:
![tile -1][tile-1]

Tile -2:
![tile -2][tile-2]

Tile -3:
![tile -3][tile-3]

Tile -4:
![tile -4][tile-4]

Tile -5:
![tile -5][tile-5]

[example-game]: http://i.imgur.com/7Lj4oZC.png
[example-data]: http://imgur.com/1aY4eXw.png
[example-game-2]: http://imgur.com/JNVKCjA.png
[example-data-2]: http://imgur.com/XhEpOhD.png
[tile-0]: http://i.imgur.com/hlaMAdW.png
[tile-1]: http://i.imgur.com/9OPaqwj.png
[tile-2]: http://i.imgur.com/lQiLk0f.png
[tile-3]: http://i.imgur.com/8k9qw3a.png
[tile-4]: http://i.imgur.com/uldNo1D.png
[tile-5]: http://i.imgur.com/fIfDipg.png
