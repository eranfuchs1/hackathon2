
if [ -z "$1" ]; then
	echo 'ERROR: no file name provided, exiting'
	exit 1
fi

blender --python interactive_blender_side.py $1
