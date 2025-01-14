"""A place to test new WIP features"""
import rubato as rb
from rubato import Vector as V

width, height = 256, 256
speed = 2

rb.init(res=V(width, height), window_size=V(width, height) * 2)
s = rb.Scene()

rect = rb.Polygon(V.poly(5, width // 6), rb.Color.blue, offset=V(48, 0))
go = rb.wrap(rect, pos=rb.Display.center, debug=True)

dropper = rb.Rectangle(width=20, height=20, color=rb.Color.red, debug=True)
rigidbody = rb.RigidBody(gravity=V(0, -100))
extra = rb.wrap([dropper, rigidbody])

font = rb.Font()
font.size = 10
text = rb.Text("Hello World", font)


def update():
    go.rotation += speed
    rect.rot_offset += speed

    text.text = f"go.rotation: {go.rotation:.2f}\nrect.offset.x: {rect.offset.x:.2f}\nrect.rot_offset: {rect.rot_offset:.2f}"


def handler(m_event):
    if m_event["button"] == 1:
        e = extra.clone()
        e.pos = V(m_event["x"], m_event["y"])
        s.add(e)
    elif m_event["button"] == 3:
        rect._image.save_as("save_test", "test", "jpg", quality=90)


rb.Radio.listen(rb.Events.MOUSEDOWN, handler)

s.add(go, rb.wrap(text, pos=rb.Display.top_left + (50, -20)))
s.fixed_update = update

rb.begin()
