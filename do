#!/bin/bash

CONTAINERS=(web db)
export COMPOSE_FILE=local.yaml

function rmdocker { echo "Deleting containers and purging volumes..."
    for c in "${CONTAINERS[@]}"; do
        echo "Stopping  & Delete: $c"
        docker-compose stop -t 1 $c
        docker-compose rm -f $c
    done
    # Space reclamation
    docker volume prune -f
}


function setup {
    rmdocker

    docker-compose build
    echo -e "\nStarting Postgres Server to create DB first"
    docker-compose up -d db  && sleep 15

    docker-compose up -d && echo -e "\nWaiting for docker to come up (and migrate) this takes one minute..." && sleep 10

    echo "(!) setup completed"
}


function usage {
    echo "ERROR: Please provide a function name. Available functions:"
    echo
    declare -f | grep '()' | grep -v 'grep' | sort | sed -e 's/^/  /'
    exit 1
}

if [[ "$#" -eq 0 ]]; then
    usage
else
    $@
fi