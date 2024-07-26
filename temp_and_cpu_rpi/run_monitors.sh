#!/bin/bash

if [ "$#" -ne 9 ]; then
    echo "Usage: $0 <IP1> <User1> <Pass1> <IP2> <User2> <Pass2> <IP3> <User3> <Pass3>"
    exit 1
fi

./monitor.sh "$1" "$2" "$3" &
./monitor.sh "$4" "$5" "$6" &
./monitor.sh "$7" "$8" "$9" &

