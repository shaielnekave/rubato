"""
UI demo for rubato
"""
from rubato import *

init()
Game.show_fps = True

main = Scene()

txt = wrap(Text("Hello World!", Font(size=64), rot_offset=25), pos=Display.center, rotation=45)

main.add(txt)

Game.draw = lambda: Draw.rect(Display.center, 100, 100, Color.red)


def handle_key():
    txt.get(Text).offset += Vector(10, 0)


Radio.listen(Events.KEYDOWN, handle_key)

begin()
