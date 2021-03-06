"""An interactive mouse-based example

This script tracks whether mouse clicks hit a circle.

On the screen there's a circle with a fixed center and radius.  Mouse clicks
inside and outside the circle to change its color.

On click (and drag), mouse coordinates are fed into the ``mousex`` and
``mousey`` input nodes.  The ``distance`` node takes those coordinates as
inputs and outputs the distance to the center of the circle.  The result is fed
into the ``is_close`` node, which outputs a ``True`` value for distances
smaller than the circle radius.  The ``alert`` node returns a string whose
value depends on that boolean value.  Finally, the circle changes its color
based on the string in the ``alert`` node.

You can also observe debug output on the console.  Note how the distance
measurement is skipped if the coordinate inputs don't change.

If you have the graphviz tool installed, you'll also see a diagram of the graph
nodes and connections on the screen.  The diagram is saved in ``mouse.gif``.

"""


from lusmu.core import Input, Node, update_inputs
from lusmu.visualization import visualize_graph
import math
import Tkinter


TARGET = {'x': 90, 'y': 110}
RADIUS = 30


def get_distance(x, y):
    print ('Measuring distance from ({x}, {y}) to {t[x]}'
           .format(x=x, y=y, t=TARGET))
    dx = x - TARGET['x']
    dy = y - TARGET['y']
    return math.sqrt(dx ** 2 + dy ** 2)


def is_close_to_target(distance):
    return distance < RADIUS


def get_distance_description(is_close):
    return "INSIDE" if is_close else "OUTSIDE"


mousex = Input(name='mouse x')
mousey = Input(name='mouse y')
distance = Node(
    name='distance',
    action=get_distance,
    inputs=Node.inputs(mousex, mousey))
is_close = Node(
    name='is close',
    action=is_close_to_target,
    inputs=Node.inputs(distance))
alert = Node(
    name='alert',
    action=get_distance_description,
    inputs=Node.inputs(is_close))


def onclick(event):
    update_inputs([(mousex, event.x),
                   (mousey, event.y)])
    print 'distance.value == {:.1f}'.format(distance.value)
    print 'is_close.value == {!r}'.format(is_close.value)
    print 'alert.value == {!r}'.format(alert.value)
    print
    colors = {'INSIDE': 'red', 'OUTSIDE': 'blue'}
    draw_circle(colors[alert.value])


def draw_circle(color):
    tx = TARGET['x']
    ty = TARGET['y']
    canvas.create_oval(tx - RADIUS, ty - RADIUS, tx + RADIUS, ty + RADIUS,
                       fill=color)


root = Tkinter.Tk()
frame = Tkinter.Frame(root)
frame.pack(fill=Tkinter.BOTH, expand=1)
canvas = Tkinter.Canvas(frame, background='white')
draw_circle('blue')
canvas.pack(fill=Tkinter.BOTH, expand=1)
canvas.pack()
canvas.bind("<Button-1>", onclick)
canvas.bind("<B1-Motion>", onclick)

try:
    visualize_graph([alert], 'mouse.gif')
    print 'View mouse.gif to see a visualization of the traph.'
    diagram = Tkinter.PhotoImage(file='mouse.gif')
    canvas.create_image(0, 2 * (TARGET['y'] + RADIUS),
                        image=diagram, anchor='nw')
except OSError:
    print 'Please install graphviz to visualize the graph.'

root.mainloop()
