#!/bin/sh

docker run --name rl_master -d -p 8080:8080 --env-file .env --rm cr1337:rl_master