#!/bin/bash

USERFILE="users.txt"

if [ ! -f "$USERFILE" ]; then
	echo "User file not found!"
	exit 1
fi

while IFS= read -r username; do
	if id "$username" &>/dev/null; then
		echo "User $username already exists. Skipping."
	else
		useradd "$username"
		echo "User $username created."
	fi
done < "$USERFILE"

echo "DONE."
