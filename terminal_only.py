#!/bin/python3
import curses
import sys
import copy
import os.path

def all_to_data3d(data3d, alldata3d, cursor3d):
    answer = copy.deepcopy(data3d)
    for key in alldata3d:
        z, y, x = key.split(' ')
        z = int(z) - cursor3d[0] + (len(answer) // 2) + 1
        y = int(y) - cursor3d[1] + (len(answer) // 2) + 1
        x = int(x) - cursor3d[2] + (len(answer) // 2) + 1
        if z < 0 or z > len(answer) - 1:
            continue
        elif y < 0 or y > len(answer[0]) - 1:
            continue
        elif x < 0 or x > len(answer[0][0]) - 1:
            continue
        else:
            answer[z][y][x] = alldata3d[key]
    return answer


def view_top(data3d, height, width):
    view = [[' ' for x in range(width)] for y in range(height)]
    for y in range(len(data3d[0])-1,0,-1):
        for z in range(len(data3d)):
            for x in range(len(data3d[0][0])):
                if view[z][x] == ' ':
                    view[z][x] = data3d[z][y][x]
    return view

def view_bottom(data3d, height, width):
    view = [[' ' for x in range(width)] for y in range(height)]
    for y in range(len(data3d[0])):
        for z in range(len(data3d)):
            for x in range(len(data3d[0][0])):
                if view[z][x] == ' ':
                    view[z][x] = data3d[z][y][x]
    return view

def view_front(data3d, height, width):
    view = [[' ' for x in range(width)] for y in range(height)]
    for z in range(len(data3d)):
        for y in range(len(data3d[0])):
            for x in range(len(data3d[0][0])):
                if view[y][x] == ' ':
                    view[y][x] = data3d[z][y][x]
    return view

def view_left(data3d, height, width):
    view = [[' ' for x in range(width)] for y in range(height)]
    for z in range(len(data3d)):
        for y in range(len(data3d[0])):
            for x in range(len(data3d[0][0])):
                if view[y][z] == ' ':
                    view[y][z] = data3d[z][y][x]
    return view

def view_right(data3d, height, width):
    view = [[' ' for x in range(width)] for y in range(height)]
    for z in range(len(data3d)):
        for y in range(len(data3d[0])):
            for x in range(len(data3d[0][0]) - 1,0,-1):
                if view[y][(len(data3d) - 1) - z] == ' ':
                    view[y][(len(data3d) - 1) - z] = data3d[z][y][x]
    return view

views = {}
views['0 0'] = 'top'
views['0 1'] = 'front'
views['1 0'] = 'left'
views['1 1'] = 'right'

functions = {}
functions['0 0'] = view_top
functions['0 1'] = view_front
functions['1 0'] = view_left
functions['1 1'] = view_right


def move3d(cursor3d, y, x, i, j):
    global views, width, height
    view_name = views[f'{i} {j}']
    if view_name == 'top':
        cursor3d[0] += y
        cursor3d[2] += x
    elif view_name == 'front':
        cursor3d[1] += y
        cursor3d[2] += x
    elif view_name == 'left':
        cursor3d[1] += y
        cursor3d[0] += x
    elif view_name == 'right':
        cursor3d[1] += y
        cursor3d[0] -= x
    #cursor3d = check_limits_any(cursor3d, width)
    return cursor3d

def cursor2d(cursor3d, i, j):
    global width, views
    view_name = views[f'{i} {j}']
    y = 0
    x = 0
    if view_name == 'top':
        y = cursor3d[0]
        x = cursor3d[2]
    elif view_name == 'front':
        y = cursor3d[1]
        x = cursor3d[2]
    elif view_name == 'left':
        y = cursor3d[1]
        x = cursor3d[0]
    elif view_name == 'right':
        y = cursor3d[1]
        x = (width - 2) - cursor3d[0]
    return y, x


stdscr = curses.initscr()
cols = curses.COLS
lines = curses.LINES
width = cols // 2
height = lines // 2

width = min([height, width])
height = min([height, width])

data3d_blank = [[[' ' for x in range(width - 1)] for y in range(height - 1)] for z in range(height - 1)]
alldata3d = {}
if len(sys.argv) > 1:
    if os.path.isfile(f'{sys.argv[1]}.ascii3d'):
        with open(f'{sys.argv[1]}.ascii3d', 'r') as f:
            alldata3d = eval(f.read())



curses.noecho()
curses.cbreak()
stdscr.keypad(True)
begin_x = 0; begin_y = 0
wins = [[curses.newwin(height, width, begin_y, begin_x) for begin_x in [0,width]] for begin_y in [0, height]]
for win_rows in wins:
    for win in win_rows:
        win.keypad(True)

i = 0
j = 0
win = wins[i][j]
win.keypad(True)

xs = [[0,0],[0,0]]
ys = [[0,0],[0,0]]
cursor3d = [0,0,0]
ch = win.getkey()

def check_limits_any(indices, size):
    answer = indices.copy()
    for idx, value in enumerate(indices):
        if value >= size - 1:
            value = size - 2
        elif value < 1:
            value = 1
        answer[idx] = value
    return answer

def check_limits(y, x, height, width):
    if x < 0:
        x = 0
    elif x >= width:
        x = width - 1
    if y < 0:
        y = 0
    elif y >= height:
        y = height - 1
    return y, x

while ch != 'q':
    x = 0
    y = 0
    if ch == 'KEY_UP':
        ys[i][j] -= 1
        y = -1
    elif ch == 'KEY_DOWN':
        ys[i][j] += 1
        y = 1
    elif ch == 'KEY_LEFT':
        xs[i][j] -= 1
        x = -1
    elif ch == 'KEY_RIGHT':
        xs[i][j] += 1
        x = 1
    elif ch == 'k':
        i -= 1
    elif ch == 'j':
        i += 1
    elif ch == 'h':
        j -= 1
    elif ch == 'l':
        j += 1
    elif len(ch) == 1:
        alldata3d['{} {} {}'.format(*cursor3d)] = ch
        #data3d[cursor3d[0]][cursor3d[1]][cursor3d[2]] = ch
    i, j = check_limits(i, j, 2, 2)
    cursor3d = move3d(cursor3d, y, x, i, j)
    data3d = all_to_data3d(data3d_blank, alldata3d, cursor3d)
    for I in range(len(wins)):
        for J in range(len(wins[I])):
            wins[I][J].clear()
            for Y, row in enumerate(functions[f'{I} {J}'](data3d, height - 1, width - 1)):
                for X, cell in enumerate(row):
                    wins[I][J].addch(Y, X, cell)
            wins[I][J].refresh()
    win = wins[i][j]
    #y2, x2 = check_limits(ys[i][j], xs[i][j], height - 1, width - 1)
    c2d = [width//2, width//2]
    if views[f'{i} {j}'] == 'right':
        c2d[1] -= 2
    win.move(c2d[0], c2d[1])
    ch = win.getkey()





curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

with open(f'{sys.argv[1]}.ascii3d', 'w') as f:
    f.write(str(alldata3d))
