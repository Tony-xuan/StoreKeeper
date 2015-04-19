#!/bin/bash -e

function do_preinstall()
{
    apt_get_install wget

    if [ ! -e '/etc/apt/sources.list.d/nodesource.list' ]
    then
        wget -q 'https://deb.nodesource.com/setup' -O - | sudo bash -
    fi
    apt_get_install nodejs
}

function do_postinstall()
{
    if [ "${PRODUCTION}" == true ]
    then
        npm install --production
    else
        npm install
        npm run update-webdriver
    fi
    node_modules/bower/bin/bower install
}

function do_clear()
{
    purge node_modules
    purge app/bower_components
}


cd "$(dirname "$0")"
source ../.main.sh
