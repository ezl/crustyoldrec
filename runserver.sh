#!/bin/sh

ps aux | grep -v "grep" | grep  "runserver" | awk {'print $2'} | xargs kill > /dev/null
/usr/bin/python /home/atlantic304/src/reconciliation/manage.py runserver_plus 0.0.0.0:8000
