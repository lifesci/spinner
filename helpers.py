import math


def get_menu_positions(
    x, y, width, height, num_elements, num_cols=1, buffer_size=5, proportions=None
):
    num_rows = math.ceil(num_elements / num_cols)

    widths = _get_element_widths(width, num_cols, buffer_size, proportions)
    height = _get_element_height(height, num_rows, buffer_size)

    positions = []
    for i in range(num_elements):
        row = i // num_cols
        col = i % num_cols

        width = widths[col]
        x_pos = sum(widths[:col]) + buffer_size * (col + 1)
        y_pos = height * row + buffer_size * (row + 1)
        position = {"x": x_pos, "y": y_pos, "width": width, "height": height}
        positions.append(position)

    return positions


def _get_element_widths(width, num_cols, buffer_size, proportions):
    buffers = num_cols + 1
    remaining_width = width - buffers * buffer_size
    if proportions:
        widths = [remaining_width * proportion for proportion in proportions]
    else:
        widths = [remaining_width]
    return widths


def _get_element_height(height, num_rows, buffer_size):
    buffers = num_rows + 1
    remaining_height = height - buffers * buffer_size
    height = remaining_height / num_rows
    return height
