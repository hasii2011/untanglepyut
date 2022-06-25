#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=$(basename ${PWD})
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes untanglepyut tests
# mypy --config-file .mypi.ini --pretty  --show-error-codes untanglepyut tests
status=$?

echo "Exit with status: ${status}"
exit ${status}

