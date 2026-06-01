#!/bin/bash

IP_FILE="last_ip.txt"

# Get current public IP
CURRENT_IP=$(curl -s ifconfig.me)

echo "Current public IP: $CURRENT_IP"

# Check if file exists
if [ ! -f "IP_FILE" ]; then
	echo "$CURRENT_IP" > "$IP_FILE"
	echo "First run - IP saved."
else
	LAST_IP=$(cat "$IP_FILE")

	if [ "CURRENT_IP" == "LAST_IP" ]; then
	   echo "IP has not changed."
	else
	   echo "IP CHANGED! old: $LAST_IP -> New: $CURRENT_IP"
	   echo "$CURRENT_IP" > "IP_FILE"
	fi
fi
