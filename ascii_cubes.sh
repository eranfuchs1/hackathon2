
if [ -z "$1" ]; then
	echo 'ERROR: no file name provided, exiting'
	exit 1
fi

blender --background --python untitled.py $1 --app-template "$(pwd)/startup.blend"
