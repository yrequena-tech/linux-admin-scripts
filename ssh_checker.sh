#!/bin/bash

SERVER_FILE="servers.txt"

if [ ! -f "$SERVER_FILE" ]; then
	echo "Server list file not found!"
	exit 1
fi

echo "==== SSH Availability Checker  ===="
echo ""

while IFS= read -r server; do
	nc -z -w 3 "$server" 22 &>/dev/null
	if [ $? -eq 0 ]; then
	   echo "[ UP ] $server - SSH port 22 is OPEN"
	else
	   echo "[ DOWN ] $server - SSH port 22 is CLOSED"
	fi
done < "$SERVER_FILE"

echo ""
echo "Scan complete."
