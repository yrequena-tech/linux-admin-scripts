#!/bin/bash

echo "Starting system update..."
sudo dnf check-update

read -p "Do you want to upgrade now? (y/n): " confirm

if [ "$confirm" == "y" ]; then
	sudo dnf upgrade -y
	echo "System upgraded successfully."
else
	echo "Upgrade cancelled."
fi 
