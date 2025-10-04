#!/usr/bin/bash

sql_script="$1"

if [[ ! -f "${sql_script}" ]]; then
	echo "ERROR: No such file: ${sql_script}" >&2
	exit 1
fi

echo -e "\n# --- RUNNING SQLSCRIPT ---\n"
sqlite3 db.sqlite3 < "${sql_script}" &
sleep 1

echo -e "\n# --- VIEW DB STATE ---\n"
sqlite3 db.sqlite3 <<- EOF
	.mode column
	SELECT * FROM users;
EOF
