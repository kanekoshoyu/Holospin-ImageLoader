import serial
import time
import db
import logging
import sys
import colorlog
from typing import List


def printCursor(cursor):
    for record in cursor:
        logging.info(record, "\r\n")


def downloadImage(order_id: int):
    col = db.get_collection(db.DataBaseType.Order)
    logging.debug(col)
    myquery = {"order_id": order_id}
    cursor = col.find(myquery)
    printCursor(cursor)
    result = 0
    return result


def initLog():
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('my_log_info.log')
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


class PixArrayConfig:
    resolution: int = 8  # bits
    length: int = 16
    angle: int = 72


class Pixel(object):
    red: int = 255
    green: int = 255
    blue: int = 255

    def shift(self, bits: int):
        self.red >> bits
        self.green >> bits
        self.blue >> bits


class PixelProgrammer(serial.Serial):
    def __init__(self, port):
        try:
            super().__init__(
                port=port,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2  # seconds
            )
        except Exception as e:
            logging.warning("No UART found")
            return None

    def send_pixel(self, pixel: Pixel):
        self.write(pixel.red)
        self.write(pixel.green)
        self.write(pixel.blue)

    def send_pixarray(self, pixarray: List[List[Pixel]]):
        set_validation = False
        for index, angle in enumerate(pixarray):
            # angle element
            logging.info("Sending "+str(index))
            self.write(index)
            self.send_pixel(angle)
            if not set_validation:
                continue
            len = 0
            while len == 0:
                try:
                    rxline = serial.readline()
                    len = len(rxline)
                except:
                    logging.error("No reply from MCU")


def generatePixArray(config: PixArrayConfig, image) -> List[List[Pixel]]:
    arr = [[Pixel()]*config.length]*config.angle
    # fill in the array with data
    Pixel
    bitshift = 8 - config.resolution  # number of bits to be shifted
    return arr


def main():
    initLog()
    # logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("HAPS #2")
    # Function 1
    # Input OrderId
    # Output image
    logging.info("F1")

    db.list_collection(db.DataBaseType.Order)
    try:
        order_id = 0
        image = downloadImage(order_id)
        print(image)
    except Exception as e:
        logging.error("Function 1 error", e)
        return

    # Function 2
    # Input ,image
    # Output pixarrayf
    logging.info("F2")
    image = "Something"
    config = PixArrayConfig()
    pixarr = generatePixArray(config, image)

    # Function 3
    # Input pixarray
    # Output uart signal
    logging.info("F3")
    pp = PixelProgrammer('/dev/ttyUSB0')
    if not pp.is_open:
        logging.error("Oh no")
        return

    logging.info("Sending...")
    pp.write("hello\n".encode())
    pp.send_pixarray(pixarray)
    logging.info("Done")


if __name__ == "__main__":
    main()
