#!/usr/bin/env python

from collections import deque

def cpu_temps():
    """Run sensors program and parse temperatures."""
    from os import popen
    from re import findall
    dta = popen('sensors').read()
    #print(dta)
    return map(float, findall(':\s*\+([\d\.]+)', dta))

def cpu_freq():
    from os import popen
    from re import findall
    dta = open('/proc/cpuinfo').read()
    #print(dta)
    return map(float, findall('cpu MHz\s*:\s*([\d\.]+)', dta))
    
def temp_graph():
    """Animate a graph with temperatures from sensors output."""
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.pyplot import plot, show, figure, draw, axis
    from time import time, sleep
    from threading import Thread
    init_temps = cpu_temps()
    window =[ deque([i]*300) for i in init_temps ]
    fig = figure()
    ax = fig.add_subplot(111)
    lines = [ ax.plot(win)[0] for win in window ]
    ax.axis([0, 300,
             min(30, min(init_temps)-10),
             max(60, max(init_temps)+10)])
    def update():
        if update.live and fig.canvas.manager.window:
            for i in xrange(len(init_temps)):
                window[i].append(cpu_temps()[i])
                window[i].popleft()
                lines[i].set_ydata(window[i])
            fig.canvas.draw()
            fig.canvas.manager.window.after(1000, update)
    update.live = True
    fig.canvas.manager.window.after(1000, update)
    def toggle(event):
        if update.live:
            update.live = False
        else:
            update.live = True
            fig.canvas.manager.window.after(100, update)
    fig.canvas.mpl_connect('key_press_event', toggle)
    show()    
        
if __name__=='__main__':
    temp_graph()
