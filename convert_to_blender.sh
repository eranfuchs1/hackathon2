
if [ -z "$1" ]; then
	echo "ERROR: no input file given"
	exit 1
elif [ -z "$2" ]; then
	echo "ERROR: no output file name given"
	exit 1
fi
blender --background --python convert_to_blender.py $1 $2
