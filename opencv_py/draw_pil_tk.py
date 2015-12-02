#!/usr/bin/env python

import Image
import ImageDraw
import ImageTk
import Tkinter
import random

SIZE = 300

# create an image
image = Image.new('RGB', (SIZE, SIZE))  # 'RGBA' - transparent

# draw something
draw = ImageDraw.Draw(image)
for _ in range(SIZE*SIZE/40):
    draw.point((random.randint(0, SIZE), random.randint(0, SIZE)), fill=(0, 0, 255))
for i in range(1, 6):
    draw.line((0, i * SIZE/10) + image.size, fill=(255, 255, 0))

# initialize Tkinter
root = Tkinter.Tk()

# load the image we created before
tk_image = ImageTk.PhotoImage(image)



# layout the window
root.geometry('{0}x{0}'.format(SIZE+10))
label_image = Tkinter.Label(root, image=tk_image)
# label_image.place(x=0, y=0, width=150, height=150)
label_image.pack()
root.mainloop()
