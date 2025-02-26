#!/usr/bin/env bash

if [ "$1" == "-h" ]; then # CALL THE HELP TO EXPLAIN HOW TO USE THE SCRIPT
    echo "This script will create an app inside the apps folder"
    echo "To use type the following line:"
    echo "bash start-app.sh app_name project_folder"
    echo "Replace app_name with the actual name for your app"
    echo "Replace project_folder with the actual name for your project folder path if the script is out(optional)"

elif [ "$1" == "-e" ]; then # DISPLAY THE MESSAGE FOR THE CONFIGURATION IF YOU CLEAR THE CONSOLE
    echo "add INSTALLED_APPS += ['apps.app_name'] in your project's settings.py"
    echo "change the name of app_name in the app_name/apps.py -- app_nameConfig -- name to 'apps.app_name'"
elif [ "$1" != "" ]; then # CHECK IF YOU ADD THE APP NAME
    if [ -d $2 ]; then # CHECK IF THE PROJECT FOLDER IS ADDED
        cd $2 # CHANGE THE DIRECTORY TO THE PROJECT FOLDER
    fi
    if [ ! -d "apps" ]; then # CHECK IF THE APPS FOLDER EXISTS
        mkdir apps
        touch apps/__init__.py
    fi
    mkdir apps/$1 # CREATE THE APP_NAME FOLDER
    python manage.py startapp $1 apps/$1 # CREATE THE APP

    echo "Success! The app $1 has been aded, don't forget to:"
    echo "add INSTALLED_APPS += ['apps.$1'] in your project's settings.py"
    echo "change the name of $1 in the $1/apps.py -- $1Config -- name to 'apps.$1'"
else
    echo "USE THE PARAMETER -h TO DISPLAY HELP"
    echo "USE THE PARAMETER -e TO REDISPLAY THE SUCCES MESSAGE"
fi
