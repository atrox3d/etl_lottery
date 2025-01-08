#!/usr/bin/env bash

# from host
docker compose exec -it db bash
    # from container
    mysql --routines -u root -p < dump/filename.sql
# OR
docker compose exec -it db /bin/bash -c 'mysql --routines -u root -p employee < dump/filename'
