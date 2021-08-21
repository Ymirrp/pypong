
class Ball:
  def __init__(self, x, y, going_left=False, going_right=False, going_up=False, going_down=False, is_outside=False):
    self.x = x
    self.y = y
    self.going_left = going_left
    self.going_right = going_right
    self.going_up = going_up
    self.going_down = going_down
    self.is_outside = is_outside
