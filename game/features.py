from . import Rect


class V_tunnel(Rect.Rect):
    def __init__(self, x, y, l):
        super().__init__(x, y, 1, l)
        self.id = "v_tunnel"


class H_tunnel(Rect.Rect):
    def __init__(self, x, y, l):
        super().__init__(x, y, l, 1)
        self.id = "h_tunnel"


class Room(Rect.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.id = "room"
