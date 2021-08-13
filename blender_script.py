import bpy
import sys
import os

def render_ascii_cubes(data3d):
    for z, slc in enumerate(data3d):
        for y, row in enumerate(slc):
            for x, cell in enumerate(row):
                if cell != ' ':
                    bpy.ops.mesh.primitive_cube_add()
                    cube = bpy.context.selected_objects[0]
                    cube.location = (float(x), float(y), float(z))


def write_to_file(fname):
    bpy.ops.wm.save_as_mainfile(f'{fname}.blend')
