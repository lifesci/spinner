import math

class Menu:
  def __init__(self, x, y, width, height, elements, col_data=None, buffer_size=5):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.elements = elements
    self.col_data = col_data
    self.buffer_size = buffer_size
    if col_data:
      num_cols = len(col_data)
    else:
      num_cols = 1
  
    self.num_cols = num_cols
    self.num_rows = math.ceil(len(elements)/num_cols)
    
  def _get_button_widths(self):
    buffers = self.num_cols + 1
    remaining_width = self.width - buffers*self.buffer_size
    if self.col_data:
      widths = [remaining_width*col["proportion"] for col in self.col_data]
    else:
      widths = [remaining_width]
    return widths

  def _get_button_height(self):
    buffers = self.num_rows + 1
    remaining_height = self.height - buffers*self.buffer_size
    return remaining_height/self.num_rows
