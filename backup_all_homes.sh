#!/bin/bash
BACKUP_DIR="$(date +%F)"
TIMESTAMP=$(date +%F)
mkdir -p "$BACKUP_DIR"

for dir in /tmp/testhomes/*; do
	user=$(basename "$dir")
	tar -czf "$BACKUP_DIR/${user}_backup_$TIMESTAMP.tar.gz" "$dir"
done
echo "Home directories backed up."
