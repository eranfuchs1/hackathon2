import bpy
import os
import sys
import copy
import os.path
import threading
import time

def write_to_file(fname):
    bpy.ops.wm.save_as_mainfile(filepath=str('./{}'.format(fname)))




def render_ascii_cubes():
    global alldata3d
    next_alldata3d = {}
    override = bpy.context.copy()
    with open('./test20.ascii3d', 'r') as f:
        next_alldata3d = eval(f.read())
    for key in next_alldata3d:
        if key in alldata3d:
            continue
        z, y, x = key.split(' ')
        z = int(z)
        y = int(y)
        x = int(x)
        cell = next_alldata3d[key]
        if cell != ' ':
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.selected_objects[0]
            cube.location = (float(x) * 2, float(y) * 2, float(z) * 2)
    alldata3d.update(next_alldata3d)
    #bpy.types.Scene.update()
    #bpy.context.scene.update()
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    return 2.0



alldata3d = {}


bpy.app.timers.register(render_ascii_cubes)
