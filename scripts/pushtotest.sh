#!/bin/bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}
changeToProjectRoot

clear

twine upload --repository-url https://test.pypi.org/legacy/ dist/*
