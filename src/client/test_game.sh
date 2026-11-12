#!/bin/bash

curl -s -X POST http://127.0.0.1:5000/game

GAME_UUID="fe7299a2-a187-4257-9b90-b47e25d10975"
curl -s -X POST http://127.0.0.1:5000/game/$GAME_UUID \
  -H "Content-Type: application/json" \
  -d '{"field": {"matrix": [[1,0,0],[0,0,0],[0,0,0]]}}'


curl -s -X POST http://127.0.0.1:5000/game/$GAME_UUID \
  -H "Content-Type: application/json" \
  -d '{"field": {"matrix": [[1,0,0],[0,2,0],[1,0,0]]}}'