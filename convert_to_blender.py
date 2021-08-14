import curses
import sys
import copy
import os.path


alldata3d = {}
if os.path.isfile(f'{sys.argv[4]}.ascii3d'):
    with open(f'{sys.argv[4]}.ascii3d', 'r') as f:
        alldata3d = eval(f.read())



import bpy
import os

def render_ascii_cubes(alldata3d):
    for key in alldata3d:
        z, y, x = key.split(' ')
        z = int(z)
        y = int(y)
        x = int(x)
        cell = alldata3d[key]
        if cell != ' ':
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.selected_objects[0]
            cube.location = (float(x) * 2, float(y) * 2, float(z) * 2)


def write_to_file(fname):
    bpy.ops.wm.save_as_mainfile(filepath=str('./{}.blend'.format(fname)))

render_ascii_cubes(alldata3d)
write_to_file(sys.argv[5])
