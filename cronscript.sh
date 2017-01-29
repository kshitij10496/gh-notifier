#!/bin/sh
# Hack for using notify-send as cronjob
eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)";

#Code:
DISPLAY=:0
DIR=`dirname $0`
/usr/bin/env python3 $DIR/ghnotifier/main_cli.py
