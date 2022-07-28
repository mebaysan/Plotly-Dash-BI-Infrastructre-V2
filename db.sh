#! /bin/bash

docker run --name postgres -e POSTGRES_PASSWORD=123456 -d -p 5433:5432 -v /tmp/dash-web-app/volumes/postgres:/var/lib/postgresql/data postgres