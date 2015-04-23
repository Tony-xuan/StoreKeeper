#!/bin/bash -e
PYTHON_VERSION=3.4

function init()
{
    PYTHON="python${PYTHON_VERSION}"
    if [ "${GLOBAL_INSTALL}" == false ]
    then
        PYTHON='flask/bin/python'
    fi

    PIP='sudo pip3'
    if [ "${GLOBAL_INSTALL}" == false ]
    then
        PIP="${PYTHON} -m pip"
    fi
}

function do_preinstall()
{
    # Extra dependencies for fast Yaml file reading (http://stackoverflow.com/a/24791419/1108919)
    packages="build-essential python${PYTHON_VERSION} python${PYTHON_VERSION}-dev libyaml-dev"
    if [ "${GLOBAL_INSTALL}" == true ]
    then
        packages="${packages} python3-pip"
    else
        packages="${packages} python-virtualenv"
    fi
    apt_get_install ${packages}

    if [ "${GLOBAL_INSTALL}" == false ]
    then
        # Install virtualenv
        if [ ! -e flask ]
        then
            virtualenv -p python${PYTHON_VERSION} flask
        fi
    fi
    ${PIP} install --upgrade pip setuptools
}

function do_install()
{
    ${PIP} install -r requirements.txt --upgrade
    if [ "${PRODUCTION}" == false ]
    then
        ${PIP} install -r requirements-dev.txt --upgrade
    fi

    mkdir -p tmp
}

function do_clear()
{
    purge tmp
    purge flask
    purge test/.cache
    find_and_purge -name __pycache__
}

function do_start()
{
    ${PYTHON} run.py
}

function do_test()
{
    ./test.sh "$@"
}


cd "$(dirname "$0")"
source ../.main.sh
