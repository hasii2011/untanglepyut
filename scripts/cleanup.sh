#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

rm -rf dist build

find . -type d -name '*'.egg-info -delete

rm -rf .eggs
rm -rfv untanglepyut.egg-info
