import math

def build_menu(
  x,
  y,
  width,
  height,
  num_elements,
  num_cols=1,
  with_titles=False,
  buffer_size=5
):

  num_rows = math.ceil(len(elements)/num_cols)
  if with_titles:
    num_rows += 1
  
  widths = _get_element_widths()
  height = _get_element_height(num_rows, buffer_size)

  positions = []
  for i in range(num_elements):
    row_pos = i%num_cols
    cur_x = x + buffer_size
    cur_y = y + buffer_size
    width = widths[row_pos]
    position = {
      "x": cur_x,
      "y": cur_y,
      "width": width,
      "height": height
    }
    positions.append(position)

def _get_element_widths(self):
  buffers = self.num_cols + 1
  remaining_width = self.width - buffers*self.buffer_size
  if self.col_data:
    widths = [remaining_width*col["proportion"] for col in self.col_data]
  else:
    widths = [remaining_width]
  return widths

def _get_element_height(height, num_rows, buffer_size):
  buffers = num_rows + 1
  remaining_height = height - buffers*buffer_size
  height =  remaining_height/num_rows
  return height
