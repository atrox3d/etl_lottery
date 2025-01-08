#!/usr/bin/env bash

# from host
docker compose exec -it db bash
    # from container
    mysqldump -u root -p employee > dump/filename.sql
# OR
docker compose exec -it db /bin/bash -c 'mysqldumpmp -u root -p --events --routines --triggers --all-databases > /out/MySQLData.sql'
#  -u root -p employee > dump/test'
# docker compose exec -it db /bin/bash -c 'mysqldu