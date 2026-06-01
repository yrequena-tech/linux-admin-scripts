#!/bin/bash

while true; do
	echo ""
	echo "====User Management Menu ===="
	echo "1. Add a user"
	echo "2. Delete a user"
	echo "3. Change a user password"
	echo "4. List all users"
	echo "5. Exit"
	echo "============================="
	read -p "Enter your choice [1-5]: " choice

	case $choice in
		1) 
		  read -p "Enter username to add: " username
		  sudo useradd "$username"
		  echo "User $username added."
		  ;;
		2)
		  read -p "Enter username to delete: " username
		  sudo userdel -r "$username"
		  echo "User $username deleted."
		  ;;
		3)
		  read -p "Enter username to change password: " username
		  sudo passwd "$username"
		  ;;
		4)
		  echo "Current users:"
		  cut -d: -f1 /etc/passwd
		  ;;
		5)
		  echo "Goodbye!"
		  exit 0
		  ;;
		*)
		  echo "invalid option. Please enter 1-5."
		  ;;
	esac
done
