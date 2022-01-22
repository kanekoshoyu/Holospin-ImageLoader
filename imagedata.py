from typing import List

class Pixel(object):
    red: int = 255
    green: int = 255
    blue: int = 255

    def shift(self, bits: int):
        self.red >> bits
        self.green >> bits
        self.blue >> bits


class WarpImage(object):
    # 8b rgb xy
    data: List[List[Pixel]]

    def __init__(self, data: List[List[Pixel]] = None):
        if not data:
            data = [[Pixel] * 5]*5
        self.data = data

    def serialised_line(self):
        return self.data[0][0]

    def count_section(self) -> int:
        # row
        return len(self.data)

    def count_radius(self) -> int:
        # column
        return len(self.data[0])
