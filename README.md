# Minesweeper
[![Build Status](https://travis-ci.com/d8660091/minesweeper.svg?token=poM8cpAzssr1tR1xqCdN&branch=master)](https://travis-ci.com/d8660091/minesweeper)
[![Coverage Status](https://coveralls.io/repos/github/d8660091/minesweeper/badge.svg?t=RwWiOT)](https://coveralls.io/github/d8660091/minesweeper)

![screenshot][screenshot]

### [minesweeper.xudeng.io](http://minesweeper.xudeng.io)

A multiplayer online minesweeper game built with Django Channel and Vue.

## Introduction

* __Vue__ is used for rendering the game graphics. But the priority for frontend is not high since it's much more important to guarantee bug-free backend, so webpack with live reloading is not set.

* __sqlite3__ is used for prototyping. Postgres or Mysql may be used for production.

* __Websocket__ is used to provide a stable, low-latency, bi-directional connection. Users can play the game in their browser without noticing the game core is on the backend. 

* __Django__ Channel is responsible for handling the requests from frontend, for example, when user clicks a tile and send the action to the server, Django Channel returns the new game data to the user. It also notifies the frontend actively when it detects data changing of game data in the database.

## Run locally
1. Create a Python 3.6 virtualenv
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

## Map

Game data is composed of mainly two arrays, game_data and game_mask. Game_data is the underlying matrix that contains the 'true' data of the game, which should be hidden from users. So game_mask's responsibility is to keep track of the game's progress and reveal only the visible information to users. When we combine game_data and game_mask with some matrix operations, we can get a user_map which is passed to the frontend to be rendered by Vue.

Rendered game 1:

![rendered-game][example-game]

Corresponding data 2 (-1 means mine):

![data][example-data]

Rendered game 2:

![rendered-game-2][example-game-2]

Corresponding data 2 (viewed by user, -2 means hidden):

![data][example-data-2]

### Special Tiles
* Tile 0:
![tile -0][tile-0]

* Tile -1:
![tile -1][tile-1]

* Tile -2:
![tile -2][tile-2]

* Tile -3:
![tile -3][tile-3]

* Tile -4:
![tile -4][tile-4]

* Tile -5:
![tile -5][tile-5]

[screenshot]: http://imgur.com/a4noUAr.png
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
