from PIL import Image
from __init__ import calculate

def render(num, name):
    imgs = []
    for i in range(0,15):
        imgs.append(Image.open("images/" + str(i) + ".png"))

    renderstring = calculate(int(num)).split(" ")

    canvas = Image.new('RGB', (125*7,125))

    for item in range(0,7):
        c = 125 * item
        canvas.paste(imgs[int(renderstring[item])], (c,0))

    canvas.save(name + '.jpg')


