#!/usr/bin/env bash

docker compose exec -it db bash
# OR
docker compose exec -it db mysql -u root -p

