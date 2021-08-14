
if [ -z "$1" ]; then
	echo 'ERROR: no file name provided, exiting'
	exit 1
fi

python interactive.py $1
