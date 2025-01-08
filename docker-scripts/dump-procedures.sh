#!/usr/bin/env bash

SCRIPTS_DIR=$(dirname ${BASH_SOURCE})

. ${SCRIPTS_DIR}/dump.source

DATABASE=
SQL_FILE=
check_params "${@}"

DOCKER_OUTPUT_DIR=out
DOCKER_INPUT_DIR=in

echo "DATABASE.............: ${DATABASE}"
echo "SQL_FILE.............: ${SQL_FILE}"
echo "DOCKER_INPUT_DIR.....: ${DOCKER_INPUT_DIR}"
echo "DOCKER_OUTPUT_DIR....: ${DOCKER_OUTPUT_DIR}"

DOCKER_COMMAND_PARTS=(
    "mysqldump -u root -p"                             # run mysqldump as root
    "--routines"                                       # backup stored procedures
    "--no-create-info"                                 #
    "--no-data"                                        #
    "--no-create-db"                                   #
    "--skip-opt"                                       #
    "--skip-triggers"                                  #
    "${DATABASE} > /${DOCKER_OUTPUT_DIR}/${SQL_FILE}"  #
)
DOCKER_COMMAND="${DOCKER_COMMAND_PARTS[*]}"
echo "docker compose exec -it db /bin/bash -c" "${DOCKER_COMMAND}"
docker compose exec -it db /bin/bash -c "${DOCKER_COMMAND}"

