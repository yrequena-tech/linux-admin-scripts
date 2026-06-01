#!/bin/bash

echo "Network Scanner"
echo "==============="

#Get local IP
IP=$(hostname -I | awk '{print $1}')
echo "Your IP: $IP"

# Extract network prefix (first 3 octets)
NETWORK=$(echo "$IP" | cut -d. -f1-3)

echo "Scanning network: $NETWORK.0/24"
echo ""

for i in $(seq 1 254); do
	HOST="$NETWORK.$i"
	ping -c 1 -w "$HOST" &>/dev/null
	if [ $? eq 0 ]; then
		echo "Host UP: $HOST"
	fi
done

echo ""
echo "Scan complete."
