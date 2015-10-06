#!/bin/sh

# path to xinit exec
DAEMON=/usr/bin/python

# startup args
DAEMON_OPTS=" /usr/bin/oldphone/OldPhone-Keypad/program/keypad.py"

# script name
NAME=oldphonekeypad

# app name
DESC=OldPhoneKeyPad

# user
RUN_AS=root

# Path of the PID file
PID_FILE=/var/run/keypadd.pid

############### END EDIT ME ##################

test -x $DAEMON || exit 0

set -e

case "$1" in
  start)
        echo "Starting $DESC"
        start-stop-daemon --start -c $RUN_AS --background --pidfile $PID_FILE  --make-pidfile --exec $DAEMON -- $DAEMON_OPTS
        ;;
  stop)
        echo "Stopping $DESC"
        start-stop-daemon --stop --pidfile $PID_FILE
        ;;

  restart|force-reload)
        echo "Restarting $DESC"
        start-stop-daemon --stop --pidfile $PID_FILE
        sleep 5
        start-stop-daemon --start -c $RUN_AS --background --pidfile $PID_FILE  --make-pidfile --exec $DAEMON -- $DAEMON_OPTS
        ;;
  *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|force-reload}" >&2
        exit 1
        ;;
esac

exit 0
